--- This script is used as a backup for the RBAC hierarchy

--- Using super user account
USE ROLE ACCOUNTADMIN;


--- Creating the dbt_wh to do the transformations

DROP WAREHOUSE IF EXISTS DBT_WH;
CREATE WAREHOUSE DBT_WH WITH warehouse_size = 'x-small' auto_suspend = 60;


DROP DATABASE IF EXISTS COMPLAINTS_DB;
--- Creating the database (where all the transformations happen)
CREATE DATABASE COMPLAINTS_DB;

--- Creating the schemas that serve as the medallion architecture

CREATE SCHEMA COMPLAINTS_BRONZE;

CREATE SCHEMA COMPLAINTS_SILVER;

CREATE SCHEMA COMPLAINTS_GOLD;


DROP ROLE IF EXISTS DBT_ROLE;
--- Creating the role to do the transformations
CREATE ROLE DBT_ROLE;

--- Grant the following permissions to the roles and users:
--  - usage of the warehouse to dbt_role
--  - grant all permissions of the database to dbt_role
--  - grant create tables on schemas to dbt_role
--  - grant role to user

-- usage of the warehouse to dbt_role
GRANT USAGE ON WAREHOUSE DBT_WH TO DBT_ROLE;


-- grant all permissions of the database to dbt_role
GRANT ALL ON DATABASE COMPLAINTS_DB TO DBT_ROLE;

-- grant create tables on schemas to dbt_role
GRANT CREATE TABLE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_BRONZE TO ROLE DBT_ROLE;
GRANT CREATE TABLE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_SILVER TO ROLE DBT_ROLE;
GRANT CREATE TABLE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_GOLD TO ROLE DBT_ROLE;

--- Grant usages of the schemas to dbt role
GRANT USAGE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_BRONZE TO ROLE DBT_ROLE;
GRANT USAGE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_SILVER TO ROLE DBT_ROLE;
GRANT USAGE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_GOLD TO ROLE DBT_ROLE;

--- Grant create to stages of the schemas to dbt role
GRANT CREATE STAGE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_BRONZE TO ROLE DBT_ROLE;
GRANT CREATE STAGE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_SILVER TO ROLE DBT_ROLE;
GRANT CREATE STAGE ON SCHEMA COMPLAINTS_DB.COMPLAINTS_GOLD TO ROLE DBT_ROLE;

--- Grant all privileges of the schemas to dbt role
GRANT ALL PRIVILEGES ON SCHEMA COMPLAINTS_DB.COMPLAINTS_BRONZE TO ROLE DBT_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA COMPLAINTS_DB.COMPLAINTS_SILVER TO ROLE DBT_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA COMPLAINTS_DB.COMPLAINTS_GOLD TO ROLE DBT_ROLE;

-- Finally grant role to users

GRANT ROLE DBT_ROLE TO USER SHADOW750098;

-- Btw we have to create the format
CREATE OR REPLACE FILE FORMAT COMPLAINTS_BRONZE.CSV
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  EMPTY_FIELD_AS_NULL = TRUE
  PARSE_HEADER = TRUE;



-- And the stage
CREATE STAGE COMPLAINTS_DB.COMPLAINTS_BRONZE.DBT_STAGE;


-- Creating the stage table
CREATE OR REPLACE TABLE COMPLAINTS_DB.COMPLAINTS_BRONZE.BRONZE_COMPLAINTS (
    expediente          VARCHAR(50)    NOT NULL, -- Identificador único del expediente
    fecha_ingreso       DATE           NOT NULL, -- Fecha de recepción
    anio_creacion       SMALLINT       NOT NULL, -- Año (extraído o definido)
    estado_procesal     VARCHAR(100),            -- Estatus actual del proceso
    razon_social        VARCHAR(255),            -- Nombre legal de la empresa
    nombre_comercial    VARCHAR(255),            -- Nombre de marca
    giro                VARCHAR(150),            -- Actividad específica
    sector              VARCHAR(100),            -- Sector económico
    area_responsable    VARCHAR(100),            -- Unidad interna que atiende
    estado              VARCHAR(50),             -- Estado geográfico o ubicación
    motivo_reclamacion  VARCHAR(1000),           -- Descripción breve del motivo
    
    -- Metadatos útiles para auditoría en Snowflake/Airflow
    fecha_carga_dw      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);