
CREATE TABLE chats (
	id BIGSERIAL NOT NULL, 
	title VARCHAR, 
	type VARCHAR NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id)
)




CREATE TABLE users (
	id BIGSERIAL NOT NULL, 
	username VARCHAR, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR, 
	is_admin BOOLEAN, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id), 
	UNIQUE (username)
)


