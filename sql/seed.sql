-- =====================================================
-- PROJETO: SISTEMA DE FÓRMULA DE PRODUTOS
-- BANCO DE DADOS: projeto_db
-- SGBD: PostgreSQL
-- =====================================================

-- 1. CADASTRO DO PRODUTO
INSERT INTO formula (id, nome)
VALUES
(1, 'Caneta');


-- 2. CADASTRO DOS ITENS
INSERT INTO itens
(id, nome, descricao, preco)
VALUES
(1, 'Caneta', 'Objeto esferográfico de escrita', 3.50),
(2, 'Tinta', 'Tinta da caneta', 0.80),
(3, 'Corpo', 'Corpo da caneta', 1.00),
(4, 'Tampa', 'Tampa da caneta', 0.70),
(5, 'Pigmento', 'Pigmento da tinta', 0.45),
(6, 'Solvente', 'Solvente da tinta', 0.50),
(7, 'Plastico', 'Plástico do corpo', 0.70),
(8, 'Clip', 'Clip da caneta', 0.30),
(9, 'Plastico Tampa', 'Plástico da tampa', 0.50),
(10, 'Vedacao', 'Vedação da tampa', 0.20);


-- 3. ESTRUTURA DA FÓRMULA DO PRODUTO
INSERT INTO item_formula
(id, formula_id, item_id, parent_id, quantidade)
VALUES
-- Item final da formula
(1, 1, 1, NULL, 1.000),

-- Itens principais da caneta
(2, 1, 1, 1, 1.000),
(3, 1, 2, 1, 1.000),
(4, 1, 3, 1, 1.000),

-- Subitens da tinta
(5, 1, 4, 1, 1.000),
(6, 1, 5, 1, 1.000),

-- Subitens do corpo
(7, 1, 6, 2, 1.000),
(8, 1, 7, 2, 1.000),

-- Subitens da tampa
(9, 1, 8, 3, 1.000),
(10, 1, 9, 3, 1.000);

-- =====================================================
-- 8. ATUALIZAÇÃO DAS SEQUÊNCIAS AUTOMÁTICAS
-- =====================================================

SELECT setval('formula_id_seq',
    (SELECT MAX(id) FROM formula));

SELECT setval('itens_id_seq',
    (SELECT MAX(id) FROM itens));

SELECT setval('item_formula_id_seq',
    (SELECT MAX(id) FROM item_formula));

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================