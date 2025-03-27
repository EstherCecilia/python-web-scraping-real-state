# 🏠 Web Scraper de Imóveis - Documentação

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📌 Visão Geral
Scraper para extração automatizada de dados de portais imobiliários, com tratamento de dados e exportação em múltiplos formatos.

## 🚀 Começando
### Pré-requisitos
- Python 3.8+
- Gerenciador de pacotes pip
- Navegador Chrome/Firefox (para versão com Selenium)

### 📥 Instalação
1. Clonar repositório:

```sh
git clone https://github.com/seu-usuario/imoveis-scraper.git
cd imoveis-scraper
```
2. Ambiente Virtual (Recomendado):

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

3. Instalar dependências:

```sh
pip install -r requirements.txt
```

## 🏃 Execução
Modo básico:

```sh
python main.py
```

##  🗃️ Estrutura do Projeto
```sh
.
├── .github/
│   └── workflows/       # CI/CD
├── output/                # Dados de saída
├── models/
│   ├── analytics
│   ├── process
│   ├── realstate
├── requirements.txt     # Dependências
└── main.py              # Ponto de entrada
```

##  📊 Saída de Dados
Exemplo de dados coletados:

Bairro	| Rua	| Área | Quartos | Banheiros | Vagas	| Preço
------- | --- | ---- | ------- | --------- | ------ | ------
Califórnia | José Cláudio Sanches | 53m² | 2 | 1 | 1 | 190000
Nova Gameleira | Cândido de Souza | 55m² | 3 | 2 | 1 | 237000

Formatos suportados:
- CSV (padrão)
- JSON
- SQLite

##  🤝 Contribuição
1. Reporte issues no GitHub
2. Faça fork do projeto
3. Crie sua branch (git checkout -b feature/nova-feature)
4. Commit suas mudanças (git commit -m 'Add some feature')
5. Push para a branch (git push origin feature/nova-feature)
6. Abra um Pull Request

