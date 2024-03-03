select 
lead_id,
customer_id,
conversion_timestamp
from {{ source('staging','customer_lead_mapping') }}