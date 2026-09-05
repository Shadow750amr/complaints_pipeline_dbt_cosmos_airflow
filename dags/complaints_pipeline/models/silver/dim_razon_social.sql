{{config(materialized='table')}}

SELECT 
    razon_social,
        nombre_comercial,
            giro,
                sector,
                    razon_social_key,
                    dbt_updated_at as updated_at,
                        dbt_valid_from as start_date,
                            dbt_valid_to as end_date,
                                CASE WHEN dbt_valid_to is null then 1 else 0 end as is_current
FROM {{ref('razon_social_snapshot')}}