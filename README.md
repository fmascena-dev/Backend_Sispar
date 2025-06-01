# Documentação do Projeto Backend Sispar

*Este documento serve como um guia completo para configurar, executar e interagir com a API Flask do projeto.*

## Primeiros Passos

*Siga as instruções abaixo para obter uma cópia do projeto em sua máquina local para fins de desenvolvimento e teste.*

### Pré-requisitos

- *Antes de começar, certifique-se de ter o seguinte software instalado:*

    - *Python 3.8+*
    - *pip (gerenciador de pacotes Python)*
    - *Um sistema de banco de dados (ex: MySQL, PostgreSQL). O arquivo* `config.py` *utiliza a variável* `DATABASE_URL` *que pode ser configurada para diversos bancos de dados.*

### Instalação

- **Clone o repositório:**

```
git clone https://github.com/fmascena-dev/Backend_Sispar.git
cd Backend_Sispar
```


- **Crie um ambiente virtual (recomendado):**

```
python -m venv venv
```

- **Ative o ambiente virtual:**

```
No Windows:

.\venv\Scripts\activate
```

```
No macOS/Linux:

source venv/bin/activate
```

- **Instale as dependências:**

    - *O arquivo* **`requirements.txt`** *lista todos os pacotes Python necessários.*

```
pip install -r requirements.txt
```

### Variáveis de Ambiente

*O projeto utiliza variáveis de ambiente para sua configuração. Você precisará criar um arquivo .env na raiz do diretório do seu projeto.*

*Aqui estão as variáveis de ambiente necessárias, baseadas no config.py:*

- **`DATABASE_URL`**: *Sua string de conexão com o banco de dados. Exemplos:*
    - **MySQL**: `mysql://usuario:senha@host/nome_do_banco`
    - **PostgreSQL**: `postgresql://usuario:senha@host:porta/nome_do_banco`
- **`SECRET_KEY`**: *Uma string longa e aleatória usada para gerenciamento de sessão e segurança. Você pode gerar uma usando Python:*
```
import os
print(os.urandom(24).hex())
```

- **`FRONTEND_URL`**: *A URL da sua aplicação frontend. Isso é usado para a configuração do CORS. Se você estiver executando um frontend em* **`http://localhost:3000`**, *pode configurá-lo para isso.*

### Exemplo de arquivo **`.env`**:

```
DATABASE_URL=mysql://user:password@localhost/reimbursement_db
SECRET_KEY=sua_chave_secreta_super_segura
FRONTEND_URL=http://localhost:3000
```

### Executando o Projeto

*Após instalar as dependências e configurar suas variáveis de ambiente, você pode executar a aplicação Flask usando Gunicorn (conforme listado em* **`requirements.txt`** *e* **`Procfile`***):*

```
gunicorn --bind 0.0.0.0:$PORT src.app:app
```

*Este comando iniciará a aplicação, tornando-a acessível no endereço que o* **`$PORT`** *apontar (geralmente* **`http://0.0.0.0:5000`** *em ambientes de desenvolvimento ou a porta definida pelo provedor de hospedagem em produção). Para desenvolvimento local sem a variável* **`$PORT`**, *você pode simplesmente usar* **`gunicorn src.app:app`** *ou* **`flask run`**.

### Documentação da API (Swagger)

*Este projeto utiliza Flasgger para gerar uma documentação interativa da API. Uma vez que a aplicação esteja em execução, você pode acessar a interface do Swagger UI em:*

**`http://127.0.0.1:8000/apidocs/`** *(ou a porta na qual sua aplicação está rodando)*

*Esta interface permite que você explore os endpoints disponíveis, seus formatos de requisição esperados e exemplos de respostas.*

### Rotas Importantes da API

*A seguir, as principais rotas da API atualmente implementadas, divididas por seus respectivos blueprints:*

#### Rotas de Colaboradores (`/colaborador`)
    
- **GET (/colaborador/todos-colaboradores)**
    - **Descrição:** *Retorna uma lista de todos os colaboradores cadastrados no sistema.*
    - **Método: `GET`**
    - **Respostas:**
        - **`200 OK`**: *Retorna um array JSON de objetos* `Colaborador`, *contendo* `id`, `nome`, `cargo`, `salario` e `email`.
        - `500 Internal Server Error`: *Ocorreu um erro inesperado.*

---

- **POST (/colaborador/cadastrar)**
    - **Descrição:** *Cadastra um novo colaborador no sistema. A senha é automaticamente hashed antes de ser armazenada.*
    - **Método: `POST`**
    - **Corpo da Requisição (Exemplo):**

```JSON
{
    "nome": "João Silva",
    "email": "joao.silva@example.com",
    "senha": "senhaSegura123",
    "cargo": "Analista de RH",
    "salario": 3500.00
}
```

- **Respostas:**
    - **`201 Created`:** *Colaborador cadastrado com sucesso.*
    - **`400 Bad Request`:** *Dados de requisição inválidos ou incompletos.*
    - **`500 Internal Server Error`:** *Erro ao cadastrar o colaborador.*

---

