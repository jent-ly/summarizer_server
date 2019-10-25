CREATE TABLE account (
  id SERIAL PRIMARY KEY,
  create_time TIMESTAMP NOT NULL,
  email TEXT NOT NULL,
  gaia TEXT NOT NULL
);

CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  score INTEGER NOT NULL,
  description VARCHAR(8000) NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  url TEXT NOT NULL,
  account_id INTEGER REFERENCES account(id) NOT NULL
);
