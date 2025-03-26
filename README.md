# Testes de Nivelamento - IntuitiveCare

Repositório contendo as soluções para os 4 desafios técnicos do processo seletivo da IntuitiveCare.

## 👋 Sumário

1. [Desafio 1 - Web Scraping](#-desafio-1---web-scraping)
2. [Desafio 2 - Transformação de Dados](#-desafio-2---transformação-de-dados)
3. [Desafio 3 - Banco de Dados](#-desafio-3---banco-de-dados)
4. [Desafio 4 - API + Interface Web](#-desafio-4---api--interface-web)
5. [Diferenciais Implementados](#-diferenciais-implementados)

---

## 🕷️ Desafio 1 - Web Scraping

**Objetivo**: Baixar os Anexos I e II do site da ANS e compactá-los em um arquivo ZIP.

### Como executar:

```bash
cd Web Scraping
pip install -r requirements.txt
python teste1_web_scraping.py
```

### Estrutura de arquivos:
```
Web Scraping/
├── anexos/               # Pasta com os PDFs baixados
│   ├── Anexo_I.pdf
│   └── Anexo_II.pdf
├── teste1_web_scraping.py       # Script principal
├── requirements.txt      # Dependências (requests, beautifulsoup4)
└── Anexos_ANS.zip            # Arquivo compactado gerado
```

---

## 🔄 Desafio 2 - Transformação de Dados

**Objetivo**: Extrair dados da tabela do Anexo I, transformar em CSV e compactar.

### Como executar:

```bash
cd Transformação de Dados
pip install -r requirements.txt
python teste2_transformacao_dados.py
```

### Estrutura de arquivos:
```
Transformação de Dados/
├── Rol_de_Procedimentos.csv  # Arquivo CSV gerado
├── teste2_transformacao_dados.py          # Script principal
├── requirements.txt          # Dependências (pandas, tabula-py)
└── Teste_PlinioGoncalves.zip      # Arquivo final compactado
```

---

## 💃️ Desafio 3 - Banco de Dados

**Objetivo**: Criar um banco de dados com dados das operadoras e demonstrativos contábeis.

### Pré-requisitos:

- PostgreSQL 13+ instalado
- Banco criado com nome `ans_database`

### Como executar:

```bash
cd Banco de Dados
pip install -r requirements.txt

# Para baixar os dados e executar tudo:
python main.py --download

# Apenas para carregar dados existentes:
python main.py
```

### Estrutura de arquivos:
```
Banco de Dados/
├── data/
│   ├── demonstracoes_contabeis/  # Arquivos ZIP baixados
│   └── operadoras_ativas.csv     # Dados das operadoras
├── scripts/
│   └── sql/                      # Scripts SQL
|    helpers.py
├── config.py                     # Configurações
├── database_manager.py           # Gerenciamento do banco
├── download_data.py              # Download dos dados
└── main.py                       # Script principal
└── requirements.txt              # Dependências
```

---

## 🌐 Desafio 4 - API + Interface Web

**Objetivo**: Criar uma interface web para buscar operadoras de saúde.

### Como executar:

#### Backend (API):
```bash
cd api/backend
pip install -r requirements.txt
python server.py
```

#### Frontend (Vue.js):
```bash
cd api/frontend
npm install
npm run serve
```
Acesse: [http://localhost:8080](http://localhost:8080)

### Estrutura de arquivos:
```
4-API/
├── backend/
│   ├── server.py         # API Flask
│   ├── requirements.txt
│   └── operadoras.csv    # Dados das operadoras
└── frontend/             # Aplicação Vue.js
    ├── src/
    │   ├── components/   # Componentes Vue
    │   ├── App.vue       # Componente principal
    │   └── main.js       # Ponto de entrada
    └── package.json      # Dependências JavaScript
```

---

## 🚀 Diferenciais Implementados

### ✅ Organização do Código
- Estrutura modularizada
- Separação clara entre configuração e lógica

### ✅ Tratamento de Erros
- Exceções específicas para cada cenário
- Mensagens de erro claras

### ✅ Documentação
- READMEs detalhados
- Comentários no código

### ✅ Performance
- Índices no banco de dados
- Paginação de resultados

### ✅ Práticas Recomendadas
- Type hints em Python
- Componentes Vue reutilizáveis
- Variáveis de ambiente para configurações

---

## 📝 Notas Adicionais

- Todos os scripts foram testados em **Python 3.9+**
- Certifique-se de ter o **Java** instalado para o `tabula-py` (Desafio 2)
- Para o **Desafio 4**, recomendo o **Node.js 16+**
