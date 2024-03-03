with open_json as (
    select
    JSON_VALUE(bulk_column, '$.lead_id') AS lead_id,
    JSON_VALUE(bulk_column, '$.first_name') AS first_name,
    JSON_VALUE(bulk_column, '$.last_name') AS last_name,
    JSON_VALUE(bulk_column, '$.city') AS city,
    JSON_VALUE(bulk_column, '$.date_of_birth') AS date_of_birth,
    JSON_VALUE(bulk_column, '$.agent_id') AS agent_id,
    JSON_VALUE(bulk_column, '$.lead_status') AS lead_status,
    loaded_at
    from {{ source('staging','lead_blob')}}
    {{ lambda_filter('loaded_at') }}
)
select
    cast(lead_id as varchar(64)) as lead_id,
    cast(first_name as varchar(32)) as first_name,
    cast(last_name as varchar(32)) as last_name,
    cast(city as varchar(64)) as city,
    cast(date_of_birth as date) as date_of_birth,
    cast(agent_id as varchar(64)) as agent_id,
    cast(lead_status as varchar(16)) as lead_status,
    cast(loaded_at as datetime) as loaded_at
from open_json