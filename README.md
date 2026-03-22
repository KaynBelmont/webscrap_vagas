# 🕷️ Webscrap Vagas — Coletor e Dashboard de Vagas de Emprego

Sistema de Web Scraping desenvolvido em **Python** para coletar, estruturar e visualizar vagas de emprego do **Vagas.com.br**. Os dados são extraídos automaticamente, exportados para **CSV** via Pandas e exibidos em um **dashboard interativo** hospedado no Streamlit Cloud.

---

## 📁 Arquivos

| Arquivo | Descrição |
|---|---|
| [`main.py`](./main.py) | Ponto de entrada — orquestra o scraper, parser e exporter |
| [`dashboard.py`](./dashboard.py) | Dashboard interativo com filtros e gráficos via Streamlit |
| [`src/scraper.py`](./src/scraper.py) | Requisições HTTP ao Vagas.com.br |
| [`src/parser.py`](./src/parser.py) | Extração dos dados via BeautifulSoup |
| [`src/exporter.py`](./src/exporter.py) | Estruturação com Pandas e exportação para CSV |
| [`data/vagas.csv`](./data/vagas.csv) | Arquivo de saída com as vagas coletadas |
| [`requirements.txt`](./requirements.txt) | Dependências do projeto |

---

## 🏗️ Arquitetura

```
main.py
  │
  ├── src/scraper.py
  │     └── requests.get() → HTML bruto da página
  │
  ├── src/parser.py
  │     └── BeautifulSoup → extrai título, empresa, local, nível, link
  │
  └── src/exporter.py
        └── pandas.DataFrame → exporta data/vagas.csv

dashboard.py
  └── streamlit + pandas
        ├── Lê data/vagas.csv
        ├── Filtros: nível, localidade, busca textual
        ├── Métricas: total de vagas, empresas, localidades
        ├── Gráfico: vagas por nível
        ├── Gráfico: top 10 localidades
        └── Tabela interativa com links clicáveis
```

---

## 📋 Módulos

### 1. `src/scraper.py`

Responsável por realizar a requisição HTTP ao Vagas.com.br e retornar o HTML bruto de cada página de resultados.

**Fluxo:**

```
buscar_pagina(termo, pagina)
  → Monta URL: vagas.com.br/vagas-de-{termo}?pagina={pagina}
  → requests.get() com headers de navegador real
  → raise_for_status() — valida resposta HTTP
  → Retorna HTML bruto (str)
```

**Detalhe técnico:**
- Utiliza `User-Agent` customizado nos headers para simular um navegador real e evitar bloqueios por bot detection
- Timeout de 10 segundos por requisição

---

### 2. `src/parser.py`

Responsável por navegar o HTML e extrair os dados estruturados de cada card de vaga.

**Fluxo:**

```
extrair_vagas(html)
  → BeautifulSoup(html, "lxml")
  → find_all("li", class_="vaga") → lista de cards
  → Para cada card:
        ├── Título   → a.link-detalhes-vaga [atributo title]
        ├── Empresa  → span.emprVaga
        ├── Local    → span.vaga-local (remove ícone SVG)
        ├── Nível    → span.nivelVaga
        └── Link     → vagas.com.br + href
  → Retorna list[dict]
```

**Seletores CSS mapeados por inspeção manual do HTML:**

| Campo | Tag | Classe / Atributo |
|---|---|---|
| Título | `<a>` | `class="link-detalhes-vaga"` → `title` |
| Empresa | `<span>` | `class="emprVaga"` |
| Localidade | `<span>` | `class="vaga-local"` |
| Nível | `<span>` | `class="nivelVaga"` |
| Link | `<a>` | `class="link-detalhes-vaga"` → `href` |

---

### 3. `src/exporter.py`

Responsável por estruturar os dados em um DataFrame Pandas e exportar para CSV.

**Fluxo:**

```
exportar_csv(vagas, caminho)
  → pd.DataFrame(vagas)
  → drop_duplicates() — remove duplicatas
  → replace("N/A", "") — limpa valores ausentes
  → to_csv(encoding="utf-8-sig") — suporte a acentos
  → Cria pasta data/ automaticamente se não existir
```

