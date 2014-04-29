create database if not exists autoleadfinder;

use autoleadfinder;

drop table if exists lead_details;

create table lead_details(
	id int auto_increment not null primary key,
	full_name varchar(255),
	name2 varchar(255),
	name3 varchar(255),
	a1 varchar(255),
	a2 varchar(255),
	tel varchar(255),
	fax varchar(255),
	email varchar(255),
	web varchar(255)
);

drop table if exists last_crawled_state

create table last_crawled_state(
	lead_id int
);