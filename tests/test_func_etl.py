import pandas as pd

from app.etl import transform


def test_calculo_valor_total_estoque():
    # Preparation
    df = pd.DataFrame(
        {
            "quantidade": [10, 5],
            "preco": [20.0, 100.0],
            "categoria": ["brinquedos", "eletrônicos"],
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
            "quantidade": [1, 2],
            "preco": [10.0, 20.0],
            "categoria": ["brinquedos", "eletrônicos"],
        }
    )
    expected = pd.Series(["BRINQUEDOS", "ELETRÔNICOS"], name="categoria_normalizada")

    # Action
    result = transform(df)

    # Verification
    pd.testing.assert_series_equal(result["categoria_normalizada"], expected)


def test_determinacao_disponibilidade():
    # Preparation
    df = pd.DataFrame(
        {
            "quantidade": [0, 2],
            "preco": [10.0, 20.0],
            "categoria": ["brinquedos", "eletrônicos"],
        }
    )
    expected = pd.Series([False, True], name="disponibilidade")

    # Action
    result = transform(df)

    # Verification
    pd.testing.assert_series_equal(result["disponibilidade"], expected)
