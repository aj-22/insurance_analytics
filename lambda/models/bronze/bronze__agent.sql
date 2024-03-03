select 
agent_id,
first_name,
last_name,
city,
date_of_birth,
hire_date,
loaded_at
from {{ source('staging','agent') }}