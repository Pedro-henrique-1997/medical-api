# Medical API

API REST desenvolvida com Django REST Framework para gerenciamento de

profissionais e consultas médicas.

O projeto foi construído com foco em organização, segurança,

autenticação, testes automatizados, containerização e integração

contínua.

> \*\*\*\*Status:\*\*\*\* backend, testes, Docker e CI concluídos. A
> etapa de deploy

> em AWS ainda será configurada e validada antes da entrega final.

## Tecnologias

-     Python 3.13

-     Django 6.1

-     Django REST Framework

-     PostgreSQL 17

-     Simple JWT

-     django-cors-headers

-     python-dotenv

-     Docker

-     Docker Compose

-     Gunicorn

-     Poetry

-     Pytest

-     Pytest-Django

-     Ruff

-     Git

-     GitHub

-     GitHub Actions

## Funcionalidades

### Profissionais

A API permite:

-     criar profissional;

-     listar profissionais;

-     buscar profissional por ID;

-     atualizar profissional;

-     atualizar parcialmente;

-     excluir profissional.

Campos principais:

-     nome social (`social_name`);

-     profissão (`profession`);

-     endereço (`address`);

-     contato (`contact`).

Os profissionais utilizam UUID como identificador.

### Consultas

A API permite:

-     criar consulta;

-     listar consultas;

-     buscar consulta por ID;

-     atualizar consulta;

-     atualizar parcialmente;

-     excluir consulta;

-     filtrar consultas por profissional.

Cada consulta possui:

-     UUID como identificador;

-     data e horário (`date`);

-     relacionamento com um profissional (`professional`).

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

GET    /api/professionals/

POST   /api/professionals/

GET    /api/professionals/<id>/

PUT    /api/professionals/<id>/

PATCH  /api/professionals/<id>/

DELETE /api/professionals/<id>/
```

### Consultas

``` http

GET    /api/appointments/

POST   /api/appointments/

GET    /api/appointments/<id>/

PUT    /api/appointments/<id>/

PATCH  /api/appointments/<id>/

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

│   ├── migrations/

│   ├── models.py

│   ├── serializers.py

│   ├── tests.py

│   ├── urls.py

│   └── views.py

│

├── professionals/

│   ├── migrations/

│   ├── models.py

│   ├── serializers.py

│   ├── tests.py

│   ├── urls.py

│   └── views.py

│

├── config/

│   ├── settings.py

│   ├── urls.py

│   ├── asgi.py

│   └── wsgi.py

│

├── .github/

│   └── workflows/

│       └── ci.yml

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

│   ├── Django

│   ├── Django REST Framework

│   └── Gunicorn

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

O projeto possui \*\*\*\*19 testes automatizados\*\*\*\* utilizando
Django REST

Framework `APITestCase`, Pytest e pytest-django.

A suíte cobre, entre outros cenários:

-     criação de profissionais;

-     listagem de profissionais;

-     busca de profissional por ID;

-     atualização completa de profissional;

-     atualização parcial de profissional;

-     exclusão de profissional;

-     dados inválidos;

-     acesso sem autenticação;

-     criação de consultas;

-     listagem de consultas;

-     busca de consulta por ID;

-     atualização completa de consulta;

-     atualização parcial de consulta;

-     exclusão de consulta;

-     profissional inexistente;

-     data inválida;

-     campos obrigatórios ausentes;

-     acesso sem autenticação;

-     filtro de consultas por profissional.

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

1.   checkout do repositório;

2.   configuração do Python 3.13;

3.   instalação do Poetry;

4.   instalação das dependências;

5.   inicialização de um PostgreSQL 17 de teste;

6.   `python manage.py check`;

7.   `ruff check .`;

8.   execução da suíte com `pytest`.

O CI foi validado com sucesso no GitHub Actions.

O banco criado pelo workflow existe somente durante a execução do CI e

não utiliza o banco local ou futuro banco de produção.

## Segurança

Medidas aplicadas no projeto:

-     autenticação JWT;

-     endpoints protegidos;

-     refresh token;

-     variáveis sensíveis carregadas por ambiente;

-     `.env` fora do Git;

-     `.env.example` sem credenciais reais;

-     validação de entrada por serializers do Django REST Framework;

-     relacionamento com profissionais validado pelo ORM/serializer;

