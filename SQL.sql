
CREATE DATABASE IF NOT EXISTS petshop;

USE petshop;

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
VALUES ('Admin User', 'edi@petshop.com', '32768:8:1$H1cXbHeiZiEBPWjX$d172456b1591741bff9fb706e40851486cba37b7f3168a8beaf0fb6ac9a8eb2804775270aadce80b8feecdb40e3bd267db401085b0fd2f835bbe04451cf06845', 'admin', '11901239874')

DELETE FROM usuarios WHERE id = 7;

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

-- Quando o cliente realizar a compra, você pode registrar uma venda, incluindo as informações necessárias como a quantidade e o valor total. 
INSERT INTO vendas (usuario_id, produto_id, quantidade, valor_total, forma_pagamento)
VALUES (1, 1, 2, 61.80, 'PIX');  -- O usuário de ID 1 comprou 2 unidades do produto de ID 1 (Ração Golden)

-- Para visualizar as vendas realizadas, você pode fazer uma consulta simples
SELECT v.id, u.nome AS usuario, p.nome AS produto, v.quantidade, v.valor_total, v.forma_pagamento, v.data_venda
FROM vendas v
JOIN usuarios u ON v.usuario_id = u.id
JOIN produtos p ON v.produto_id = p.id;