**Por que `utf-8-sig`?**
Encoding com BOM (Byte Order Mark) — garante que acentos e caracteres especiais sejam exibidos corretamente ao abrir o CSV no Excel ou Google Sheets.

---

### 4. `main.py`

Ponto de entrada do projeto. Orquestra os três módulos acima em sequência.

**Configurações ajustáveis:**

```python
TERMO_BUSCA   = "python"         # Termo pesquisado no Vagas.com.br
TOTAL_PAGINAS = 3                # Páginas coletadas (~40 vagas por página)
ARQUIVO_CSV   = "data/vagas.csv"
```

---

### 5. `dashboard.py`

Dashboard interativo construído com Streamlit. Lê o CSV gerado e exibe os dados com filtros, métricas e gráficos.

**Recursos:**

| Recurso | Descrição |
|---|---|
| Métricas | Total de vagas, empresas únicas, localidades únicas |
| Filtro por nível | Selectbox: Todos / Júnior / Pleno / Sênior / etc. |
| Filtro por localidade | Selectbox com todas as localidades coletadas |
| Busca textual | Filtra por título ou nome da empresa |
| Gráfico de níveis | Bar chart com distribuição por senioridade |
| Top 10 localidades | Bar chart com as localidades mais frequentes |
| Tabela de vagas | Tabela HTML com links clicáveis para cada vaga |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|---|---|---|
| `requests` | 2.32.x | Requisições HTTP |
| `beautifulsoup4` | 4.14.x | Parsing e extração do HTML |
| `lxml` | 6.x | Parser HTML de alta performance |
| `pandas` | 3.x | Estruturação e exportação dos dados |
| `streamlit` | latest | Dashboard interativo e deploy |

---

## ⚙️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/webscrap_vagas.git
cd webscrap_vagas
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o scraper

```bash
python main.py
```

O arquivo `data/vagas.csv` será gerado automaticamente ao final da execução.

### 5. Abra o dashboard

```bash
streamlit run dashboard.py
```

Acesse `http://localhost:8501` no navegador.

---

## 🌐 Deploy — Streamlit Cloud

O dashboard está hospedado gratuitamente no **Streamlit Community Cloud**.