-     acesso ao banco através do ORM do Django, sem concatenação manual
    de

    SQL nas operações implementadas;

-     CORS configurável por variável de ambiente;

-     PostgreSQL não publicado para o host no Docker Compose atual;

-     Gunicorn para servir a aplicação containerizada;

-     logs do Django configurados;

-     testes automatizados;

-     análise estática com Ruff;

-     CI automatizado no GitHub Actions.

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

-     formato inválido de data;

-     campos obrigatórios ausentes;

-     referência a profissional inexistente;

-     requisição sem autenticação.

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

A aplicação está preparada para implantação com Docker, Gunicorn,
PostgreSQL e configurações fornecidas por variáveis de ambiente.

O pipeline de integração contínua foi implementado e validado com GitHub
Actions.

O provisionamento dos ambientes de staging e produção na AWS não foi
realizado, pois a criação da infraestrutura exigia uma conta AWS
habilitada com método de pagamento, indisponível durante o
desenvolvimento do desafio.

Essa limitação não altera a configuração local/containerizada do
projeto. Credenciais e configurações específicas de um ambiente de
produção devem ser fornecidas externamente e nunca armazenadas no
repositório.

### Arquitetura proposta para deploy

A arquitetura abaixo representa uma proposta de implantação e **não foi
provisionada na AWS**:

``` text
GitHub
  |
  v
GitHub Actions / CI
  |
  v
Staging
  |
  v
Produção
  |
  v
Django + Gunicorn
  |
  v
PostgreSQL
```

Em uma implantação real, staging e produção devem utilizar configurações
e segredos próprios, mantendo os ambientes isolados.

## Estratégia de rollback

Uma estratégia proposta de rollback é manter releases e imagens Docker
versionadas por tag ou commit.

Caso uma nova implantação apresente problemas:

1.  identificar a última versão estável;
2.  selecionar a imagem ou release correspondente;
3.  realizar novamente o deploy utilizando a versão anterior;
4.  validar endpoints, autenticação e logs após o retorno;
5.  investigar a versão com falha antes de uma nova publicação.

Alterações de banco de dados exigem cuidado adicional. Migrations devem
ser planejadas de forma compatível com a versão anterior sempre que um
rollback da aplicação puder ser necessário.

Essa estratégia está documentada como proposta de produção e não
representa um fluxo AWS já provisionado.

## Status do projeto

 Item ------- Status

**------------------------- -----------**

 CRUD de profissionais -- Concluído

 CRUD de consultas -- Concluído

 Filtro por profissional -- Concluído

  JWT --  Concluído

 CORS  -- Concluído

 PostgreSQL -- Concluído

 Validações -- Concluído

 Logs -- Concluído

 Testes automatizados -- 19/19

 Ruff -- Aprovado

 Docker -- Concluído

 Gunicorn -- Concluído

 Git/GitHub -- Concluído

 GitHub Actions / CI --  Aprovado

 AWS / staging Não provisionado

 AWS / produção Não provisionado

 Revisão final --  Concluida


 ---

## Testes manuais da API com Postman

Além dos **19 testes automatizados executados com pytest**, a API também pode ser validada manualmente utilizando o Postman.

Antes de iniciar os testes, certifique-se de que a aplicação esteja em execução:

