CREATE DATABASE storage;
-- CREATE USER docker WITH PASSWORD 'docker';
-- GRANT ALL PRIVILEGES ON DATABASE storage TO docker;

\c storage;

CREATE TABLE space (
    id SERIAL NOT NULL,
    name VARCHAR(32) NOT NULL,
    is_refrigerated BOOLEAN NOT NULL,
    max_capacity INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE TABLE item_type (
    id SERIAL NOT NULL,
    name VARCHAR(32) NOT NULL,
    is_kept_cold BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
);


CREATE TABLE item (
    id SERIAL NOT NULL,
    name VARCHAR(32) NOT NULL,
    expiration_date DATE NOT NULL,
    item_type_id INTEGER NOT NULL,
    space_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(item_type_id) REFERENCES item_type (id),
    FOREIGN KEY(space_id) REFERENCES space (id)
);


INSERT INTO space (id, name, is_refrigerated, max_capacity)
VALUES
       (1, 'Refrigerator small', true, 10),
       (2, 'Refrigerator big', true, 30),
       (3, 'Pantry', false, 50),
       (4, 'Shelves', false, 15);


INSERT INTO item_type (id, name, is_kept_cold)
VALUES
       (1, 'Ice-cream', true),
       (2, 'Cookies', false),
       (3, 'Milk', true),
       (4, 'Bread', false);


INSERT INTO item (name, expiration_date, item_type_id, space_id)
VALUES
       ('Ben & Jerry’s', '2022-12-31', 1, 1),
       ('Ben & Jerry’s', '2022-11-20', 1, 1),
       ('Ben & Jerry’s', '2022-11-26', 1, 1),
       ('Oreo', '2023-01-26', 2, 4),
       ('Oreo', '2023-02-26', 2, 4),
       ('Slavushkin product', '2022-07-26', 3, 2),
       ('Slavushkin product', '2022-07-26', 3, 2),
       ('Slavushkin product', '2022-07-26', 3, 2),
       ('Slavushkin product', '2022-07-26', 3, 2),
       ('Harry’s', '2022-08-26', 4, 3),
       ('Harry’s', '2022-08-26', 4, 2),
       ('Harry’s', '2022-08-26', 4, 3),
       ('Harry’s', '2022-08-26', 4, 2);
