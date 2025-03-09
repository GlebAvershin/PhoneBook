CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    fio VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    note TEXT
);