```bash
docker compose up -d
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

Os endpoints de profissionais e agendamentos são protegidos por autenticação JWT. Portanto, primeiro é necessário gerar um token de acesso.

### 1. Gerar token JWT

**Método:** `POST`

```text
http://127.0.0.1:8000/api/token/
```

No Postman, selecione:

```text
Body → raw → JSON
```

Envie:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Resposta esperada:

```text
HTTP 200 OK
```

Exemplo:

```json
{
  "refresh": "...",
  "access": "..."
}
```

Copie o valor de `access`.

Nas próximas requisições protegidas, utilize no Postman:

```text
Authorization → Bearer Token
```

e informe o token de acesso recebido.

---

### 2. Listar profissionais

**Método:** `GET`

```text
http://127.0.0.1:8000/api/professionals/
```

Autenticação:

```text
Authorization: Bearer <access_token>
```

Resultado esperado:

```text
HTTP 200 OK
```

A resposta deve retornar a lista de profissionais cadastrados.

---

### 3. Criar profissional

**Método:** `POST`

```text
http://127.0.0.1:8000/api/professionals/
```

Autenticação:

```text
Authorization: Bearer <access_token>
```

No Postman:

```text
Body → raw → JSON
```

Exemplo:

```json
{
  "social_name": "Maria Silva",
  "profession": "Psicóloga",
  "address": "Rua Exemplo, 100",
  "contact": "11999999999"
}
```

Resultado esperado:

```text
HTTP 201 Created
```

A resposta deverá conter os dados do profissional e seu UUID.

Guarde o valor do campo `id`, pois ele poderá ser utilizado nos testes seguintes.

---

### 4. Consultar um profissional

**Método:** `GET`

```text
http://127.0.0.1:8000/api/professionals/<uuid_do_profissional>/
```

Autenticação:

```text
Authorization: Bearer <access_token>
```

Resultado esperado:

```text
HTTP 200 OK
```

---

### 5. Atualizar parcialmente um profissional

**Método:** `PATCH`

```text
http://127.0.0.1:8000/api/professionals/<uuid_do_profissional>/
```

Exemplo de Body:

```json
{
  "contact": "11888888888"
}
```

Resultado esperado:

```text
HTTP 200 OK
```

---

### 6. Criar agendamento

**Método:** `POST`

```text
http://127.0.0.1:8000/api/appointments/
```

Autenticação:

```text
Authorization: Bearer <access_token>
```

No Postman:

```text
Body → raw → JSON
```

Exemplo:

```json
{
  "date": "2026-09-01T14:30:00Z",
  "professional": "<uuid_do_profissional>"
}
```

Resultado esperado:

```text
HTTP 201 Created
```

A resposta deverá retornar o agendamento criado e seu UUID.

---

### 7. Listar agendamentos

**Método:** `GET`

```text
http://127.0.0.1:8000/api/appointments/
```

Autenticação:

```text
Authorization: Bearer <access_token>
```

Resultado esperado:

```text
HTTP 200 OK
```

---

### 8. Filtrar agendamentos por profissional

A API permite buscar os agendamentos relacionados a um profissional específico através do UUID.

**Método:** `GET`

```text
http://127.0.0.1:8000/api/appointments/?professional=<uuid_do_profissional>
```

Autenticação:

```text
Authorization: Bearer <access_token>
```

Resultado esperado:

```text
HTTP 200 OK
```

A resposta deverá conter apenas os agendamentos associados ao profissional informado.

---

### 9. Validar profissional inexistente

Tente cadastrar um agendamento utilizando um UUID de profissional que não existe.

**Método:** `POST`

```text
http://127.0.0.1:8000/api/appointments/
```

Exemplo:

```json
{
  "date": "2026-09-01T14:30:00Z",
  "professional": "00000000-0000-0000-0000-000000000000"
}
```

Resultado esperado:

```text
HTTP 400 Bad Request
```

Esse teste verifica a validação do relacionamento entre agendamento e profissional.

---

### 10. Validar data inválida

**Método:** `POST`

```text
http://127.0.0.1:8000/api/appointments/
```

Exemplo:

```json
{
  "date": "data-invalida",
  "professional": "<uuid_do_profissional>"
}
```

Resultado esperado:

```text
HTTP 400 Bad Request
```

---

### 11. Testar endpoint sem autenticação

Remova temporariamente o Bearer Token e faça:

**Método:** `GET`

```text
http://127.0.0.1:8000/api/professionals/
```

Resultado esperado:

```text
HTTP 401 Unauthorized
```

Esse teste confirma que os endpoints protegidos não podem ser acessados sem autenticação JWT.

---

### 12. Renovar token JWT

**Método:** `POST`

```text
http://127.0.0.1:8000/api/token/refresh/
```

No Body, envie o `refresh` obtido durante a autenticação:

```json
{
  "refresh": "<refresh_token>"
}
```

Resultado esperado:

```text
HTTP 200 OK
```

A resposta deverá fornecer um novo token de acesso.

---

### Observação sobre os testes

Os testes descritos acima são destinados à **validação manual da API utilizando Postman**.

A validação automatizada do projeto é realizada separadamente através do pytest:

```bash
poetry run pytest
```

O projeto possui **19 testes automatizados**, cobrindo autenticação, CRUD, validações e filtro de agendamentos por profissional.

Esses testes também são executados automaticamente pelo pipeline de CI configurado no GitHub Actions.

---

## Proposta de integração com Asaas — Split de Pagamento

Como evolução da aplicação, é proposta uma integração com a **Asaas** para permitir o processamento de pagamentos relacionados aos atendimentos e a divisão dos valores através de split de pagamento.

> Esta integração é uma proposta arquitetural e não foi implementada nesta versão do projeto.

### Objetivo

Em um cenário de produção, após o agendamento de um atendimento, a aplicação poderia gerar uma cobrança através da API da Asaas.

O pagamento poderia ser dividido entre os participantes definidos pela regra de negócio, como, por exemplo:

```text
Paciente
   │
   │ realiza pagamento
   ▼
