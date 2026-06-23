# Zoo Management System

A database management project developed as a **group project** for the Database Systems course at **Instituto Superior Técnico**.

The project models and manages different areas of a zoo, including zones, enclosures, species, animals, ticket sales, visitor access and voting.

## Group project

This project was developed collaboratively by a team of students.

The database design, data generation, SQL queries, constraints, triggers, API endpoints, testing and validation were completed as part of the group work.

Individual contributions are not separated in this repository because the project was developed collaboratively.

## Main features

* Relational database design using PostgreSQL
* Management of zoo zones and enclosures
* Management of species and animals
* Ticket sales and zone access control
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
├── zoo-management-system.ipynb
├── requirements.txt
├── LICENSE.md
├── README.md
└── data/
    ├── populate.py
    ├── zonas.sql
    ├── recintos.sql
    ├── especies.sql
    ├── animais.sql
    └── demo_100_sales.sql
```

## Demo dataset

The original project generated a substantially larger dataset in order to satisfy the course requirements.

A reduced dataset with 100 sales is included in:

```text
data/demo_100_sales.sql
```

This smaller dataset is intended for demonstration and easier inspection on GitHub.

The complete dataset can be generated using the population script.

## Course-provided material

The initial Flask application template and deployment configuration were provided by the course staff.

The original copyright notices and license information have been preserved.

## Group contributions

The group was responsible for:

* database modelling;
* schema definition;
* database constraints and triggers;
* generation and population of test data;
* SQL queries;
* Flask API endpoints;
* transaction handling;
* testing and validation;
* project documentation.

## Running the project

### 1. Install the dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the database connection

Set the PostgreSQL connection through the `DATABASE_URL` environment variable.

Linux or macOS:

```bash
export DATABASE_URL="postgres://username:password@hostname/database"
```

Windows PowerShell:

```powershell
$env:DATABASE_URL="postgres://username:password@hostname/database"
```

### 3. Create and populate the database

Before starting the API, create the PostgreSQL database structure and populate it using:

* `zoo-management-system.ipynb`;
* the SQL files inside the `data/` directory;
* `data/demo_100_sales.sql` for the reduced demonstration dataset.

The full dataset can also be generated through:

```bash
python data/populate.py > data/zoo123.sql
```

The generated `zoo123.sql` file is intentionally not included in the repository because of its size.

### 4. Start the API

```bash
python app.py
```

The API includes endpoints for:

* listing the enclosures and species of a zone;
* registering a visitor vote;
* creating ticket sales;
* checking whether the application is running.

## API examples

### Health check

```http
GET /ping
```

### View a zoo zone

```http
GET /zona/1
```

### Register a vote

```http
PUT /recinto/1/voto/1
```

### Create a sale

```http
POST /venda
Content-Type: application/json
```

Example request body:

```json
{
  "NIF": "123456789",
  "bilhetes": [
    {
      "id_zona": [1, 2, 3],
      "desconto": 0.5
    }
  ]
}
```

## License

The Flask template is distributed under the Modified BSD License.

See `LICENSE.md` for further information.
