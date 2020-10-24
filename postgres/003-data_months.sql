create materialized view data_months as
	SELECT DISTINCT date(date_trunc('month'::text, data_coviddataraw.date::timestamp with time zone)) AS month
FROM data_coviddataraw
ORDER BY (date(date_trunc('month'::text, data_coviddataraw.date::timestamp with time zone)));

alter materialized view data_months owner to "DataTitans";

