CREATE TABLE inventory (
    art_id INT(3) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    stock INT(4) NOT NULL
);

CREATE TABLE products (
    name VARCHAR(20) NOT NULL,
    art_id INT(3) NOT NULL,
    amount_of INT(3) NOT NULL,
    FOREIGN KEY(art_id) REFERENCES inventory(art_id)
);

CREATE VIEW allproducts
    AS SELECT p.name AS ProductName, p.art_id, i.name AS ArticleName, i.stock, p.amount_of AS StockRequired
    FROM products p, inventory i
    WHERE p.art_id = i.art_id;