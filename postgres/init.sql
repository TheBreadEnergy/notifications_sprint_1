CREATE SCHEMA IF NOT EXISTS content;
CREATE TABLE IF NOT EXISTS content.files(
    id uuid primary key,
    url varchar not null,
    filename varchar not null,
    size integer not null,
    file_type varchar(100),
    short_name varchar(24) not null,
    created timestamp with time zone
);

CREATE UNIQUE INDEX files_short_name_idx on content.files(short_name);
--
-- CREATE TABLE IF NOT EXISTS content.film_work (
--     id uuid primary key,
--     title varchar(200) not null,
--     description text,
--     creation_date DATE,
--     rating float,
--     type text not null,
--     created timestamp with time zone,
--     modified timestamp with time zone
-- );
--
-- CREATE TABLE IF NOT EXISTS content.genre (
--     id uuid primary key,
--     name varchar(100) not null,
--     description text,
--     created timestamp with time zone,
--     modified timestamp with time zone
-- );
--
--
-- CREATE TABLE IF NOT EXISTS content.person (
--     id uuid primary key,
--     full_name varchar(100) not null,
--     gender text not null,
--     created timestamp with time zone,
--     modified timestamp with time zone
-- );
--
-- CREATE TABLE IF NOT EXISTS content.person_film_work (
--     id uuid primary key,
--     person_id uuid references content.person (id),
--     film_work_id uuid references content.film_work (id),
--     role text NOT NULL,
--     created timestamp with time zone
-- );
--
-- CREATE TABLE IF NOT EXISTS content.genre_film_work (
--     id uuid primary key,
--     genre_id uuid references content.genre (id),
--     film_work_id uuid references content.film_work (id),
--     created timestamp with time zone
-- );
--
-- CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
-- CREATE UNIQUE INDEX genre_film_work_idx on content.genre_film_work(genre_id, film_work_id);
-- CREATE UNIQUE INDEX person_film_work_idx on content.person_film_work(person_id, film_work_id, role);
--