🔗 **Acesse aqui:** [webscrapvagas.streamlit.app](https://webscrapvagas-pksan5w7gfbtnzjqmxjxxe.streamlit.app/)

### Como o deploy funciona

O Streamlit Cloud conecta diretamente ao repositório GitHub. Qualquer `git push` na branch `main` atualiza o app automaticamente — sem nenhuma etapa manual de redeploy.

### Como atualizar os dados

```bash
python main.py                        # coleta novas vagas
git add data/vagas.csv
git commit -m "data: atualiza vagas coletadas"
git push
```

O dashboard reflete os novos dados em segundos após o push.

---

## 📊 Exemplo de Saída

```
=======================================================
   Vagas Scraper — Vagas.com.br
=======================================================
[main] Coletando página 1 de 3...
[scraper] Buscando: https://www.vagas.com.br/vagas-de-python?pagina=1
[scraper] Status: 200 — OK!
[parser] 40 vagas encontradas na página
[main] Coletando página 2 de 3...
[scraper] Buscando: https://www.vagas.com.br/vagas-de-python?pagina=2
[scraper] Status: 200 — OK!
[parser] 25 vagas encontradas na página
[main] Total coletado: 65 vagas
[exporter] 65 vagas exportadas para 'data/vagas.csv'
=======================================================
   Coleta finalizada com sucesso!
=======================================================
```

---

## ⚠️ Aviso Legal

Este projeto foi desenvolvido exclusivamente para fins educacionais e de portfólio.
O uso deve respeitar os [Termos de Uso](https://www.vagas.com.br) do Vagas.com.br e as boas práticas de Web Scraping, incluindo o respeito ao arquivo `robots.txt` e ausência de sobrecarga nos servidores.

---

## 👨‍💻 Autor

Desenvolvido como projeto de portfólio para aprendizado de Web Scraping, manipulação de dados e deploy de dashboards com Python.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](# 🕷️ Webscrap Vagas — Coletor e Dashboard de Vagas de Emprego

Sistema de Web Scraping desenvolvido em **Python** para coletar, estruturar e visualizar vagas de emprego do **Vagas.com.br**. Os dados são extraídos automaticamente, exportados para **CSV** via Pandas e exibidos em um **dashboard interativo** hospedado no Streamlit Cloud.

---

## 📁 Arquivos

| Arquivo | Descrição |
|---|---|
| [`main.py`](./main.py) | Ponto de entrada — orquestra o scraper, parser e exporter |
| [`dashboard.py`](./dashboard.py) | Dashboard interativo com filtros e gráficos via Streamlit |
| [`src/scraper.py`](./src/scraper.py) | Requisições HTTP ao Vagas.com.br |
| [`src/parser.py`](./src/parser.py) | Extração dos dados via BeautifulSoup |
| [`src/exporter.py`](./src/exporter.py) | Estruturação com Pandas e exportação para CSV |
| [`data/vagas.csv`](./data/vagas.csv) | Arquivo de saída com as vagas coletadas |
| [`requirements.txt`](./requirements.txt) | Dependências do projeto |

---

## 🏗️ Arquitetura

```
main.py
  │
  ├── src/scraper.py
  │     └── requests.get() → HTML bruto da página
  │
  ├── src/parser.py
  │     └── BeautifulSoup → extrai título, empresa, local, nível, link
  │
  └── src/exporter.py
        └── pandas.DataFrame → exporta data/vagas.csv

dashboard.py
  └── streamlit + pandas
        ├── Lê data/vagas.csv
        ├── Filtros: nível, localidade, busca textual
        ├── Métricas: total de vagas, empresas, localidades
        ├── Gráfico: vagas por nível
        ├── Gráfico: top 10 localidades
        └── Tabela interativa com links clicáveis
```

---

## 📋 Módulos

### 1. `src/scraper.py`

Responsável por realizar a requisição HTTP ao Vagas.com.br e retornar o HTML bruto de cada página de resultados.

**Fluxo:**

```
buscar_pagina(termo, pagina)
  → Monta URL: vagas.com.br/vagas-de-{termo}?pagina={pagina}
  → requests.get() com headers de navegador real
  → raise_for_status() — valida resposta HTTP
  → Retorna HTML bruto (str)
```

**Detalhe técnico:**
- Utiliza `User-Agent` customizado nos headers para simular um navegador real e evitar bloqueios por bot detection
- Timeout de 10 segundos por requisição

---

### 2. `src/parser.py`

Responsável por navegar o HTML e extrair os dados estruturados de cada card de vaga.

**Fluxo:**

```
extrair_vagas(html)
  → BeautifulSoup(html, "lxml")
  → find_all("li", class_="vaga") → lista de cards
  → Para cada card:
        ├── Título   → a.link-detalhes-vaga [atributo title]
        ├── Empresa  → span.emprVaga
        ├── Local    → span.vaga-local (remove ícone SVG)
        ├── Nível    → span.nivelVaga
        └── Link     → vagas.com.br + href
  → Retorna list[dict]
```

**Seletores CSS mapeados por inspeção manual do HTML:**

| Campo | Tag | Classe / Atributo |
|---|---|---|
| Título | `<a>` | `class="link-detalhes-vaga"` → `title` |
| Empresa | `<span>` | `class="emprVaga"` |
| Localidade | `<span>` | `class="vaga-local"` |
| Nível | `<span>` | `class="nivelVaga"` |
| Link | `<a>` | `class="link-detalhes-vaga"` → `href` |

---

### 3. `src/exporter.py`

Responsável por estruturar os dados em um DataFrame Pandas e exportar para CSV.

**Fluxo:**

```
exportar_csv(vagas, caminho)
  → pd.DataFrame(vagas)
  → drop_duplicates() — remove duplicatas
  → replace("N/A", "") — limpa valores ausentes
  → to_csv(encoding="utf-8-sig") — suporte a acentos
  → Cria pasta data/ automaticamente se não existir
```

**Por que `utf-8-sig`?**
Encoding com BOM (Byte Order Mark) — garante que acentos e caracteres especiais sejam exibidos corretamente ao abrir o CSV no Excel ou Google Sheets.

---

### 4. `main.py`

Ponto de entrada do projeto. Orquestra os três módulos acima em sequência.

**Configurações ajustáveis:**

```python
TERMO_BUSCA   = "python"         # Termo pesquisado no Vagas.com.br
TOTAL_PAGINAS = 3                # Páginas coletadas (~40 vagas por página)
ARQUIVO_CSV   = "data/vagas.csv"
```

---

### 5. `dashboard.py`

Dashboard interativo construído com Streamlit. Lê o CSV gerado e exibe os dados com filtros, métricas e gráficos.

**Recursos:**

| Recurso | Descrição |
|---|---|
| Métricas | Total de vagas, empresas únicas, localidades únicas |
| Filtro por nível | Selectbox: Todos / Júnior / Pleno / Sênior / etc. |
| Filtro por localidade | Selectbox com todas as localidades coletadas |
| Busca textual | Filtra por título ou nome da empresa |
| Gráfico de níveis | Bar chart com distribuição por senioridade |
| Top 10 localidades | Bar chart com as localidades mais frequentes |
| Tabela de vagas | Tabela HTML com links clicáveis para cada vaga |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|---|---|---|
| `requests` | 2.32.x | Requisições HTTP |
| `beautifulsoup4` | 4.14.x | Parsing e extração do HTML |
| `lxml` | 6.x | Parser HTML de alta performance |
| `pandas` | 3.x | Estruturação e exportação dos dados |
| `streamlit` | latest | Dashboard interativo e deploy |

---

## ⚙️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/webscrap_vagas.git
cd webscrap_vagas
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o scraper

```bash
python main.py
```

O arquivo `data/vagas.csv` será gerado automaticamente ao final da execução.

### 5. Abra o dashboard

```bash
streamlit run dashboard.py
```

Acesse `http://localhost:8501` no navegador.

---

## 🌐 Deploy — Streamlit Cloud

O dashboard está hospedado gratuitamente no **Streamlit Community Cloud**.

🔗 **Acesse aqui:** [webscrapvagas.streamlit.app](https://webscrapvagas-pksan5w7gfbtnzjqmxjxxe.streamlit.app/)

### Como o deploy funciona

O Streamlit Cloud conecta diretamente ao repositório GitHub. Qualquer `git push` na branch `main` atualiza o app automaticamente — sem nenhuma etapa manual de redeploy.

### Como atualizar os dados

```bash
python main.py                        # coleta novas vagas
git add data/vagas.csv
git commit -m "data: atualiza vagas coletadas"
git push
```

O dashboard reflete os novos dados em segundos após o push.

---

## 📊 Exemplo de Saída

```
=======================================================
   Vagas Scraper — Vagas.com.br
=======================================================
[main] Coletando página 1 de 3...
[scraper] Buscando: https://www.vagas.com.br/vagas-de-python?pagina=1
[scraper] Status: 200 — OK!
[parser] 40 vagas encontradas na página
[main] Coletando página 2 de 3...
[scraper] Buscando: https://www.vagas.com.br/vagas-de-python?pagina=2
[scraper] Status: 200 — OK!
[parser] 25 vagas encontradas na página
[main] Total coletado: 65 vagas
[exporter] 65 vagas exportadas para 'data/vagas.csv'
=======================================================
   Coleta finalizada com sucesso!
=======================================================
```

---

## ⚠️ Aviso Legal

Este projeto foi desenvolvido exclusivamente para fins educacionais e de portfólio.
O uso deve respeitar os [Termos de Uso](https://www.vagas.com.br) do Vagas.com.br e as boas práticas de Web Scraping, incluindo o respeito ao arquivo `robots.txt` e ausência de sobrecarga nos servidores.
