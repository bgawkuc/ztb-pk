ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';
SELECT 'CREATE DATABASE grocery_store'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'grocery_store')