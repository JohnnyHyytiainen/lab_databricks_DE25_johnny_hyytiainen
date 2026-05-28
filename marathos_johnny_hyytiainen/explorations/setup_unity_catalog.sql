-- Skapa huvudkatalogen
CREATE CATALOG IF NOT EXISTS marathos;
USE CATALOG marathos;

-- Skapa scheman för alla 3 medallion-lager
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE VOLUME IF NOT EXISTS default.raw;

