import pandera as pa
from pandera.typing import Series


class ProdutoSchema(pa.DataFrameModel):
    """
    Um modelo de esquema para validar um DataFrame contendo informações de produtos usando pandera.

    Atributos:
    ----------
    id_produto : Series[int]
        Um campo inteiro que representa o ID do produto. Este campo não é anulável e seus valores são convertidos para inteiros.

    nome : Series[str]
        Um campo de string que representa o nome do produto. Este campo não é anulável e seus valores são convertidos para strings.

    quantidade : Series[float]
        Um campo float que representa a quantidade do produto. Este campo tem uma restrição de intervalo com valores entre
        -150.0 e 500.0 (inclusive). Ele não é anulável e seus valores são convertidos para floats.

    preco : Series[float]
        Um campo float que representa o preço do produto. Este campo tem uma restrição de intervalo com valores entre
        2.0 e 2000.0 (inclusive). Ele não é anulável e seus valores são convertidos para floats.

    categoria : Series[str]
        Um campo de string que representa a categoria do produto. Este campo não é anulável e seus valores são convertidos para strings.

    Config:
    -------
    coerce : bool
        Uma configuração para garantir que os tipos de dados sejam convertidos conforme especificado.

    strict : bool
        Uma configuração para garantir a validação estrita do esquema.
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


class ProdutoSchemaKPI(ProdutoSchema):
    valor_total_estoque: Series[float] = pa.Field(
        ge=0
    )  # The total stock value must be >= 0
    categoria_normalizada: Series[
        str
    ]  # It is assumed that the category will be a string, no specific check is needed other than being a string
    disponibilidade: Series[
        bool
    ]  # Availability is a boolean, so no specific check is needed
