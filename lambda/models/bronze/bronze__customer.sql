SELECT 
    customer_id
    ,first_name
    ,last_name
    ,city
    ,date_of_birth
    ,loaded_at
FROM {{ source('staging','customer') }}