-- name: list
SELECT
    pk,
    created,
    updated,
    username,
    hashed_password,
    title,
    phone,
    email,
    is_active
FROM users
WHERE 1=1
ORDER BY username, pk
OFFSET :offset LIMIT :limit;


-- name: retrieve^
SELECT
    pk,
    created,
    updated,
    username,
    hashed_password,
    title,
    phone,
    email,
    is_active
FROM users
WHERE
    pk=:pk;


-- name: retrieve_active_by_username^
SELECT
    pk,
    created,
    updated,
    username,
    hashed_password,
    title,
    phone,
    email,
    is_active
FROM users
WHERE
    username=:username AND
    is_active=TRUE;


-- name: create<!
INSERT INTO users (
    created,
    updated,
    username,
    hashed_password,
    title,
    phone,
    email,
    is_active
) VALUES (
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    :username,
    :hashed_password,
    :title,
    :phone,
    :email,
    :is_active
) RETURNING
    pk,
    created,
    updated,
    username,
    hashed_password,
    title,
    phone,
    email,
    is_active;


-- name: update<!
UPDATE users SET
    updated=CURRENT_TIMESTAMP,
    username=:username,
    hashed_password=:hashed_password,
    title=:title,
    phone=:phone,
    email=:email,
    is_active=:is_active
WHERE
    pk=:pk
RETURNING
    pk,
    created,
    updated,
    username,
    hashed_password,
    title,
    phone,
    email,
    is_active;
