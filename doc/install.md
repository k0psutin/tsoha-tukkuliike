# Install instructions

Navigate to a empty folder and clone the repository from GitHub:

```
git clone https://github.com/k0psutin/tsoha-tukkuliike
```

Make sure you have at least PostgreSQL 13.x version installed.
[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Create a `.env` file to the root of program folder:

```
SECRET_KEY=<secret>
DATABASE_URL=postgres+psycopg2://<username>:<password>@<url>:<port><database>
```

Type a random string for `<secret>`-attribute, or generate MD5 string online.

Replace `<username>` and `<password>` attributes with your PostgreSQL credentials, `<database>`with the name of the database. Replace `<url>` and `<port>` with database address and port.

## Setup database

Directory `\db` contains the schema for the databse as `schema.sql`. Bring it to PostgreSQL with the following command:

```
psql < db\schema.sql
```

If you don't want to use mock data, skip over the next part.

## Mock data

Directory `\db` contains mock data for testing. To use the mock data, use the following command (small has 30 rows and large 100.):

```
psql < db\users.sql
psql < db\mock_companies_small.sql
psql < db\mock_items_small.sql
psql < db\mock_supply_orders_small.sql
psql < db\mock_sale_orders_small.sql
```

Note that the order of imports are crucial. Mock data uses data from other tables, and gives an error if there are no specific entries.

## Preparing application for launch

Create a new virtual environment:

```
python 3 -m venv venv
```

Activate virtual environment:

```
source venv/bin/activate (linux)
```

or

```
venv\Scripts\activate (windows)
```

Install the required libraries with:

```
pip install -r requirements.txt
```

## Creating a user

If you choose not to import any of the data, you can create a new controller user with:

```
flask init
```

Start the application with:

```
flask run
```

Open the application at [http://localhost:5000/](http://localhost:5000/)
