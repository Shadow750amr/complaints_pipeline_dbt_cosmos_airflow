{% snapshot dim_zonas_snapshot %}

{{
  config(
    target_schema='snapshots',
    strategy='check',
    unique_key='area_responsable',
    check_cols= ['estado']
  )
}}

select * from {{ ref('dim_zonas_stage') }}

{% endsnapshot %}