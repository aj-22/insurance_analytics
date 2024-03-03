SELECT
    policy_id
    ,policy_type
    ,coverage_details
    ,premium_amount
    ,start_date
    ,end_date
    ,customer_id
    ,loaded_at
FROM {{ source('staging','policy') }}