Medical API
   │
   │ solicita criação da cobrança
   ▼
API Asaas
   │
   ├── Parte do valor → Profissional
   │
   └── Parte do valor → Plataforma
```

### Fluxo proposto

```text
1. Paciente solicita/agende um atendimento
                │
                ▼
2. Medical API registra o agendamento
                │
                ▼
3. Medical API solicita uma cobrança à Asaas
                │
                ▼
4. Asaas cria a cobrança
                │
                ▼
5. Pagamento é realizado
                │
                ▼
6. Asaas processa o pagamento e o split
                │
                ├──► Profissional
                │
                └──► Plataforma
                │
                ▼
7. Asaas envia atualização por webhook
                │
                ▼
8. Medical API atualiza o status do pagamento
```

### Possível implementação

Uma implementação futura poderia adicionar uma entidade de pagamento relacionada ao agendamento.

Exemplo conceitual:

```text
Appointment
    │
    │ 1:1
    ▼
Payment
    ├── id
    ├── appointment
    ├── external_payment_id
    ├── amount
    ├── status
    └── created_at
```

Após a criação de um agendamento, a aplicação poderia solicitar a geração da cobrança na Asaas e armazenar o identificador externo retornado pela plataforma.

O split seria configurado conforme as regras de negócio definidas para o profissional e para a plataforma.

### Webhooks

Para evitar depender de consultas constantes ao serviço externo, a aplicação poderia disponibilizar um endpoint específico para receber eventos enviados pela Asaas.

Exemplo conceitual:

```text
POST /api/webhooks/asaas/
```

Esse endpoint poderia receber eventos relacionados ao ciclo de vida do pagamento, permitindo que a aplicação atualize seu estado interno.

Fluxo:

```text
Asaas
  │
  │ webhook
  ▼
/api/webhooks/asaas/
  │
  ▼
Validação do evento
  │
  ▼
Localização do pagamento
  │
  ▼
Atualização do status
```

### Segurança da integração

Em uma implementação real, alguns cuidados seriam necessários:

- credenciais da Asaas armazenadas em variáveis de ambiente;
- nenhuma chave de API versionada no Git;
- validação das requisições recebidas pelo webhook;
- comunicação através de HTTPS;
- tratamento de falhas e indisponibilidade da API externa;
- registro de logs das operações de pagamento;
- prevenção de processamento duplicado de eventos;
- validação dos valores antes da criação do split.

As credenciais poderiam ser configuradas externamente, seguindo o mesmo princípio já utilizado no projeto para informações sensíveis:

```env
ASAAS_API_KEY=your-api-key
```

O arquivo `.env.example` conteria apenas o nome da variável, nunca uma credencial real.

### Tratamento de falhas

Caso a Asaas estivesse temporariamente indisponível, a criação do agendamento não precisaria necessariamente ser perdida.

Uma estratégia possível seria:

```text
Agendamento criado
       │
       ▼
Tentativa de criar pagamento
       │
       ├── Sucesso → salva identificador da cobrança
       │
       └── Falha   → registra erro e permite nova tentativa
```

Em uma evolução da arquitetura, o processamento também poderia ser realizado de forma assíncrona através de uma fila de tarefas.

### Status da integração

```text
Proposta de fluxo       → Documentada
Split de pagamento      → Proposto
Webhook                 → Proposto
Persistência pagamento  → Proposta
Integração real Asaas   → Não implementada
```

A proposta demonstra como a API poderia evoluir para integrar pagamentos sem acoplar diretamente a lógica principal de agendamentos ao serviço externo.

## Autor

Pedro Henrique Carneiro Gomes da Silva

Linkedin: https://www.linkedin.com/in/pedro-hgomes-dev/

github: https://github.com/Pedro-henrique-1997
