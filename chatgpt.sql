CREATE TABLE users (
    u_id INT AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(255),
    role VARCHAR(255),
    content TEXT,
    date TIMESTAMP
);

CREATE TABLE assistant (
    a_id INT AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(255),
    role VARCHAR(255),
    content TEXT,
    date TIMESTAMP,
    u_id INT,
    CONSTRAINT FK_u_id FOREIGN KEY (u_id) REFERENCES users(u_id)
);

