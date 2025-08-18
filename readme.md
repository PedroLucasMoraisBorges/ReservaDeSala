# Sistema de Reserva de Salas

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-26.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)

---

## 📜 Descrição do Projeto

Este projeto é um sistema web para gerenciamento e reserva de salas de reunião. Ele permite que usuários cadastrados visualizem a disponibilidade das salas, agendem horários e gerenciem suas reservas. O sistema é projetado com perfis de usuário distintos, incluindo administradores (staff) que podem gerenciar salas e prédios.

---

## 📑 Índice

* [Stack de Tecnologias](#-stack-de-tecnologias)
* [Estrutura de Apps Django](#-estrutura-de-apps-django)
* [Iniciando o Projeto (Primeira Vez)](#-iniciando-o-projeto-primeira-vez)
* [Executando o Projeto](#️-executando-o-projeto)
* [Comandos Úteis do Docker Compose](#️-comandos-úteis-do-docker-compose)
* [Equipe e Papéis](#-equipe-e-papéis)

---

## 🚀 Stack de Tecnologias

* **Backend:** Python 3.13, Django 5.2
* **Banco de Dados:** PostgreSQL 17
* **Servidor WSGI:** Gunicorn (para produção)
* **Containerização:** Docker & Docker Compose

---

## 📦 Estrutura de Apps Django

| App         | Descrição                                                                      |
| ----------- | ------------------------------------------------------------------------------ |
| `core`      | App principal que contém as configurações do projeto, URLs e arquivos de base. |
| `auth_user` | Gerencia a autenticação, registro, login e perfis de usuários.                 |
| `rooms`     | Responsável pelo gerenciamento de salas (Rooms) e prédios (Buildings).         |
| `reserves`  | Controla a lógica de criação, visualização e cancelamento de reservas.         |

---

## ✨ Iniciando o Projeto (Primeira Vez)

Siga estes passos para configurar e executar o ambiente de desenvolvimento pela primeira vez.

### ✅ Pré-requisitos

Antes de começar, certifique-se de que você tem as seguintes ferramentas instaladas:

* [Git](https://git-scm.com/downloads)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído com o Docker Desktop)

### ⚙️ Passos para Instalação

**1. Clone o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_DIRETORIO>


**2. Configure as Variáveis de Ambiente**
Crie um arquivo chamado .env na raiz do projeto, copiando o conteúdo abaixo. Este arquivo é fundamental para configurar o banco de dados e as chaves secretas da aplicação.

```bash
# Arquivo: .env
SECRET_KEY='django-insecure-e4^u3_hk!(_$!i(om+%o0o(b2=(us*y0)h71%0bhp(@_s=+#&2'
DEBUG=True
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=ReservaDeSalasDb
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=0000
DATABASE_HOST=db
DATABASE_PORT=5432


**3. Construa e Inicie os Contêineres**
Este comando irá construir as imagens Docker (se ainda não existirem) e iniciar os serviços do Django e do PostgreSQL em modo de desenvolvimento. O -d (detached) executa os contêineres em segundo plano.

```bash
docker-compose up --build -d

O compose.override.yml garante que as migrações do banco de dados sejam aplicadas automaticamente na inicialização.

**4. Crie um Superusuário**
Para acessar a área administrativa do Django, crie uma conta de superusuário:

```bash
docker-compose exec django-web python manage.py createsuperuser

Siga as instruções no terminal para definir o e-mail, nome e senha.

Pronto! O ambiente de desenvolvimento está configurado.

## ▶️ Executando o Projeto
Após a configuração inicial, use os seguintes comandos na raiz do projeto para gerenciar o ambiente.

- Para iniciar os serviços:

```bash
docker-compose up

- Para parar os serviços:

```bash
docker-compose down


A aplicação estará acessível em http://localhost:8000.

## 🛠️ Comandos Úteis do Docker Compose
Todos os comandos devem ser executados a partir da raiz do projeto.

- **Executar Testes:**

´´´bash
docker-compose exec django-web python manage.py test

- **Acessar o Shell do Django:**

```bash
docker-compose exec django-web python manage.py shell

- **Acessar o Terminal (bash) do Contêiner Django:**

```bash
docker-compose exec django-web /bin/bash

- **Visualizar os Logs em Tempo Real:**

```bash
docker-compose logs -f