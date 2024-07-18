---- Luis Gerardo Baeza
---- Sample transaction table
---- SQL Server


-- #### Create table
CREATE TABLE transactions (
  tx_id int,
  tx_date DATE,
  amount float
);

DECLARE @i int = 0

WHILE @i < 2000
BEGIN
    SET @i = @i + 1
    insert into transactions  
      select RAND()*(99999-1000)+1000  as tx_id, concat('2024/', FLOOR(RAND()*(12-1)+1),'/', FLOOR(RAND()*(28-1)+1)) as tx_date, RAND()*(9999-100)+100 as amount 
      UNION ALL
      select RAND()*(99999-1000)+1000  as tx_id, concat('2024/', FLOOR(RAND()*(12-1)+1),'/', FLOOR(RAND()*(28-1)+1)) as tx_date, RAND()*(9999-100)+100 as amount 
      UNION ALL
      select RAND()*(99999-1000)+1000  as tx_id, concat('2024/', FLOOR(RAND()*(12-1)+1),'/', FLOOR(RAND()*(28-1)+1)) as tx_date, RAND()*(9999-100)+100 as amount 
      UNION ALL
      select RAND()*(99999-1000)+1000  as tx_id, concat('2024/', FLOOR(RAND()*(12-1)+1),'/', FLOOR(RAND()*(28-1)+1)) as tx_date, RAND()*(9999-100)+100 as amount 
      UNION ALL
      select RAND()*(99999-1000)+1000  as tx_id, concat('2024/', FLOOR(RAND()*(12-1)+1),'/', FLOOR(RAND()*(28-1)+1)) as tx_date, RAND()*(9999-100)+100 as amount 

END;

select * from erp.dbo.transactions;


-- ### Create BQ Table
CREATE TABLE erp_sqlserver.transactions (
  tx_id INT64,
  tx_date DATE,
  amount FLOAT64
);


-- #### Create user
CREATE LOGIN dataflow WITH PASSWORD = 'D4t4fl0w!'; 
CREATE USER dataflow_user for login dataflow;
GRANT ALL ON database::erp TO dataflow_user;
GRANT ALL ON erp.dbo.transactions TO dataflow_user;

-- #### Test user
EXECUTE AS USER = 'dataflow_user';
select * from erp.dbo.transactions

-- #### Check running queries
SELECT  t.text, p.* 
from sys.dm_exec_requests p
outer apply sys.dm_exec_sql_text(p.sql_handle) t
order by start_time desc

