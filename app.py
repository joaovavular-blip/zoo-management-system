#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.

"""Flask API for the Zoo Management System."""

import os
from decimal import Decimal
from logging.config import dictConfig
from typing import Any

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from psycopg import Error as PsycopgError
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": (
                    "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s "
                    "- %(funcName)s(): %(message)s"
                ),
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://app:app@postgres/app",
)

app = Flask(__name__)
app.config.from_prefixed_env()

log = app.logger

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=RATELIMIT_STORAGE_URI,
)

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,
        "row_factory": dict_row,
    },
    min_size=1,
    max_size=10,
    open=True,
    name="postgres_pool",
    timeout=5,
)


def error_response(message: str, status_code: int):
    """Create a consistent JSON error response."""
    return jsonify({"message": message, "status": "error"}), status_code


def parse_sale_payload(data: Any):
    """Validate and normalize the JSON body used to create a sale."""
    if not isinstance(data, dict):
        raise ValueError("The request body must be a JSON object.")

    tickets = data.get("bilhetes")
    if not isinstance(tickets, list) or not tickets:
        raise ValueError("'bilhetes' must be a non-empty list.")

    normalized_tickets = []

    for index, ticket in enumerate(tickets, start=1):
        if not isinstance(ticket, dict):
            raise ValueError(f"Ticket {index} must be a JSON object.")

        zone_ids = ticket.get("id_zona")
        if not isinstance(zone_ids, list) or not zone_ids:
            raise ValueError(
                f"Ticket {index} must contain a non-empty 'id_zona' list."
            )

        if not all(isinstance(zone_id, int) and zone_id > 0 for zone_id in zone_ids):
            raise ValueError(
                f"All zone IDs in ticket {index} must be positive integers."
            )

        if len(zone_ids) != len(set(zone_ids)):
            raise ValueError(f"Ticket {index} contains repeated zone IDs.")

        discount = ticket.get("desconto", 0)

        if isinstance(discount, bool) or not isinstance(discount, (int, float)):
            raise ValueError(
                f"The discount in ticket {index} must be a number between 0 and 1."
            )

        discount_decimal = Decimal(str(discount))

        if not Decimal("0") <= discount_decimal <= Decimal("1"):
            raise ValueError(
                f"The discount in ticket {index} must be between 0 and 1."
            )

        normalized_tickets.append(
            {
                "zone_ids": zone_ids,
                "discount": discount_decimal,
            }
        )

    nif = data.get("NIF")

    if nif is not None:
        nif = str(nif).strip()
        if not nif.isdigit() or len(nif) != 9:
            raise ValueError("'NIF' must contain exactly 9 digits.")

    return nif, normalized_tickets


@app.errorhandler(PsycopgError)
def handle_database_error(error: PsycopgError):
    """Return a generic response for unexpected database errors."""
    log.exception("Database error: %s", error)
    return error_response("A database error occurred.", 500)


@app.route("/zona/<int:id_zona>", methods=("GET",))
@app.route("/zona/<int:id_zona>/", methods=("GET",))
@limiter.limit("1 per second")
def zone_index(id_zona: int):
    """Return the enclosures and species belonging to a zoo zone."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1
                FROM zona
                WHERE id_zona = %(id_zona)s;
                """,
                {"id_zona": id_zona},
            )

            if cur.fetchone() is None:
                return error_response("Zone not found.", 404)

            cur.execute(
                """
                SELECT
                    a.id_recinto,
                    a.nome_cientifico,
                    e.nome_comum,
                    COUNT(*) AS num_animais
                FROM animal AS a
                JOIN recinto AS r
                    ON r.id_recinto = a.id_recinto
                JOIN especie AS e
                    ON e.nome_cientifico = a.nome_cientifico
                WHERE r.id_zona = %(id_zona)s
                GROUP BY
                    a.id_recinto,
                    a.nome_cientifico,
                    e.nome_comum
                ORDER BY
                    a.id_recinto,
                    e.nome_comum;
                """,
                {"id_zona": id_zona},
            )

            enclosures = cur.fetchall()

    return jsonify(enclosures), 200


