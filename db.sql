--
-- Create User, Database 
--
CREATE USER aiopg_user WITH PASSWORD 'aiopg_password';
CREATE DATABASE aiopg_db;
GRANT ALL PRIVILEGES ON DATABASE aiopg_db TO aiopg_user;
--
-- Create table Feed
--
\c aiopg_db;
SET ROLE 'aiopg_user';
DROP TABLE IF EXISTS feed;
CREATE TABLE feed (
  id serial PRIMARY KEY,
  title varchar(300),
  link varchar(300),
  pub_date timestamp with time zone);
