{{config(materialized='table')}}



with duplicates as (

    SELECT razon_social,nombre_comercial,giro,sector,
    ROW_NUMBER() OVER(PARTITION BY razon_social ORDER BY razon_social DESC) as row_num FROM {{ref('complaints_stage')}}

)

SELECT *,  
        {{dbt_utils.generate_surrogate_key(['razon_social','nombre_comercial','giro','sector'])}} as razon_social_key
                 FROM duplicates
                 WHERE row_num = 1
   
