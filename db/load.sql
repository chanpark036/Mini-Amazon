\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);
\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Feedback FROM 'Feedback.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.feedback_id_seq',
                         (SELECT MAX(id)+1 FROM Feedback),
                         false);
                         
\COPY Inventory FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV
