create materialized view data_coviddataclean as
	SELECT dc.iso_code,
       dc.continent,
       dc.location,
       dc.date,
       dc.total_cases,
       dc.new_cases,
       dc.new_cases_smoothed,
       dc.total_deaths,
       dc.new_deaths,
       dc.new_deaths_smoothed,
       dc.total_cases / dc.population * 1000000::numeric         AS total_cases_per_million,
       dc.new_cases / dc.population * 1000000::numeric           AS new_cases_per_million,
       dc.new_cases_smoothed / dc.population * 1000000::numeric  AS new_cases_smoothed_per_million,
       dc.total_deaths / dc.population * 1000000::numeric        AS total_deaths_per_million,
       dc.new_deaths / dc.population * 1000000::numeric          AS new_deaths_per_million,
       dc.new_deaths_smoothed / dc.population * 1000000::numeric AS new_deaths_smoothed_per_million,
       dc.new_tests,
       dc.total_tests,
       dc.total_tests / dc.population * 1000::numeric            AS total_tests_per_thousand,
       dc.new_tests / dc.population * 1000::numeric              AS new_tests_per_thousand,
       dc.population
FROM (SELECT data_coviddataraw.iso_code,
             data_coviddataraw.continent,
             data_coviddataraw.location,
             data_coviddataraw.date,
             sum(data_coviddataraw.new_cases)
             OVER (PARTITION BY data_coviddataraw.iso_code ORDER BY data_coviddataraw.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_cases,
             data_coviddataraw.new_cases,
             avg(data_coviddataraw.new_cases)
             OVER (PARTITION BY data_coviddataraw.iso_code ORDER BY data_coviddataraw.date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)         AS new_cases_smoothed,
             sum(data_coviddataraw.new_deaths)
             OVER (PARTITION BY data_coviddataraw.iso_code ORDER BY data_coviddataraw.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_deaths,
             data_coviddataraw.new_deaths,
             avg(data_coviddataraw.new_deaths)
             OVER (PARTITION BY data_coviddataraw.iso_code ORDER BY data_coviddataraw.date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)         AS new_deaths_smoothed,
             data_coviddataraw.new_tests,
             sum(data_coviddataraw.new_tests)
             OVER (PARTITION BY data_coviddataraw.iso_code ORDER BY data_coviddataraw.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_tests,
             avg(data_coviddataraw.new_tests)
             OVER (PARTITION BY data_coviddataraw.iso_code ORDER BY data_coviddataraw.date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)         AS new_tests_smoothed,
             data_coviddataraw.tests_units,
             data_coviddataraw.stringency_index,
             data_coviddataraw.population
      FROM data_coviddataraw
      ORDER BY data_coviddataraw.iso_code, data_coviddataraw.date) dc
WHERE dc.iso_code IS NOT NULL
  AND dc.continent IS NOT NULL
ORDER BY dc.iso_code, dc.date;

alter materialized view data_coviddataclean owner to "DataTitans";

