CREATE DATABASE login_system;
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON login_system.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;
