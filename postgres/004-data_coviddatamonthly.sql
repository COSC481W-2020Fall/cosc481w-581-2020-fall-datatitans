create materialized view data_coviddatamonthly as
	SELECT DISTINCT data_coviddataclean.iso_code,
                data_coviddataclean.continent,
                data_coviddataclean.location,
                date(date_trunc('month'::text, data_coviddataclean.date::timestamp with time zone))      AS month,
                sum(data_coviddataclean.new_cases) OVER (PARTITION BY data_coviddataclean.iso_code, (date(
                        date_trunc('month'::text, data_coviddataclean.date::timestamp with time zone)))) AS new_cases,
                sum(data_coviddataclean.new_deaths) OVER (PARTITION BY data_coviddataclean.iso_code, (date(
                        date_trunc('month'::text, data_coviddataclean.date::timestamp with time zone)))) AS new_deaths,
                sum(data_coviddataclean.new_tests) OVER (PARTITION BY data_coviddataclean.iso_code, (date(
                        date_trunc('month'::text, data_coviddataclean.date::timestamp with time zone)))) AS new_tests
FROM data_coviddataclean
ORDER BY data_coviddataclean.iso_code,
         (date(date_trunc('month'::text, data_coviddataclean.date::timestamp with time zone)));

alter materialized view data_coviddatamonthly owner to "DataTitans";

