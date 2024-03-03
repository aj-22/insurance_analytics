{% macro convert_tz_to_UTC(column_name) %} {{ column_name }} AT TIME ZONE 'India Standard Time' AT TIME ZONE 'UTC' {% endmacro %}


{% macro lambda_filter(column_name) %}

{%- set materialized = config.require('materialized') -%}

{%- set filter_time = run_started_at -%}

{%- if materialized == 'view' -%}

where {{ convert_tz_to_UTC(column_name) }} >= '{{ filter_time }}'

{%- elif is_incremental() -%}

where {{ column_name }} >= (select max({{ column_name }}) from {{ this }})

and {{ convert_tz_to_UTC(column_name) }} < '{{ filter_time }}'

{%- else -%}

where {{ convert_tz_to_UTC(column_name) }} < '{{ filter_time }}'

{%- endif -%}

{% endmacro %}