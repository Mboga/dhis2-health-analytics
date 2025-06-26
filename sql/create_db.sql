SELECT
    pid,
    usename,
    datname,
    client_addr,
    application_name,
    backend_start,
    state,
    query
FROM
    pg_stat_activity
WHERE
    datname = 'sierra_dhis2';

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'sierra_dhis2';

drop database sierra_dhis2;
create database sierra_dhis2 encoding 'UTF8';