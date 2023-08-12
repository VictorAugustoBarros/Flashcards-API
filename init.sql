CREATE TABLE IF NOT EXISTS cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer VARCHAR(255) NOT NULL,
    creation_date DATETIME,
    INDEX idx_creation_date (creation_date)
);

CREATE TABLE IF NOT EXISTS subdecks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATETIME,
    deck_id INT NOT NULL,
    FOREIGN KEY (deck_id) REFERENCES decks(id),
    INDEX idx_creation_date (creation_date)
);

CREATE TABLE IF NOT EXISTS decks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATETIME,
    INDEX idx_creation_date (creation_date)
);