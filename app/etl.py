import os
from pathlib import Path

import duckdb
import pandas as pd
import pandera as pa
from dotenv import load_dotenv
from schema import ProdutoSchema, ProdutoSchemaKPI
from schema_email import ProdutoSchemaEmail
from sqlalchemy import create_engine


def load_settings():
    dotenv_path = Path.cwd() / ".env"
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT"),
    }

    return settings


@pa.check_output(ProdutoSchema, lazy=True)
@pa.check_output(ProdutoSchemaEmail, lazy=True)
def extract(query: str) -> pd.DataFrame:
    """
    Extracts data from a PostgreSQL database using the provided query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The extracted data as a pandas DataFrame.
    """
    settings = load_settings()

    # create connection string
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"

    # create sqlalchemy engine
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
        df_crm = pd.read_sql(query, conn)

    return df_crm


@pa.check_input(ProdutoSchema, lazy=True)
@pa.check_output(ProdutoSchemaKPI, lazy=True)
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the given DataFrame by adding new columns and modifying existing ones.

    Args:
        df (pd.DataFrame): The input DataFrame to be transformed.

    Returns:
        pd.DataFrame: The transformed DataFrame.
    """
    df["valor_total_estoque"] = df["quantidade"] * df["preco"]
    df["categoria_normalizada"] = df["categoria"].str.lower()
    # True if the product is available, False otherwise
    df["disponibilidade"] = df["quantidade"] > 0

    return df


def load(df: pd.DataFrame, table_name: str, db_file: str = "duckdb_file.db"):
    """
    Loads the given DataFrame into a DuckDB database.

    Args:
        df (pd.DataFrame): The DataFrame to load into the database.
        table_name (str): The name of the table to create in the database.
        db_file (str): The path to the DuckDB database file.
    """
    # create a connection to the database
    conn = duckdb.connect(database=db_file, read_only=False)

    # load the DataFrame into the database
    conn.register("df_temp", df)
    conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_temp")

    # close the connection
    conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM produtos_bronze_email"

    df_crm = extract(query=query)
    df_crm_kpi = transform(df_crm)

    with open("infer_schema.json", "r") as file:
        file.write(df_crm_kpi.to_json())

    load(df_crm_kpi, table_name="tabela_kpi")
