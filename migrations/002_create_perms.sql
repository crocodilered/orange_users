CREATE TABLE perms
(
    user_pk integer NOT NULL,
    can_create_user boolean NOT NULL,
    can_update_user boolean NOT NULL,
    can_update_user_password boolean NOT NULL,
    can_update_user_perms boolean NOT NULL,
    PRIMARY KEY (user_pk)
);
