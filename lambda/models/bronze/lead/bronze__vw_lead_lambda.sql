with unioned as (
    select 
        lead_id,
        first_name,
        last_name,
        city,
        date_of_birth,
        agent_id,
        lead_status,
        loaded_at
    from {{ ref('bronze__vw_lead_fresh') }}
    union all
    select 
        lead_id,
        first_name,
        last_name,
        city,
        date_of_birth,
        agent_id,
        lead_status,
        loaded_at
    from {{ ref('bronze__tbl_lead_hist') }}
),
numbered as (
    select
    *, row_number() over (partition by lead_id order by loaded_at desc) as rn 
    from unioned
)
select * from numbered where rn = 1









