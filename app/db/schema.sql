DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS customer_due;
DROP TABLE IF EXISTS due_payment_info;

CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  mobile_number TEXT UNIQUE NOT NULL
);

CREATE TABLE customer_due(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    due_amount REAL NOT NULL,
    reference_id TEXT UNIQUE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer (id)
);



CREATE TABLE due_payment_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  due_id INTEGER NOT NULL,
  amount_paid REAL NOT NULL,
  paid_on_date TEXT NOT NULL,
  transaction_id TEXT UNIQUE NOT NULL,
  acknowledgement_id TEXT UNIQUE NOT NULL,
  FOREIGN KEY (due_id) REFERENCES customer_due (id)
);


insert into customer(name, mobile_number) values
('Person 1', '9234567891')
,('Person 2', '9234567892')
,('Person 3', '9234567893')
,('Person 4', '9234567894')
,('Person 5', '9234567895')
,('Person 6', '9234567896')
,('Person 7', '9234567897');


insert into customer_due(customer_id, due_date, due_amount, reference_id) values
(1, '2020-08-01', 1000, 'REF1234561')
,(2, '2020-08-03', 2000, 'REF1234562')
,(3, '2020-08-10', 345, 'REF1234563')
,(4, '2020-08-12', 899, 'REF1234564')
,(5, '2020-08-02', 170.81, 'REF1234565');
