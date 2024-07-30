import pandera as pa
from pandera.typing import Series


class ProdutoSchema(pa.DataFrameModel):
    """
    A schema model for validating a DataFrame containing product information using pandera.

    Attributes:
    -----------
    id_produto : Series[int]
        An integer field representing the product ID. This field is not nullable and its values are coerced to integers.

    nome : Series[str]
        A string field representing the product name. This field is not nullable and its values are coerced to strings.

    quantidade : Series[float]
        A float field representing the quantity of the product. This field has a range constraint with values
        between -150.0 and 500.0 (inclusive). It is not nullable and its values are coerced to floats.

    preco : Series[float]
        A float field representing the price of the product. This field has a range constraint with values
        between 2.0 and 2000.0 (inclusive). It is not nullable and its values are coerced to floats.

    categoria : Series[str]
        A string field representing the product category. This field is not nullable and its values are coerced to strings.

    Config:
    -------
    coerce : bool
        A configuration setting to ensure that the data types are coerced as specified.

    strict : bool
        A configuration setting to ensure strict validation of the schema.
    """

    id_produto: Series[int] = pa.Field(nullable=False, coerce=True)
    nome: Series[str] = pa.Field(nullable=False, coerce=True)
    quantidade: Series[float] = pa.Field(
        ge=-150.0, le=500.0, nullable=False, coerce=True
    )
    preco: Series[float] = pa.Field(ge=2.0, le=2000.0, nullable=False, coerce=True)
    categoria: Series[str] = pa.Field(nullable=False, coerce=True)

    class Config:
        coerce = True
        strict = True
