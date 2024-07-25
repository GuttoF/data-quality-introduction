# Introdução ao Data Quality

Para resolver o problema, iremos utilizar o seguinte esquema de ETL:

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

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
