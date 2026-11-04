# Product Structure

Sistema para representação e gerenciamento de fórmulas de produtos por meio de uma estrutura de árvore genérica, desenvolvido em Python para a disciplina de Estruturas de Dados II.

## Sobre o projeto

O projeto tem como objetivo representar a composição hierárquica de produtos, permitindo organizar seus componentes e realizar operações sobre as fórmulas cadastradas.

A estrutura de árvore permite representar produtos compostos por outros itens, que também podem possuir seus próprios componentes.

### Funcionalidades

O projeto prevê as seguintes funcionalidades:

- **Gerenciamento de produtos e componentes:** cadastro, consulta, atualização e remoção de registros.
- **Representação hierárquica:** organização dos componentes por meio de uma árvore.
- **Explosão de fórmula:** detalhamento da composição de um produto e de seus componentes.
- **Cálculo de quantidades:** determinação das quantidades necessárias de componentes para produzir uma quantidade especificada de um produto.
- **Cálculo de custos:** obtenção dos custos relacionados aos componentes e à produção.
- **Implosão de fórmula:** análise dos componentes e dos custos associados à remontagem de um produto.

> Algumas funcionalidades podem estar em desenvolvimento. A disponibilidade de cada operação depende do estado atual da implementação.

## Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Poetry:** gerenciamento de dependências e do ambiente do projeto.
- **pytest:** execução de testes automatizados.

Outras tecnologias poderão ser adicionadas conforme o desenvolvimento do projeto.

## Requisitos

Para trabalhar com o projeto, é necessário ter:

- [Python](https://www.python.org/downloads/) em uma versão compatível com a configuração do projeto.
- [pipx](https://pipx.pypa.io/stable/installation/) para instalação isolada de ferramentas Python, caso seja utilizado para instalar o Poetry.
- [Poetry](https://python-poetry.org/docs/#installation/) para instalar e gerenciar as dependências do projeto.
- [Git](https://git-scm.com/downloads) para clonar o repositório.

Consulte as páginas oficiais para obter as instruções de instalação adequadas ao seu sistema operacional.

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/MathN2/Product_Structure.git
```

Entre no diretório do projeto:

```bash
cd Product_Structure
```

### 2. Instale as dependências

Na raiz do projeto, execute:

```bash
poetry install
```

O Poetry utilizará as configurações do projeto para instalar as dependências necessárias.

3. Configure as variáveis de ambiente

O projeto utiliza um arquivo ".env" para armazenar configurações da aplicação e credenciais de acesso ao banco de dados.

Na raiz do projeto, copie o arquivo de exemplo:

Linux:

```bash
cp .env.example .env
```

Windows:

```cmd
copy .env.example .env
```

Abra o arquivo ".env" e configure as variáveis de acordo com seu ambiente:

```bash
APP_NAME="Product Structure"
APP_ENV=development
APP_PORT=8000
APP_URL=http://localhost
APP_SECRET_KEY=replace_with_your_own_secret_key

DATABASE_URL=postgresql://seu_user:sua_senha@localhost:5432/product_structure
```

Altere principalmente:

- "APP_SECRET_KEY": substitua pelo valor de uma chave secreta própria.
- "DATABASE_URL": informe o usuário, a senha, o endereço, a porta e o nome do banco PostgreSQL.

O formato da conexão é:

`postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO`

Importante: o arquivo ".env" contém informações sensíveis e não deve ser enviado ao repositório. Utilize o ".env.example" como modelo para outros ambientes.

## Executando o projeto

Com o banco PostgreSQL configurado em `DATABASE_URL`, inicie a API e a interface com:

```bash
poetry run task run_uvicorn
```

Abra `http://127.0.0.1:8000/` para usar a interface. A documentação interativa da API fica em `http://127.0.0.1:8000/docs`; `http://127.0.0.1:8000/health` verifica a API.

Os endpoints consumidos e as operações ainda não expostas estão registrados em [`docs/api-interface.md`](docs/api-interface.md).

## Executando os testes

O projeto utiliza `pytest` para executar os testes automatizados.

Para executar os testes com o ambiente gerenciado pelo Poetry:

```bash
poetry run task test
```

Os testes devem verificar o comportamento das estruturas de dados e das operações implementadas, incluindo casos válidos e situações de erro.

## Estrutura do projeto

A organização dos diretórios poderá evoluir durante o desenvolvimento. A estrutura planejada contempla a separação entre a implementação das estruturas de dados, os serviços responsáveis pelas operações do sistema e os testes automatizados.

Consulte os diretórios do repositório para verificar a organização atual do código.

## Documentação

A documentação técnica detalhará a estrutura da árvore, os nós, o armazenamento dos dados, a reconstrução das estruturas a partir do banco de dados e os contratos dos métodos.

O documento será disponibilizado no diretório `docs/` conforme seu desenvolvimento.

## Contexto acadêmico

Projeto desenvolvido em grupo para a disciplina de Estruturas de Dados II, com foco na aplicação de estruturas de dados hierárquicas a um problema de representação e gerenciamento de fórmulas de produtos.