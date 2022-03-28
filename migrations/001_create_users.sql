CREATE TABLE users (
    pk serial,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    username text NOT NULL,
    hashed_password text NOT NULL,
    title text NOT NULL,
    phone text NOT NULL,
    email text NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (pk),
    CONSTRAINT users_unique_username UNIQUE (username)
);


CREATE INDEX users_index_01 ON users (username, is_active);
