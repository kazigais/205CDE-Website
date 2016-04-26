DROP TABLE IF EXISTS articles_table;
DROP TABLE IF EXISTS comments_table;


CREATE TABLE articles_table (
    id integer PRIMARY KEY,
    title text NOT NULL,
    content text NOT NULL,
    articleDate text not NULL
);
CREATE TABLE comments_table (
    id integer PRIMARY KEY,
    article_id integer,
    commentContent text,
    commentDate text,
    FOREIGN KEY(article_id) REFERENCES articles_table(id)
);
    