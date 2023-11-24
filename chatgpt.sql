CREATE TABLE bots (
    b_id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(255),
    system_role TEXT
);


CREATE TABLE users (
    u_id INT AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(255),
    role VARCHAR(255),
    content TEXT,
    date TIMESTAMP,
    b_id INT,
    CONSTRAINT FK_b_id FOREIGN KEY (b_id) REFERENCES bots(b_id)
);


-- Crear la tabla 'bot'
CREATE TABLE bot (
    id INT PRIMARY KEY AUTO_INCREMENT,
    empresa VARCHAR(255) NOT NULL,
    system VARCHAR(255) NOT NULL
);

-- Crear la tabla 'chats'
CREATE TABLE chats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uid INT NOT NULL,
    role VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_bot INT NOT NULL,
    FOREIGN KEY (id_bot) REFERENCES bot(id)
);