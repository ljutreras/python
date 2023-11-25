SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE history_chat.bots (
  b_id int PRIMARY KEY AUTO_INCREMENT,
  empresa varchar(255) NOT NULL,
  system text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO history_chat.bots (b_id, empresa, system) VALUES
(1, 'onbot', 'Eres un agente virtual llamada MIA y tu objetivo es dar la fecha');


CREATE TABLE history_chat.chats (
  c_id int PRIMARY KEY AUTO_INCREMENT,
  uid varchar(255) NOT NULL,
  role varchar(10) NOT NULL,
  content text NOT NULL,
  date timestamp(3) NOT NULL DEFAULT current_timestamp(3) ON UPDATE current_timestamp(3),
  id_bot int(11) NOT NULL,
  FOREIGN KEY (id_bot) REFERENCES history_chat.bots (b_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
COMMIT;

