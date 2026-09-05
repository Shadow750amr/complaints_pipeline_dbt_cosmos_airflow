{%snapshot razon_social_snapshot%}


{{
  config(
    target_schema='snapshots',
    strategy='check',
    unique_key='razon_social',
    check_cols= ['nombre_comercial','giro','sector']
  )
}}


SELECT * FROM {{ref('razon_social_stage')}}

{% endsnapshot %}