import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.etl import transform


def test_calculo_valor_total_estoque():
    # Preparation
    df = pd.DataFrame(
        {
            "id_produto": [1, 2],
            "nome": ["Produto 1", "Produto 2"],
            "quantidade": [10, 5],
            "preco": [20.0, 100.0],
            "categoria": ["BrinQuedos", "Eletrônicos"],
            "email": ["test@gmail.com", "test@outlook.com"],
        }
    )
    expected = pd.Series([200.0, 500.0], name="valor_total_estoque")

    # Action
    result = transform(df)

    # Verification
    pd.testing.assert_series_equal(result["valor_total_estoque"], expected)


def test_normalizacao_categoria():
    # Preparation
    df = pd.DataFrame(
        {
            "id_produto": [1, 2],
            "nome": ["Produto 1", "Produto 2"],
            "quantidade": [10, 5],
            "preco": [20.0, 100.0],
            "categoria": ["BrinQuedos", "Eletrônicos"],
            "email": ["test@gmail.com", "test@outlook.com"],
        }
    )
    expected = pd.Series(["brinquedos", "eletrônicos"], name="categoria_normalizada")

    # Action
    result = transform(df)

    # Verification
    pd.testing.assert_series_equal(result["categoria_normalizada"], expected)


def test_determinacao_disponibilidade():
    # Preparation
    df = pd.DataFrame(
        {
            "id_produto": [1, 2],
            "nome": ["Produto 1", "Produto 2"],
            "quantidade": [10, 5],
            "preco": [20.0, 100.0],
            "categoria": ["BrinQuedos", "Eletrônicos"],
            "email": ["test@gmail.com", "test@outlook.com"],
        }
    )
    expected = pd.Series([True, True], name="disponibilidade")

    # Action
    result = transform(df)

    # Verification
    pd.testing.assert_series_equal(result["disponibilidade"], expected)

# Execute in a terminal with the command: pytest tests/test_func_etl.py on root folder