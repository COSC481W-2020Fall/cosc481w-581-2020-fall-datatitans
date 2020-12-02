create materialized view data_country as
	SELECT DISTINCT ON (data_coviddataclean.iso_code) data_coviddataclean.iso_code AS country_code,
                                                  data_coviddataclean.location AS name,
                                                  data_coviddataclean.continent,
                                                  data_coviddataclean.population
FROM data_coviddataclean
ORDER BY data_coviddataclean.iso_code;

alter materialized view data_country owner to "DataTitans";
