# 00_dimensional_modeling_docs.md

## Physical Data Model (Snowflake Schema)

### Design Decision: Snowflake over pure Star

* `dim_country` is shared between `dim_event` and `dim_athlete`, a deliberate snowflake extension to avoid duplicating country data across two dimensions.

* Documented as a conscious engineering decision, not a deviation from the assignment.

### IOC Standard for historical country codes
Historical nations (URS, YUG, TCH) are preserved as-is following IOC archival standards. Changing them to modern successor states would alter historical facts.