- **PUT (/colaborador/atualizar/int:id_colaborador):**
    - **Descrição:** *Atualiza os dados de um colaborador existente com base no seu ID. Atualmente, este endpoint parece ter um erro lógico, pois itera sobre uma variável* `dados` *não definida e usa* `colaborador_encontrado` *de forma inadequada.* **Esta rota precisará de revisão para funcionar corretamente.**
    - **Método: `PUT`**
    - **Parâmetros:**
        - **`id_colaborador` (path):** *O ID único do colaborador a ser atualizado.*
    - **Corpo da Requisição (Exemplo):**

```JSON

{
    "nome": "João Silva Atualizado",
    "cargo": "Coordenador de RH"
}
```

- **Respostas (esperadas após correção):**
    - **`200 OK`:** *Dados do colaborador atualizados com sucesso.*
    - **`404 Not Found`:** *Colaborador com o ID fornecido não encontrado.*
    - **`400 Bad Request`:** *Dados de requisição inválidos.*
    - **`500 Internal Server Error`:** *Erro ao atualizar o colaborador.*
---
- **POST /colaborador/login**
    - **Descrição:** *Realiza o login de um colaborador, verificando o email e a senha fornecidos.*
    - **Método: `POST`**
    - **Corpo da Requisição (Exemplo):**

```JSON
{
    "email": "joao.silva@example.com",
    "senha": "senhaSegura123"
}
```

- **Respostas:**
    - **`200 OK`:** *Login realizado com sucesso.*
    - **`400 Bad Request`:** *Credenciais inválidas ou dados incompletos.*
    - **`404 Not Found`:** *Usuário não encontrado.*

---

#### Rotas de Reembolso (/reembolso)

- **POST (/reembolso/reembolsos)**
    - **Descrição:** *Cadastra um ou mais registros de reembolso.*
    - **Método: `POST`**
    - **Corpo da Requisição (exemplo de reembolso único):**

```JSON
{
    "colaborador": "Nome do Colaborador",
    "empresa": "Nome da Empresa",
    "num_prestacao": 12345,
    "descricao": "Despesa de Viagem",
    "data": "25/05/2025",
    "tipo_reembolso": "Transporte",
    "centro_custo": "CC001",
    "ordem_interna": "OI-001",
    "divisao": "Divisão A",
    "pep": "PEP-001",
    "moeda": "BRL",
    "distancia_km": "150",
    "valor_km": "1.50",
    "valor_faturado": 225.00,
    "despesa": 225.00,
    "status": "Em analise"
}
```

**Corpo da Requisição (exemplo de múltiplos reembolsos):**

```JSON
[
    {
        "colaborador": "Colaborador Um",
        "empresa": "Empresa Alfa",
        "num_prestacao": 1001,
        "descricao": "Almoço de Negócios",
        "data": "01/06/2025",
        "tipo_reembolso": "Alimentação",
        "centro_custo": "CC002",
        "moeda": "BRL",
        "valor_faturado": 50.75
    },
    {
        "colaborador": "Colaborador Dois",
        "empresa": "Empresa Beta",
        "num_prestacao": 1002,
        "descricao": "Combustível",
        "data": "02/06/2025",
        "tipo_reembolso": "Transporte",
        "centro_custo": "CC003",
        "moeda": "USD",
        "valor_faturado": 30.00,
        "distancia_km": "50",
        "valor_km": "0.75"
    }
]
```

- **Respostas:**
    - **`201 Created`:** *Reembolso(s) cadastrado(s) com sucesso.*
    - **`400 Bad Request`:** *Formato de dados inválido (ex: formato de data).*
    - **`404 Not Found`:** *Colaborador não encontrado.*
    - **`500 Internal Server Error`:** *Ocorreu um erro inesperado ao cadastrar o reembolso.*

---

- **GET (/reembolso/reembolsos)**
    - **Descrição:** *Retorna uma lista de todos os registros de reembolso.*
    - **Método: `GET`**

    - **Respostas:**
        - **`200 OK`:** *Retorna um array JSON de objetos de reembolso.*
        - **`500 Internal Server Error`:** *Ocorreu um erro inesperado.*

---

- **DELETE (/reembolso/reembolsos/int:id)**
    - **Descrição:** *Exclui um registro de reembolso específico pelo seu ID.*
    - **Método: `DELETE`**

    - **Parâmetros:**
        - **`id` (path):** *O identificador único do reembolso.*

    - **Respostas:**
        - **`200 OK`:** *Reembolso com o ID fornecido deletado com sucesso.*
        - **`404 Not Found`:** *Reembolso com o ID fornecido não encontrado.*
        - **`500 Internal Server Error`:** *Ocorreu um erro inesperado ao deletar o reembolso.*

---

- **GET (/reembolso/reembolsos/prestacao/string:num_prestacao)**
    - **Descrição:** *Retorna registros de reembolso pelo seu* `num_prestacao` *(número da prestação).*
    - **Método: `GET`**

    - **Parâmetros:**
        - **`num_prestacao` (path):** *O número da prestação a ser pesquisado.*

    - **Respostas:**
        - **`200 OK`:** *Retorna um array JSON de objetos de reembolso que correspondem ao num_prestacao.*
        - **`404 Not Found`:** *Nenhum reembolso encontrado para o número de prestação fornecido.*
        - **`500 Internal Server Error`:** *Ocorreu um erro inesperado ao buscar reembolsos por número de prestação.*
