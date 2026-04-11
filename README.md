# Dimensa IP API Backend Test

Projeto de teste técnico Backend utilizando **Python 3, Flask, MongoDB (Atlas) e Celery / Redis**. A API gerencia informações de localização e conectividade a partir de um IP utilizando a API pública `ipwho.is`.

## Estrutura do Projeto
```
/app
  /routes       -> endpoints
  /controller   -> lógica de negócios e persistência
  /database     -> conexão mongoDB
  /utils        -> middlewares, ex: token auth
  /workers      -> Celery workers
/tests          -> Pytest automatizado
docker-compose.yml -> Redis Local Environment
```

## Configurando o MongoDB Atlas (Cluster)

Para criar o banco de dados mongoDB na nuvem:

1. **Crie uma Conta:** Acesse [mongodb.com/atlas](https://www.mongodb.com/atlas) e crie sua conta gratuita.
2. **Crie um Projeto e Cluster:** 
   - Crie um novo projeto (ex: `Dimensa-API`).
   - Crie um Shared Cluster gratuito (M0). Escolha o provedor e região (ex: AWS - N. Virginia).
3. **Configure o Acesso à Rede (IP Whitelist):**
   - No menu lateral, vá em **Network Access** -> **Add IP Address**.
   - Clique em **Allow Access From Anywhere** (ou adicione seu IP atual) e confirme.
4. **Crie um Usuário de Banco de Dados:**
   - Vá em **Database Access** -> **Add New Database User**.
   - Escolha o método **Password**, defina um usuário e senha (anote-os!) e dê a permissão `Read and write to any database`.
5. **Obtenha a Connection String (MONGO_URI):**
   - Vá em **Database** (ou Clusters) e clique no botão **Connect**.
   - Escolha **Drivers** e selecione Python 3.x.
   - Copie a string `mongodb+srv://<db_username>:<db_password>@cluster0.xxxx.mongodb.net/?...` e substitua os campos entre `< >` pelos dados que você criou no passo 4.

## Passos para Instalação

Você precisa possuir instalado no seu computador:
- Python 3.9+
- Docker & Docker Compose (Para inicialização do Redis em modo broker local)

**1. Crie e ative um Ambiente Virtual (venv)**
O ambiente virtual isola as dependências do projeto. Na raiz do projeto, digite no terminal:

**No Windows:**
```powershell
python -m venv env
.\env\Scripts\activate
```

**No Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

**2. Instale as dependências**
Com o ambiente ativado, instale todos os pacotes obrigatórios através do PIP:
```powershell
pip install -r requirements.txt
pip install eventlet pytest pytest-cov
```


**3. Configure suas Variáveis de Ambiente**
Crie um arquivo novo chamado `.env` na raiz do projeto. Ele será o repositório das senhas e configurações. Preencha como o exemplo dado abaixo:
```env
MONGO_URI=mongodb+srv://<seu-login>:<sua-senha>@...
DB_NAME=ip_db
SECRET_TOKEN=123456
IPWHOIS_API_KEY=Opcional_token_aqui
REDIS_URL=redis://127.0.0.1:6379/0
```

## Como rodar o projeto

**1. Suba o ambiente Redis**
```bash
docker-compose up -d
```

**2. Rode a API Localmente(com o env ativado)**
```bash

python run.py
```
*(A API subirá em `http://127.0.0.1:5000`)*

**3. Inicie o Worker do Celery e o Beat (Separadamente no Windows e com o env ativado)**
Para que o serviço de background de 12 horas funcione, você precisa iniciar o worker e beat.

**No Terminal 2 - Worker do Celery (com o env ativado):**
```bash
pip install eventlet
celery -A app.workers.celery_app.celery worker --loglevel=info -P eventlet
```

**No Terminal 3 - Beat / Agendador (com o env ativado):**
```bash
celery -A app.workers.celery_app.celery beat --loglevel=info
```

## Endpoints Disponíveis
*(Atenção: envie o header `Authorization: Bearer <TOKEN>` em todas as rotas)*

- `POST /ips`: Cadastra ou busca um IP no cache interno do BD. No Body (`json`): `{"ip": "200.200.200.200"}`
- `GET /ips?page=1&limit=15&filter_ip=200`: Lista de forma paginada e com regex os IPs.

## Rodando os Testes automatizados
Para exercitar a suíte de testes de integração via Mock:
```bash
# com o env ativado
windows: python -m pytest tests/
linux/mac: pytest tests/
```
