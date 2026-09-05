FROM quay.io/astronomer/astro-runtime:11.3.0

# Install dbt-snowflake into a virtual environment
RUN python -m venv dbt_venv && \
    ./dbt_venv/bin/pip install --no-cache-dir dbt-snowflake
