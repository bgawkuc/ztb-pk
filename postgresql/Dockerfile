FROM postgres:15.3-alpine
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB grocery_store
COPY db_init.sql /docker-entrypoint-initdb.d/
EXPOSE 5432