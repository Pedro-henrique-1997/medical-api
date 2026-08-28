# Medical API

API REST desenvolvida com Django REST Framework para gerenciamento de
profissionais e consultas médicas.

O projeto foi construído com foco em organização, segurança,
autenticação, testes automatizados, containerização e integração
contínua.

> **Status:** backend, testes, Docker e CI concluídos. A etapa de deploy
> em AWS ainda será configurada e validada antes da entrega final.

## Tecnologias

-   Python 3.13
-   Django 6.1
-   Django REST Framework
-   PostgreSQL 17
-   Simple JWT
-   django-cors-headers
-   python-dotenv
-   Docker
-   Docker Compose
-   Gunicorn
-   Poetry
-   Pytest
-   Pytest-Django
-   Ruff
-   Git
-   GitHub
-   GitHub Actions

## Funcionalidades

### Profissionais

A API permite:

-   criar profissional;
-   listar profissionais;
-   buscar profissional por ID;
-   atualizar profissional;
-   atualizar parcialmente;
-   excluir profissional.

Campos principais:

-   nome social (`social_name`);
-   profissão (`profession`);
-   endereço (`address`);
-   contato (`contact`).

Os profissionais utilizam UUID como identificador.

### Consultas

A API permite:

-   criar consulta;
-   listar consultas;
-   buscar consulta por ID;
-   atualizar consulta;
-   atualizar parcialmente;
-   excluir consulta;
-   filtrar consultas por profissional.

Cada consulta possui:

-   UUID como identificador;
-   data e horário (`date`);
-   relacionamento com um profissional (`professional`).

O relacionamento entre consulta e profissional é feito por chave
estrangeira.

### Filtro por profissional

É possível listar apenas as consultas associadas a determinado
profissional:

``` http
GET /api/appointments/?professional=<UUID_DO_PROFISSIONAL>
```

## Autenticação JWT

Os endpoints da API são protegidos por autenticação JWT.

Uma requisição sem credenciais para endpoints protegidos retorna:

``` text
HTTP 401 Unauthorized
WWW-Authenticate: Bearer
```

Exemplo:

``` json
{
  "detail": "Authentication credentials were not provided."
}
```

### Obter tokens

``` http
POST /api/token/
```

Corpo da requisição:

``` json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Resposta:

``` json
{
  "refresh": "...",
  "access": "..."
}
```

### Atualizar o access token

``` http
POST /api/token/refresh/
```

Exemplo:

``` json
{
  "refresh": "SEU_REFRESH_TOKEN"
}
```

Para acessar os endpoints protegidos, envie o access token no cabeçalho:

``` text
Authorization: Bearer SEU_ACCESS_TOKEN
```

## Endpoints

### Profissionais

``` http
GET    /api/professionals/
POST   /api/professionals/
GET    /api/professionals/<id>/
PUT    /api/professionals/<id>/
PATCH  /api/professionals/<id>/
DELETE /api/professionals/<id>/
```

### Consultas

``` http
GET    /api/appointments/
POST   /api/appointments/
GET    /api/appointments/<id>/
PUT    /api/appointments/<id>/
PATCH  /api/appointments/<id>/
DELETE /api/appointments/<id>/
```

### Consultas por profissional

``` http
GET /api/appointments/?professional=<UUID>
```

## Estrutura do projeto

``` text
medical_api/
│
├── appointments/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── professionals/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Variáveis de ambiente

As configurações sensíveis não ficam gravadas diretamente no código.

Crie um arquivo `.env` na raiz com base em `.env.example`.

Exemplo:

``` env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

POSTGRES_DB=api_medico
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
```

O arquivo `.env` contém valores privados e está incluído no
`.gitignore`. Ele não deve ser enviado ao repositório.

O `.env.example` contém somente valores de exemplo e deve ser
versionado.

## PostgreSQL

O banco utilizado é PostgreSQL 17.

Quando a aplicação é executada pelo Docker Compose, o Django acessa o
PostgreSQL pela rede interna:

``` text
db:5432
```

O serviço do banco não precisa publicar a porta `5432` para o host para
que a aplicação Django se comunique com ele.

## Docker

A aplicação possui um `Dockerfile` para construir a imagem do Django e
um `docker-compose.yml` para executar a API e o PostgreSQL.

Arquitetura local:

``` text
Docker Compose
│
├── web
│   ├── Django
│   ├── Django REST Framework
│   └── Gunicorn
│
└── db
    └── PostgreSQL 17
```

### Construir a imagem

``` bash
docker compose build
```

### Iniciar os containers

``` bash
docker compose up -d
```

### Verificar os containers

``` bash
docker compose ps
```

### Ver logs da API

``` bash
docker compose logs web
```

### Parar os containers

``` bash
docker compose down
```

A API fica disponível localmente em:

``` text
http://127.0.0.1:8000
```

As migrations são executadas durante a inicialização configurada no
serviço web do Docker Compose.

## Gunicorn

O container da API utiliza Gunicorn para servir a aplicação WSGI do
Django.

Aplicação WSGI:

``` text
config.wsgi:application
```

Exemplo do comando:

``` bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Isso substitui o servidor de desenvolvimento `runserver` no fluxo
containerizado preparado para implantação.

## Desenvolvimento local

### Instalar dependências

``` bash
poetry install
```

### Executar migrations

``` bash
poetry run python manage.py migrate
```

### Iniciar o servidor de desenvolvimento

``` bash
poetry run python manage.py runserver
```

Ao executar Django diretamente no computador, fora do Docker, o host do
PostgreSQL pode precisar ser:

``` env
POSTGRES_HOST=localhost
```

Dentro do Docker Compose:

``` env
POSTGRES_HOST=db
```

## Testes automatizados

O projeto possui **19 testes automatizados** utilizando Django REST
Framework `APITestCase`, Pytest e pytest-django.

A suíte cobre, entre outros cenários:

-   criação de profissionais;
-   listagem de profissionais;
-   busca de profissional por ID;
-   atualização completa de profissional;
-   atualização parcial de profissional;
-   exclusão de profissional;
-   dados inválidos;
-   acesso sem autenticação;
-   criação de consultas;
-   listagem de consultas;
-   busca de consulta por ID;
-   atualização completa de consulta;
-   atualização parcial de consulta;
-   exclusão de consulta;
-   profissional inexistente;
-   data inválida;
-   campos obrigatórios ausentes;
-   acesso sem autenticação;
-   filtro de consultas por profissional.

Executar:

``` bash
poetry run pytest
```

Resultado validado durante o desenvolvimento:

``` text
19 passed
```

## Django system check

Para verificar a configuração do projeto:

``` bash
poetry run python manage.py check
```

Resultado esperado:

``` text
System check identified no issues (0 silenced).
```

## Qualidade de código

O projeto utiliza Ruff para análise estática e padronização básica do
código.

Executar:

``` bash
poetry run ruff check .
```

Resultado validado:

``` text
All checks passed!
```

As migrations geradas automaticamente pelo Django são excluídas das
verificações configuradas do Ruff.

## CI com GitHub Actions

O repositório possui integração contínua através do GitHub Actions.

O workflow está localizado em:

``` text
.github/workflows/ci.yml
```

Ele é executado em pushes e pull requests para a branch `main`.

O pipeline realiza:

1.  checkout do repositório;
2.  configuração do Python 3.13;
3.  instalação do Poetry;
4.  instalação das dependências;
5.  inicialização de um PostgreSQL 17 de teste;
6.  `python manage.py check`;
7.  `ruff check .`;
8.  execução da suíte com `pytest`.

O CI foi validado com sucesso no GitHub Actions.

O banco criado pelo workflow existe somente durante a execução do CI e
não utiliza o banco local ou futuro banco de produção.

## Segurança

Medidas aplicadas no projeto:

-   autenticação JWT;
-   endpoints protegidos;
-   refresh token;
-   variáveis sensíveis carregadas por ambiente;
-   `.env` fora do Git;
-   `.env.example` sem credenciais reais;
-   validação de entrada por serializers do Django REST Framework;
-   relacionamento com profissionais validado pelo ORM/serializer;
-   acesso ao banco através do ORM do Django, sem concatenação manual de
    SQL nas operações implementadas;
-   CORS configurável por variável de ambiente;
-   PostgreSQL não publicado para o host no Docker Compose atual;
-   Gunicorn para servir a aplicação containerizada;
-   logs do Django configurados;
-   testes automatizados;
-   análise estática com Ruff;
-   CI automatizado no GitHub Actions.

Credenciais e chaves de ambientes de staging e produção devem ser
fornecidas por variáveis de ambiente ou por um mecanismo apropriado de
gerenciamento de segredos, nunca commitadas no Git.

## Logs

O projeto possui configuração de logging do Django com saída para
console.

Isso permite que os logs sejam capturados pelo ambiente onde a aplicação
estiver sendo executada, inclusive pelo Docker.

Para visualizar os logs do container:

``` bash
docker compose logs web
```

## Validação e integridade

O Django REST Framework valida os dados recebidos antes da persistência.

Exemplos de cenários cobertos:

-   formato inválido de data;
-   campos obrigatórios ausentes;
-   referência a profissional inexistente;
-   requisição sem autenticação.

O relacionamento entre `Appointment` e `Professional` é mantido por uma
`ForeignKey`.

## Git e versionamento

A branch principal do projeto é:

``` text
main
```

Arquivos importantes versionados:

``` text
Dockerfile
docker-compose.yml
.dockerignore
.env.example
pyproject.toml
poetry.lock
.github/workflows/ci.yml
```

Arquivos sensíveis ou locais, como `.env`, ambientes virtuais, caches e
logs, são ignorados através do `.gitignore`.

## Deploy

A aplicação já está preparada para execução containerizada com:

-   Docker;
-   PostgreSQL;
-   variáveis de ambiente;
-   migrations;
-   Gunicorn.

A configuração e validação de **staging e produção na AWS ainda serão
realizadas** antes da entrega final.

Essa seção será atualizada com a arquitetura e o procedimento reais de
deploy depois que os ambientes forem criados e testados.

## Rollback

A estratégia definitiva de rollback será documentada juntamente com o
deploy.

A intenção é manter releases versionadas e permitir o retorno para uma
versão anterior estável da aplicação caso uma implantação apresente
problemas.

Não é considerado concluído até que o fluxo de deploy seja efetivamente
configurado e validado.

## Status do projeto

  Item                      Status
  ------------------------- -----------
  CRUD de profissionais     Concluído
  CRUD de consultas         Concluído
  Filtro por profissional   Concluído
  JWT                       Concluído
  CORS                      Concluído
  PostgreSQL                Concluído
  Validações                Concluído
  Logs                      Concluído
  Testes automatizados      19/19
  Ruff                      Aprovado
  Docker                    Concluído
  Gunicorn                  Concluído
  Git/GitHub                Concluído
  GitHub Actions / CI       Aprovado
  AWS / staging             Pendente
  AWS / produção            Pendente
  Revisão final             Pendente

## Autor

Pedro Henrique Carneiro Gomes da Silva
Linkedin: https://www.linkedin.com/in/pedro-hgomes-dev/
github: https://github.com/Pedro-henrique-1997
