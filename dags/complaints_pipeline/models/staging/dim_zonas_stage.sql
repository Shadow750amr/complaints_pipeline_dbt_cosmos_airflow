
{{config(
    materialized='table'
    )}}


with duplicates as (

    SELECT area_responsable, estado,
                    ROW_NUMBER() OVER(PARTITION BY area_responsable ORDER BY area_responsable DESC) as row_num 
                                 FROM {{ref('complaints_stage')}}

)

SELECT *, {{dbt_utils.generate_surrogate_key(['area_responsable','estado'])}} as s_key_estado FROM duplicates WHERE row_num = 1



