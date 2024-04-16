CREATE TABLE "category" (
	"name"	TEXT NOT NULL
);

CREATE TABLE "category_profit" (
	"name"	TEXT NOT NULL
);

CREATE TABLE "main_table" (
	"id"	INTEGER,
	"shop"	TEXT,
	"category"	TEXT,
	"payment_date"	DATETIME,
	"sum_val"	MONEY,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "profit_table" (
	"id"	INTEGER,
	"category"	TEXT,
	"payment_date"	DATETIME,
	"sum_val"	MONEY,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "shops" (
	"name"	TEXT NOT NULL
);

CREATE VIEW main_table_view AS SELECT *,
	   strftime('%m', payment_date) AS month,
	   strftime('%Y', payment_date) AS year,
	   strftime('%Y.%m', payment_date) AS month_year
FROM main_table
ORDER BY year, month;

CREATE VIEW prognosis_view AS
SELECT category, sum(sum_val)
FROM main_table_view
WHERE month_year >= (SELECT min(month_year) FROM (
	SELECT *
	FROM main_table_view 
	GROUP BY month_year 
	ORDER BY month_year DESC LIMIT 7))
GROUP BY category
ORDER BY sum(sum_val) DESC;