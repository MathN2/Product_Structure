# API usada pela interface

A interface é servida pela própria aplicação FastAPI. Inicie o backend com `poetry run uvicorn product_structure.api.main:app --reload` e abra `http://127.0.0.1:8000/`. A documentação OpenAPI fica em `/docs`; o estado da API pode ser consultado em `/health`.

## Rotas de itens

| Método | Rota | Uso |
|---|---|---|
| GET | `/itens/` | Lista o catálogo |
| GET | `/itens/{item_id}` | Consulta um item |
| POST | `/itens/` | Cadastra `{ "nome": "Caneta", "descricao": "...", "preco": 2.5 }` |
| PATCH | `/itens/{item_id}` | Atualiza nome, descrição e preço; a interface usa para editar preço |
| DELETE | `/itens/{item_id}` | Remove item que não esteja associado a uma fórmula |

## Rotas de fórmulas

| Método | Rota | Uso |
|---|---|---|
| GET | `/formulas/` | Lista fórmulas (`id`, `nome`) |
| POST | `/formulas/` | Cria fórmula com `{ "nome": "Caneta" }`; o nome precisa corresponder a um item existente, usado como raiz |
| GET | `/formulas/{formula_id}?quantidade_producao=3` | Explode a fórmula para a quantidade solicitada, escala quantidades em todos os níveis e retorna o custo de aquisição |
| POST | `/formulas/{formula_id}/nodes` | Adiciona componente com `{ "item_id": 2, "quantidade": 1, "parent_id": 1 }` |
| PATCH | `/formulas/{formula_id}/nodes/{node_id}` | Atualiza a quantidade do componente |
| DELETE | `/formulas/{formula_id}/nodes/{node_id}` | Remove o nó e seus descendentes |
| PATCH | `/formulas/{formula_id}` | Atualiza nome da fórmula |
| DELETE | `/formulas/{formula_id}` | Exclui a fórmula |

O custo de aquisição multiplica o preço atual de cada componente pela quantidade necessária em toda a hierarquia. A raiz do produto final não entra na soma. O banco continua sendo a fonte dos preços, então a explosão reflete atualizações feitas no catálogo.
