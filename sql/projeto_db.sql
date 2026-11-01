-- =====================================================
-- PROJETO: SISTEMA DE FÓRMULA DE PRODUTOS
-- BANCO DE DADOS: projeto_db
-- SGBD: PostgreSQL
-- =====================================================

-- 1. TABELA DE PRODUTOS
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    data_cadastro DATE DEFAULT CURRENT_DATE
);

-- 2. TABELA DE COMPONENTES
CREATE TABLE componentes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    valor_aquisicao NUMERIC(12,2) NOT NULL DEFAULT 0,
    data_cadastro DATE DEFAULT CURRENT_DATE
);

-- 3. TABELA DE FÓRMULAS
CREATE TABLE formula (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER NOT NULL,
    componente_id INTEGER NOT NULL,
    componente_pai_id INTEGER,
    quantidade NUMERIC(12,3) NOT NULL,

    CONSTRAINT fk_formula_produto
        FOREIGN KEY (produto_id)
        REFERENCES produtos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_formula_componente
        FOREIGN KEY (componente_id)
        REFERENCES componentes(id),

    CONSTRAINT fk_formula_pai
        FOREIGN KEY (componente_pai_id)
        REFERENCES formula(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_quantidade
        CHECK (quantidade > 0)
);

-- 4. ÍNDICES PARA MELHORAR AS CONSULTAS
CREATE INDEX idx_formula_produto
    ON formula(produto_id);

CREATE INDEX idx_formula_componente
    ON formula(componente_id);

CREATE INDEX idx_formula_pai
    ON formula(componente_pai_id);

-- =====================================================
-- 5. CADASTRO DO PRODUTO
-- =====================================================

INSERT INTO produtos (id, nome, descricao)
VALUES
(1, 'Caneta', 'Caneta esferográfica');

-- =====================================================
-- 6. CADASTRO DOS COMPONENTES
-- =====================================================

INSERT INTO componentes
(id, nome, descricao, valor_aquisicao)
VALUES
(1, 'Tinta', 'Tinta da caneta', 0.80),
(2, 'Corpo', 'Corpo da caneta', 1.00),
(3, 'Tampa', 'Tampa da caneta', 0.70),
(4, 'Pigmento', 'Pigmento da tinta', 0.45),
(5, 'Solvente', 'Solvente da tinta', 0.50),
(6, 'Plastico', 'Plástico do corpo', 0.70),
(7, 'Clip', 'Clip da caneta', 0.30),
(8, 'Plastico Tampa', 'Plástico da tampa', 0.50),
(9, 'Vedacao', 'Vedação da tampa', 0.20);

-- =====================================================
-- 7. ESTRUTURA DA FÓRMULA DO PRODUTO
-- =====================================================

INSERT INTO formula
(id, produto_id, componente_id, componente_pai_id, quantidade)
VALUES
-- Componentes principais da caneta
(1, 1, 1, NULL, 1.000),
(2, 1, 2, NULL, 1.000),
(3, 1, 3, NULL, 1.000),

-- Subcomponentes da tinta
(4, 1, 4, 1, 1.000),
(5, 1, 5, 1, 1.000),

-- Subcomponentes do corpo
(6, 1, 6, 2, 1.000),
(7, 1, 7, 2, 1.000),

-- Subcomponentes da tampa
(8, 1, 8, 3, 1.000),
(9, 1, 9, 3, 1.000);

-- =====================================================
-- 8. ATUALIZAÇÃO DAS SEQUÊNCIAS AUTOMÁTICAS
-- =====================================================

SELECT setval('produtos_id_seq',
    (SELECT MAX(id) FROM produtos));

SELECT setval('componentes_id_seq',
    (SELECT MAX(id) FROM componentes));

SELECT setval('formula_id_seq',
    (SELECT MAX(id) FROM formula));

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================