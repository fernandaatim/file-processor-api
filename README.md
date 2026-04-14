# File Processor API

![version](https://img.shields.io/badge/version-v0.1.0-blue)

Projeto desenvolvido com fins de estudo. O objetivo é explorar na prática tecnologias como FastAPI, Pandas, OpenPyXL, além de boas práticas de versionamento com Git (utilizando branches e Git Flow) e futuramente integração com banco de dados, construindo uma API funcional de processamento de arquivos CSV e Excel com validações e geração de métricas básicas.

---

## Funcionalidades

- Upload de arquivos `.csv`, `.xls` e `.xlsx`
- Cálculo do total da coluna `valor`
- Identificação de valores negativos
- Detecção de registros duplicados
- Validação de colunas obrigatórias (`id`, `cliente`, `valor`)
- Armazenamento local dos arquivos processados
- Limite de tamanho de upload via variável de ambiente

---

## Estrutura do Projeto

```
file-processor-api/
│
├── src/
│   └── app/
│       ├── main.py
│       ├── routes/
│       │   └── upload.py
│       └── services/
│           └── processor.py
│
├── data/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
└── run.ps1
```

---

## Instalação

```bash
git clone git@github.com:SEU_USUARIO/file-processor-api.git
cd file-processor-api
python -m venv venv

venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` com base no `.env.example`:

```env
MAX_FILE_SIZE=5000000
PYTHONPATH=src
```

---

## Execução

**Windows:**
```bash
.\run.ps1
```

**Linux/Mac:**
```bash
PYTHONPATH=src uvicorn src.app.main:app --reload
```

A API estará disponível em: http://127.0.0.1:8000/docs

---

## Endpoint

### POST /upload

Realiza o upload de um arquivo CSV ou Excel para processamento.

#### Requisição

- Tipo: `multipart/form-data`
- Campo: `file`

#### Resposta

```json
{
  "total_value": 450.0,
  "qtd_records": 5,
  "negative_values": [],
  "duplicate_values": []
}
```

---

## Observações

- Arquivos com colunas ausentes serão rejeitados
- Arquivos acima do limite definido serão rejeitados
- Arquivos processados são salvos no diretório `data/`

---

## Próximos passos

- [ ] Testes automatizados com `pytest`
- [x] Suporte a mais formatos de arquivo (ex: `.json`, `.parquet`)
- [x] Detecção automática de separador e encoding no CSV
- [x] Autenticação via API Key
- [ ] Histórico de arquivos processados com banco de dados
- [ ] Deploy com Docker
