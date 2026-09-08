FROM astrocrpublic.azurecr.io/runtime:3.3-7

USER root

RUN python -m venv dbt_venv && \
    ./dbt_venv/bin/pip install --no-cache-dir --upgrade pip && \
    ./dbt_venv/bin/pip install --no-cache-dir dbt-snowflake>=1.8.0

USER astro
