/* SAMPLE SCHEMA
    Policy Table:
        policy_id (Primary Key)
        policy_type
        coverage_details
        premium_amount
        start_date
        end_date
        customer_id (Foreign Key referencing Customers table)
*/

-- drop table staging.agent; 
-- GO
-- drop table staging.claim;
-- GO
-- drop table staging.customer;
-- GO
-- drop table staging.lead_blob;
-- GO
-- drop table staging.policy;
-- GO
-- 

create table staging.policy (
    policy_id varchar(64),
    policy_type varchar(32),
    coverage_details varchar(256),
    premium_amount numeric(18,4),
    start_date date,
    end_date date,
    customer_id varchar(64),
    loaded_at datetime
);
GO
/*
    Customer Table:
        customer_id (Primary Key)
        first_name
        last_name
        email
        phone_number
        address
        date_of_birth
*/
create table staging.customer (
    customer_id varchar(64),
    first_name varchar(32),
    last_name varchar(32),
    city varchar(32),
    date_of_birth date,
    loaded_at datetime
);
GO
/*
    Claim Table:
        claim_id (Primary Key)
        policy_id (Foreign Key referencing Policy table)
        customer_id (Foreign Key referencing Customers table)
        claim_date
        claim_amount
        claim_status
*/

create table staging.claim (
    claim_id varchar(64),
    policy_id varchar(64),
    customer_id varchar(64),
    claim_date date,
    claim_amount decimal(18,4),
    claim_status varchar(16), -- In Process, Approved, Pending, Denied
    loaded_at datetime
);
GO
/*
    Agent Table:
        agent_id (Primary Key)
        agent_name
        agent_email
        agent_phone
        agent_address
        hire_date
*/

create table staging.agent (
    agent_id varchar(64),
    first_name varchar(32),
    last_name varchar(32),
    city varchar(32),
    date_of_birth date,
    hire_date date,
    loaded_at datetime
);
GO
/*
    Lead Table:
        lead_id (Primary Key)
        lead_name
        lead_email
        lead_phone
        lead_address
        agent_id (Foreign Key referencing Agent table)
        lead_status (e.g., new, contacted, converted)
*/

create table lead (
    lead_id varchar(64),
    first_name varchar(32),
    last_name varchar(32),
    city varchar(64),
    date_of_birth date,
    agent_id varchar(64),
    lead_status varchar(16),  -- New, Contacted, In Process, Dropped, Converted
    loaded_at datetime
);
GO


create table customer_lead_mapping (
    lead_id varchar(64),
    customer_id varchar(64),
    conversion_timestamp datetime
);
GO

create table staging.lead_blob (
    bulk_column varchar(max),
    file_name varchar(512),
    loaded_at datetime
);

GO