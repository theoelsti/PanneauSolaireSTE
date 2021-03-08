CREATE DATABASE IF NOT EXISTS panneau;
CREATE TABLE IF NOT EXISTS  releves (
              date DATETIME NOT NULL,
              dir SMALLINT(4) NOT NULL, 
              moy decimal(4,1) NOT NULL, 
              raf decimal(3,1) NOT NULL);
ALTER TABLE `releves` ADD PRIMARY KEY(`date`);

CREATE TABLE IF NOT EXISTS etats(
    mode  boolean, 
    current boolean);
INSERT INTO etats VALUES (false, false)