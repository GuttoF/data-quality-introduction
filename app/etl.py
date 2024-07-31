import os
from pathlib import Path

import pandas as pd
import pandera as pa
from dotenv import load_dotenv
from schema import ProdutoSchema
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
    # True se quantidade for maior que 0, False caso contrário
    df["disponibilidade"] = df["quantidade"] > 0
    
    return df


if __name__ == "__main__":
    query = "SELECT * FROM produtos_bronze"

    df_crm = extract(query=query)
    # schema_crm = pa.infer_schema(df_crm)

    # with open("schema_crm.py", "w", encoding="utf-8") as file:
    #    file.write(schema_crm.to_script())

    print(df_crm)