@app.route(
    "/recinto/<int:id_recinto>/voto/<int:bid_bilhete>",
    methods=("PUT",),
)
@app.route(
    "/recinto/<int:id_recinto>/voto/<int:bid_bilhete>/",
    methods=("PUT",),
)
@limiter.limit("1 per second")
def recinto_voto_save(id_recinto: int, bid_bilhete: int):
    """Register one ticket vote for an accessible enclosure."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            with conn.transaction():
                cur.execute(
                    """
                    SELECT votou
                    FROM bilhete
                    WHERE bid = %(bid)s
                    FOR UPDATE;
                    """,
                    {"bid": bid_bilhete},
                )
                ticket = cur.fetchone()

                if ticket is None:
                    return error_response("Ticket not found.", 404)

                if ticket["votou"]:
                    return error_response("This ticket has already voted.", 409)

                cur.execute(
                    """
                    SELECT id_zona
                    FROM recinto
                    WHERE id_recinto = %(id_recinto)s;
                    """,
                    {"id_recinto": id_recinto},
                )
                enclosure = cur.fetchone()

                if enclosure is None:
                    return error_response("Enclosure not found.", 404)

                cur.execute(
                    """
                    SELECT 1
                    FROM acesso
                    WHERE bid = %(bid)s
                      AND id_zona = %(id_zona)s;
                    """,
                    {
                        "bid": bid_bilhete,
                        "id_zona": enclosure["id_zona"],
                    },
                )

                if cur.fetchone() is None:
                    return error_response(
                        "The ticket does not provide access to this enclosure.",
                        403,
                    )

                cur.execute(
                    """
                    UPDATE bilhete
                    SET votou = TRUE
                    WHERE bid = %(bid)s;
                    """,
                    {"bid": bid_bilhete},
                )

                cur.execute(
                    """
                    UPDATE recinto
                    SET votos = COALESCE(votos, 0) + 1
                    WHERE id_recinto = %(id_recinto)s;
                    """,
                    {"id_recinto": id_recinto},
                )

    return "", 204


@app.route("/venda", methods=("POST",))
@app.route("/venda/", methods=("POST",))
def add_venda():
    """Create a sale with tickets and their corresponding zone access."""
    try:
        nif, tickets = parse_sale_payload(request.get_json(silent=True))
    except ValueError as error:
        return error_response(str(error), 400)

    all_zone_ids = sorted(
        {
            zone_id
            for ticket in tickets
            for zone_id in ticket["zone_ids"]
        }
    )

    with pool.connection() as conn:
        with conn.cursor() as cur:
            with conn.transaction():
                cur.execute(
                    """
                    SELECT id_zona, preco
                    FROM zona
                    WHERE id_zona = ANY(%(zone_ids)s);
                    """,
                    {"zone_ids": all_zone_ids},
                )

                zone_prices = {
                    row["id_zona"]: Decimal(str(row["preco"]))
                    for row in cur.fetchall()
                }

                missing_zone_ids = [
                    zone_id
                    for zone_id in all_zone_ids
                    if zone_id not in zone_prices
                ]

                if missing_zone_ids:
                    missing = ", ".join(map(str, missing_zone_ids))
                    return error_response(
                        f"Unknown zone IDs: {missing}.",
                        400,
                    )

                cur.execute(
                    """
                    INSERT INTO venda (data_hora, nif_cliente)
                    VALUES (CURRENT_TIMESTAMP, %(nif)s)
                    RETURNING no_venda;
                    """,
                    {"nif": nif},
                )
                sale_number = cur.fetchone()["no_venda"]

                created_tickets = []
                total_price = Decimal("0")

                for ticket in tickets:
                    discount = ticket["discount"]

                    cur.execute(
                        """
                        INSERT INTO bilhete (desconto, votou, no_venda)
                        VALUES (%(discount)s, FALSE, %(sale_number)s)
                        RETURNING bid;
                        """,
                        {
                            "discount": discount,
                            "sale_number": sale_number,
                        },
                    )
                    ticket_id = cur.fetchone()["bid"]

                    ticket_price = Decimal("0")

                    for zone_id in ticket["zone_ids"]:
                        cur.execute(
                            """
                            INSERT INTO acesso (bid, id_zona)
                            VALUES (%(ticket_id)s, %(zone_id)s);
                            """,
                            {
                                "ticket_id": ticket_id,
                                "zone_id": zone_id,
                            },
                        )

                        ticket_price += (
                            zone_prices[zone_id]
                            * (Decimal("1") - discount)
                        )

                    ticket_price = ticket_price.quantize(Decimal("0.01"))
                    total_price += ticket_price

                    created_tickets.append(
                        {
                            "bid": ticket_id,
                            "preco": float(ticket_price),
                        }
                    )

    response = {
        "no_venda": sale_number,
        "preco_total": float(total_price.quantize(Decimal("0.01"))),
        "bilhetes": created_tickets,
    }

    return jsonify(response), 201


@app.route("/ping", methods=("GET",))
@limiter.exempt
def ping():
    """Return a simple health-check response."""
    return jsonify({"message": "pong!", "status": "success"}), 200


if __name__ == "__main__":
    app.run()
