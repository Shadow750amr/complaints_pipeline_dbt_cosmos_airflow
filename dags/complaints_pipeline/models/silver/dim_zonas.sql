{{config(materialized='incremental',incremental_strategy='merge',unique_key='dim_zonas_key',on_schema_change='append_new_columns')}}


SELECT area_responsable,
        estado,
                dbt_updated_at as updated_at,
                        dbt_valid_from as start_date,
                            dbt_valid_to as end_date,
                                CASE WHEN dbt_valid_to is null then 1 else 0 end as is_current,
                                {{dbt_utils.generate_surrogate_key(['area_responsable','dbt_updated_at'])}} as dim_zonas_key 
FROM {{ref('dim_zonas_snapshot')}}