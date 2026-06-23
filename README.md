# Zoo Management System

A database management project developed as a **group project** for the Database Systems course at **Instituto Superior Técnico**.

The project models and manages different areas of a zoo, including zones, enclosures, species, animals, ticket sales, visitor access and voting.

## Group project

This project was developed collaboratively by a team of students.

The implementation, database design, data generation, SQL queries, constraints, triggers and API endpoints were completed as part of the group work.

Individual contributions are not separated in this repository, since the project was developed collaboratively.

## Main features

* Relational database design using PostgreSQL
* Management of zoo zones and enclosures
* Management of species and animals
* Ticket sales and access control
* Visitor voting system
* Data generation and population scripts
* SQL constraints and triggers
* Flask API endpoints
* Transaction handling
* Validation and analysis using Jupyter Notebook

## Technologies

* Python
* Flask
* PostgreSQL
* SQL
* Psycopg
* Jupyter Notebook

## Project structure

```text
zoo-management-system/
├── app.py
├── populate.py
├── zonas.sql
├── recintos.sql
├── especies.sql
├── animais.sql
├── zoo123.sql
├── zoo-management-system.ipynb
├── requirements.txt
├── LICENSE.md
└── README.md
```

## Course-provided material

The initial Flask application template and deployment configuration were provided by the course staff.

The original copyright notices and license information were preserved.

## Group contributions

The group was responsible for:

* database modelling;
* schema definition;
* constraints and triggers;
* generation and population of test data;
* SQL queries;
* Flask API endpoints;
* transaction handling;
* testing and validation;
* project documentation.

## Running the project

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Set the PostgreSQL connection using the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgres://username:password@hostname/database"
```

Run the application:

```bash
python app.py
```

## License

The Flask template is distributed under the Modified BSD License.

See `LICENSE.md` for further information.
