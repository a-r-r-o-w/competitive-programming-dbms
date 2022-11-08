-- create new user

create user 'competitive-programming-dbms-admin'@'localhost' identified by '5up3r-s3cur3-p4ssw0rd';

-- grant all permissions to new user

grant all on *.* to 'competitive-programming-dbms-admin'@'localhost';
