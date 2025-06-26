SELECT
    -- Use COALESCE to get organisation unit name.
    -- If 'ou.name' column exists and has a value, use it.
    -- Otherwise, fall back to the organisationunitid converted to text.
    -- Assuming 'organisationunitid' exists in the 'organisationunit' table for the join.
    COALESCE(ou.name, ou.organisationunitid::text) AS organisation_unit_name,
    ou.organisationunitid AS organisation_unit_id, -- Explicitly include the original ID
    ou.hierarchylevel AS organisation_unit_level, -- Assuming this column exists for hierarchy
    de.name AS data_element_name, -- Assuming 'name' exists in 'dataelement'
    -- Derive period_iso from period.startdate as period.iso is not present
    TO_CHAR(p.startdate, 'YYYY-MM') AS period_iso,
    p.startdate AS period_start_date,
    p.enddate AS period_end_date,
    coc.name AS category_option_combo_name, -- Assuming 'name' exists in 'categoryoptioncombo'
    dv.value AS reported_value,
    dv.storedby,
    dv.lastupdated
    -- We are not including 'comment', 'followup', 'created', 'deleted' from datavalue
    -- as they are not typically used for direct visualization in this context,
    -- but you can add them back if needed.
FROMcrete
    datavalue dv
JOIN
    -- Join datavalue to organisationunit using sourceid from datavalue
    organisationunit ou ON dv.sourceid = ou.organisationunitid
JOIN
    dataelement de ON dv.dataelementid = de.dataelementid
JOIN
    period p ON dv.periodid = p.periodid
LEFT JOIN -- Use LEFT JOIN as not all data values have category option combos
    categoryoptioncombo coc ON dv.categoryoptioncomboid = coc.categoryoptioncomboid
WHERE
    -- Filter for data from a specific period (e.g., the year 2023)
    p.startdate >= '2023-01-01' AND p.startdate < '2024-01-01'
    -- Filter for specific data elements by their common names
    -- You might need to adjust these names based on your specific dump's metadata
    AND de.name IN (
        'ANC 1st visit',             -- First Antenatal Care Visit
        'Malaria cases < 5 years',   -- Malaria cases in children under 5
        'Measles doses given'        -- Doses of Measles vaccine administered
    )
    -- OPTIONAL: Filter by a specific hierarchy level if you want to focus on Districts (often level 3 or 4)
    -- AND ou.hierarchylevel = 3
ORDER BY
    organisation_unit_name, de.name, p.startdate, coc.name
LIMIT 10000;