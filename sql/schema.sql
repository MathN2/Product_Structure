-- =====================================================
-- PROJETO: SISTEMA DE FÓRMULA DE PRODUTOS
-- BANCO DE DADOS: projeto_db
-- SGBD: PostgreSQL
-- =====================================================

-- 1. TABELA DE ITENS
CREATE TABLE itens (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco NUMERIC(12,2) NOT NULL DEFAULT 0
);

-- 2. TABELA DE FÓRMULAS
CREATE TABLE formula (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
);

-- 3. TABELA DE ITENS DA FÓRMULA
CREATE TABLE item_formula (
    id SERIAL PRIMARY KEY,
    formula_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    parent_id INTEGER,
    quantidade NUMERIC(12,3) NOT NULL,

    CONSTRAINT fk_formula
        FOREIGN KEY (formula_id)
        REFERENCES formula(id),


    CONSTRAINT fk_formula_item
        FOREIGN KEY (item_id)
        REFERENCES itens(id),

    CONSTRAINT uq_formula_item
        UNIQUE (formula_id, id),

    CONSTRAINT fk_formula_pai
        FOREIGN KEY (formula_id, parent_id)
        REFERENCES item_formula(formula_id, id)
        ON DELETE CASCADE,

    CONSTRAINT chk_quantidade
        CHECK (quantidade > 0)
);

-- 4. ÍNDICES PARA MELHORAR AS CONSULTAS
CREATE INDEX idx_formula
    ON item_formula(formula_id);

CREATE INDEX idx_formula_item
    ON item_formula(item_id);

CREATE INDEX idx_formula_pai
    ON item_formula(parent_id);

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================