# Introdução ao Data Quality

## Fluxo

```mermaid
graph TD
    A[Configurar Variáveis] --> B[Ler o Banco SQL];
    B --> V[Validação do Schema de Entrada];
    B --> |Falha| X[Alerta de Erro];
    V --> |Falha| X[Alerta de Erro];
    V --> |Sucesso| C[Transformar os KPIs];
    C --> Y[Validação do Schema de Saída];
    Y --> |Falha| Z[Alerta de Erro];
    Y --> |Sucesso| D[Salvar no DuckDB];
```

## Contrato de dados
::: app.schema.ProdutoSchema