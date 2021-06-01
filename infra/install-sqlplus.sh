curl https://download.oracle.com/otn_software/linux/instantclient/211000/oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm --output basic-package
sudo rpm -i basic-package
curl https://download.oracle.com/otn_software/linux/instantclient/211000/oracle-instantclient-sqlplus-21.1.0.0.0-1.x86_64.rpm --output instant-client.rpm
sudo rpm -i instant-client.rpm
sqlplus 'USERNAME@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=DB_HOST)(PORT=1521))(CONNECT_DATA=(SID=YOUR-SID)))'
