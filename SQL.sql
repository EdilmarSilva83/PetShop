CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'cliente', 'petshop') NOT NULL,
    contato VARCHAR(15) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email, senha, tipo, contato) VALUES 
('Admin User', 'admin@petshop.com', '<senha_hash_admin>', 'admin'),
('Cliente User', 'cliente@petshop.com', '<senha_hash_cliente>', 'cliente'),
('Petshop User', 'petshop@petshop.com', '<senha_hash_petshop>', 'petshop');

USE petshop;
SELECT * FROM usuarios;

CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    pet_nome VARCHAR(100) NOT NULL,
    data_hora_agendamento DATETIME NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

SELECT * FROM agendamentos;

INSERT INTO usuarios (nome, email, senha, tipo, contato)
VALUES ('Admin User', 'ediadmin@petshop.com', 'scrypt:32768:8:1$NIbRDjqUMCb7vx2k$48e56ad0946fa8763bd24d8d471aee77437cdbb4a5c5a47fffa2fc75652cbec609ab772c7564724cd62220ad725ff57d9d5714366f08dc6e923f6921af5c0ebd', 'admin', '11911221122');

DELETE FROM usuarios WHERE id = 11;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    imagem VARCHAR(255) NOT NULL
);

INSERT INTO produtos (nome, descricao, preco, imagem) VALUES
('Ração Golden para Gatos', 'Ração para gatos adultos castrados, sabor salmão.', 30.90, '/static/Golden.jpg'),
('Areia Higiênica Pipicat', 'Areia higiênica para gatos, fácil de limpar.', 45.90, '/static/Areia.jpg'),
('Arranhador TV Tubo', 'Arranhador tubo de papelão para gatos, confortável e resistente.', 169.99, '/static/ArranhadorTV.jpg');

SELECT * FROM produtos;

CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    forma_pagamento ENUM('PIX', 'Cartão de Crédito') NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)  -- Aqui você precisa ter a tabela de produtos criada
);

SELECT * FROM vendas;

CREATE TABLE mensagens_contato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mensagem TEXT NOT NULL,
    data_enviado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM mensagens_contato;

CREATE TABLE pontos_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    pontos INT DEFAULT 0,
    ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

SELECT * FROM pontos_usuario;