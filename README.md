# Plataforma de Comunidade Online - API RESTful

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Integrated-003B57?style=for-the-badge&logo=sqlite)
![Auth0](https://img.shields.io/badge/Auth0-Security-EB5424?style=for-the-badge&logo=auth0)

> **Relatório de Desenvolvimento**: Backend robusto para gestão de comunidades online, com autenticação segura, moderação de conteúdo e engajamento.

---

## Sobre o Projeto

Este projeto consiste na implementação de uma **API RESTful** utilizando **FastAPI**, focada em boas práticas de desenvolvimento backend. O sistema gerencia uma plataforma de comunidade onde usuários podem criar postagens, comentar, curtir e interagir, tudo sob um sistema seguro de autenticação e autorização via **Auth0**.

O objetivo principal foi integrar persistência de dados (SQLAlchemy + SQLite), validação de dados (Pydantic) e segurança via tokens JWT.

---

## Funcionalidades Implementadas

### Segurança e Autenticação
- [x] **Integração com Auth0**: Validação robusta de tokens JWT (Bearer Token).
- [x] **Extração de Usuário**: Identificação automática do autor (`sub`) através do token.
- [x] **Proteção de Rotas**: Endpoints sensíveis acessíveis apenas a usuários autenticados.

### Gestão de Conteúdo (Postagens)
- [x] **CRUD Completo**: Criação, Leitura, Atualização e Exclusão.
- [x] **Permissões de Edição**: Usuários só editam/excluem seus próprios conteúdos.
- [x] **Paginação**: Controle de fluxo de dados via `limit` e `offset`.
- [x] **Busca Textual**: Filtro por palavras-chave em títulos e conteúdos.
- [x] **Filtragem Avançada**: Por Categoria, Autor ou Tags.

### Engajamento (Comentários e Likes)
- [x] **Comentários**: Vinculados aos posts e autores.
- [x] **Sistema de Likes**: Regra de negócio "Like Único" (um usuário não pode curtir o mesmo post duas vezes).
- [x] **Contagem Automática**: Total de likes retornados na listagem.

### Organização (Categorias e Tags)
- [x] **Categorias**: Gestão administrativa (Criar, Editar, Excluir).
- [x] **Tags Dinâmicas**: Criação automática de tags ao salvar postagens.

---

## Tecnologias Utilizadas

* **Linguagem**: Python 3.12+
* **Framework Web**: FastAPI
* **Servidor ASGI**: Uvicorn
* **ORM (Banco de Dados)**: SQLAlchemy
* **Banco de Dados**: SQLite (Arquivo local)
* **Validação de Dados**: Pydantic v2
* **Segurança/Auth**: Python-Jose (JWT) & Auth0
* **Gerenciamento de Dependências**: Pip / Venv

---

## Estrutura do Projeto

A arquitetura segue o padrão de separação de responsabilidades para facilitar a manutenção e escalabilidade.

```text
comunidade-api/
├── app/
│   ├── core/           # Configurações globais e Segurança (Auth0)
│   ├── db/             # Conexão com Banco de Dados (Session/Engine)
│   ├── models/         # Modelos do ORM (Tabelas do Banco)
│   ├── routers/        # Endpoints (Rotas da API)
│   ├── schemas/        # Schemas Pydantic (Entrada/Saída de dados)
│   └── main.py         # Ponto de entrada da aplicação
├── .env                # Variáveis de ambiente (Segredos)
├── .gitignore          # Arquivos ignorados pelo Git
├── requirements.txt    # Lista de dependências
└── comunidade.db       # Banco de dados SQLite

```

---

## Como Rodar o Projeto

### Pré-requisitos

* Python 3.10 ou superior
* Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone [https://github.com/SEU_USUARIO/api-comunidade-fastapi.git](https://github.com/SEU_USUARIO/api-comunidade-fastapi.git)
cd api-comunidade-fastapi

```


2. **Crie e ative o ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/Mac
# venv\Scripts\activate   # No Windows

```


3. **Instale as dependências**
```bash
pip install -r requirements.txt

```


4. **Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto e preencha com suas credenciais do Auth0:
```env
PROJECT_NAME="Plataforma Comunidade API"
AUTH0_DOMAIN=seu-dominio.us.auth0.com
AUTH0_API_AUDIENCE=[https://comunidade-api.com](https://comunidade-api.com)
AUTH0_ALGORITHM=RS256
AUTH0_ISSUER=[https://seu-dominio.us.auth0.com/](https://seu-dominio.us.auth0.com/)
SQLALCHEMY_DATABASE_URI="sqlite:///./comunidade.db"

```


5. **Execute o Servidor**
```bash
uvicorn app.main:app --reload

```


6. **Acesse a Documentação**
Abra seu navegador em: `http://127.0.0.1:8000/docs`

---

## Como Testar (Dica Rápida)

Para interagir com as rotas protegidas na documentação (Swagger UI), você precisará de um Token.

1. Gere um token via CURL (usando suas credenciais de Client do Auth0).
2. No navegador (`/docs`), clique no botão **Authorize**.
3. Cole o token (sem a palavra Bearer).
4. Divirta-se testando os endpoints!

---

## Autor - Jarbas Santos

```
Exercício 3 – Plataforma de Comunidade com API REST
```
