{% macro create_row_id(columns) -%}
{% for col in columns %}'[' + {{ col }} + ']' {% if not loop.last %}+{% endif %}{% endfor %}
{%- endmacro %}
