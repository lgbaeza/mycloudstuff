

-- 100 city
-- 2048 customer
-- 10 category
-- 128 products
-- 1,572,864 orders

create table customers (id serial primary key, customername varchar (50) default concat('name '), city varchar(50) default concat('city ',cast(random()*100 as int)));
create table products (id serial primary key, productname varchar (50) default concat('product '), category varchar(50) default concat('category ',cast(random()*10 as int)));
create table orders (id serial primary key, productid int default random()*100, customerid int default random()*1000, dateorder date);

insert into customers(customername) values ('name ');
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;
insert into customers(customername) select customername from customers;

insert into products(productname) values ('product ');
insert into products(productname) select productname from products;
insert into products(productname) select productname from products;
insert into products(productname) select productname from products;
insert into products(productname) select productname from products;
insert into products(productname) select productname from products;
insert into products(productname) select productname from products;
insert into products(productname) select productname from products;

insert into orders(dateorder) values ('2020/01/01');
insert into orders(dateorder) values ('2020/02/01');
insert into orders(dateorder) values ('2020/03/01');
insert into orders(dateorder) values ('2020/04/01');
insert into orders(dateorder) values ('2020/05/01');
insert into orders(dateorder) values ('2020/06/01');
insert into orders(dateorder) values ('2020/07/01');
insert into orders(dateorder) values ('2020/08/01');
insert into orders(dateorder) values ('2020/09/01');
insert into orders(dateorder) values ('2020/10/01');
insert into orders(dateorder) values ('2020/11/01');
insert into orders(dateorder) values ('2020/12/01');
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;
insert into orders(dateorder) select dateorder from orders;

-- user setup
CREATE GROUP ro_group;
CREATE USER readonly WITH password 'readonly!!';
ALTER GROUP ro_group ADD USER readonly;
GRANT USAGE ON SCHEMA "public" TO GROUP ro_group;
GRANT SELECT ON ALL TABLES IN SCHEMA "public" TO GROUP ro_group;


-- Athena
CREATE OR REPLACE VIEW sales_history AS 
SELECT
  orders.id
, orders.customerid
, orders.dateorder
, customers.customername
, customers.city
, orders.productid
, products.productname
, products.category
FROM
  ((datalakedb.sales__aurorapgsql_public_orders orders
INNER JOIN datalakedb.sales__aurorapgsql_public_customers customers ON (orders.customerid = customers.id))
INNER JOIN datalakedb.sales__aurorapgsql_public_products products ON (orders.productid = products.id))


