{{config(materialized='table')}}

select
    expediente,
    fecha_ingreso,
    anio_creacion,
    estado_procesal,
    motivo_reclamacion,
    fecha_actualizacion,
    num_observacion,
    dim_zonas.dim_zonas_key,
    dim_razon_social.razon_social_key
FROM {{ref('complaints_stage')}} stage
JOIN {{ref('dim_zonas')}} dim_zonas
ON dim_zonas.area_responsable = stage.area_responsable
AND dim_zonas.is_current = 1
JOIN {{ref('dim_razon_social')}} dim_razon_social
ON dim_razon_social.razon_social = stage.razon_social
AND dim_razon_social.is_current = 1




