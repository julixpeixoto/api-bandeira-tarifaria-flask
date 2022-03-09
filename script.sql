CREATE DATABASE dados;

USE dados;

CREATE TABLE `dados_bandeira` (
    id VARCHAR(36) NOT NULL,
    ano VARCHAR(4) NOT NULL,
    bandeira VARCHAR(50) NOT NULL,
    mes VARCHAR(10) NOT NULL,
    numero_mes INT(2) NOT NULL,
    valor VARCHAR(10) NOT NULL,
    created_at datetime NOT NULL default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
