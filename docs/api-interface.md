# API usada pela interface

A interface é servida pela própria aplicação FastAPI. Inicie o backend com `poetry run uvicorn product_structure.api.main:app --reload` e abra `http://127.0.0.1:8000/`. A documentação OpenAPI continua disponível em `/docs`; o estado da API pode ser consultado em `/health`.

## Rotas usadas

| Método | Rota | Payload / retorno | Estado |
|---|---|---|---|
| GET | `/itens/` | Lista itens (`id`, `nome`, `descricao`, `preco`) | Disponível; controller conectado nesta implementação |
| POST | `/itens/` | `{ "nome": "Caneta", "descricao": "...", "preco": 2.5 }` | Disponível; controller e schema adicionados nesta implementação |
| GET | `/formulas/` | Lista fórmulas (`id`, `nome`) | Existente |
| POST | `/formulas/` | `{ "nome": "Caneta" }`; o nome precisa existir no catálogo de itens e a API cria a raiz | Existente |
| GET | `/formulas/{formula_id}` | Explosão com produto, custo e componentes | Existente; a resposta agora inclui `node_id` em cada nível para ações na árvore |
| POST | `/formulas/{formula_id}/nodes` | `{ "item_id": 2, "quantidade": 1, "parent_id": 1 }` | Existente |
| DELETE | `/formulas/{formula_id}/nodes/{node_id}` | Remove o nó e seus descendentes conforme as regras do banco | Existente |
| DELETE | `/formulas/{formula_id}` | Exclui a fórmula | Existente |

## Operações ainda sem rota

O serviço de itens já contém funções para buscar por ID/nome e atualizar/remover no banco, mas a API ainda não expõe `GET /itens/{item_id}`, `PATCH /itens/{item_id}` nem `DELETE /itens/{item_id}`. A interface não oferece busca individual, edição ou exclusão de itens.

A API também não expõe uma rota de atualização de quantidade ou movimentação de componente; por isso a interface limita a edição da árvore a adicionar e remover componentes, conforme os endpoints disponíveis.
