DROP TABLE IF EXISTS articles_table;


CREATE TABLE articles_table (
    id integer PRIMARY KEY,
    title text NOT NULL,
    content text NOT NULL
    );