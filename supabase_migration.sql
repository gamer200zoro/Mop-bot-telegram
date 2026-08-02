CREATE TABLE chats (
	id BIGINT NOT NULL, 
	title VARCHAR, 
	type VARCHAR NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
)
CREATE TABLE users (
	id BIGINT NOT NULL, 
	username VARCHAR, 
	first_name VARCHAR NOT NULL, 	last_name VARCHAR, 
	is_admin BOOLEAN, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username)
)
