DROP TABLE IF EXISTS articles_table;


CREATE TABLE articles_table (
    id integer PRIMARY KEY,
    title text NOT NULL,
    content text NOT NULL,
    articleDate text not NULL
);
CREATE TABLE comments_table (
    id integer PRIMARY KEY,
    article_id integer FOREIGN KEY,
    content text NOT NULL,
    commentDate text not NULL
);
    