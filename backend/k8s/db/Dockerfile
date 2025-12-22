FROM postgres:16-alpine

COPY ../db/supabase_setup.sql /docker-entrypoint-initdb.d/supabase_setup.sql


COPY . .

COPY ../db ./db
WORKDIR /backend/db
CMD ["postgres"]