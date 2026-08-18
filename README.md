# 📊 Arquitetura de Dados em People Analytics: Do Python ao Power BI

💻 Como visualizar o painel

Você pode interagir com o painel publicado através do link abaixo:

🔗 https://app.powerbi.com/view?r=eyJrIjoiNWQwMmQwN2UtNmQ0Mi00MTRmLTkzZjktZjY5NDhhZmM4NGU5IiwidCI6IjhlYjI5MjAxLWEyN2QtNDMwMi04NDczLWM5ODJlYjViZTkzNSJ9

## 📌 1. Visão Estratégica e Resumo do Projeto
A área de Recursos Humanos deixou de ser um departamento estritamente operacional para se tornar o núcleo estratégico das organizações. O grande desafio, no entanto, é transformar dados crus de departamento pessoal em inteligência de negócios acionável.

O objetivo deste projeto é construir uma **arquitetura de dados completa para People Analytics**, estruturada de ponta a ponta. 

Neste repositório, apresento a construção de um banco de dados transacional realista utilizando **Python**, a modelagem dessas informações em um *Star Schema* e, por fim, o cálculo de métricas de alta complexidade (Turnover, Absenteísmo e Retenção) utilizando **Power BI e DAX Avançado**. O foco é prover à diretoria e aos Business Partners (BPs) uma visão dinâmica do fluxo de talentos e da eficácia das políticas organizacionais.

---

## 🐍 2. Engenharia de Dados e Simulação com Python
O primeiro grande gargalo em projetos de People Analytics é garantir que a base de dados espelhe a complexidade do mundo real (histórico de admissões, proporção de desligamentos e frequência de atestados ao longo do tempo).

Para o desenvolvimento deste projeto, elaborei um script em Python focado em gerar, simular e tratar o banco de dados inicial. O diferencial deste script é a aplicação de regras de negócio lógicas para garantir a integridade referencial da modelagem antes mesmo dos dados chegarem ao Power BI.

### 🛠️ Tecnologias e Bibliotecas Utilizadas:
* **`Pandas` e `NumPy`:** Utilizadas para a estruturação dos DataFrames e aplicação de probabilidades estatísticas para geração de cenários (ex: taxa de turnover fixada em 20%, e distribuição probabilística de gênero baseada no mercado).
* **`Faker (pt_BR)`:** Geração de dados sintéticos e anonimizados, garantindo formatação realista para o cenário corporativo brasileiro (nomes completos e IDs únicos).
* **`Datetime` e `Random`:** Aplicação de lógica de tempo para garantir que as regras trabalhistas sejam respeitadas (ex: a data de desligamento nunca pode ser anterior à data de admissão).

### 🗃️ Inteligência da Base Gerada:
O script simula a operação de uma empresa com 300 colaboradores, gerando três arquivos fundamentais (`.csv`) estruturados para o modelo relacional:
1. **`dim_cargo.csv`:** Tabela dimensão mapeando a hierarquia estrutural (Departamentos e Cargos: Tecnologia, RH, Comercial e Financeiro).
2. **`dim_colaborador.csv`:** Tabela dimensão contendo os dados demográficos e o ciclo de vida do funcionário (Data de Admissão, Status de Atividade, Data de Desligamento e Salário Base).
3. **`fato_ausencias.csv`:** Tabela fato transacional que registra atestados, atrasos e faltas. A inteligência do script garante um grau de realismo onde **o volume de ausências é estritamente proporcional ao tempo de casa do colaborador**, e um funcionário só registra faltas no período exato em que esteve ativo na empresa.

---

## 📈 3. Visualização e Regras de Negócio no Power BI (DAX)
Com a base relacional estruturada, o foco no Power BI foi traduzir as regras complexas de Recursos Humanos e Legislação Trabalhista em métricas analíticas rápidas e à prova de erros de contexto temporal.

### 🗂️ Modelagem Star Schema
O projeto foi estruturado em um modelo relacional *Star Schema* clássico, garantindo alta performance de processamento e clareza analítica:
* **Dimensões:** `dCalendario` (Inteligência de tempo), `dim_colaborador` e `dim_cargo`.
* **Fato:** `fato_ausencias`.

### 🧠 Inteligência de Dados e DAX Avançado
Em vez de apresentar apenas números absolutos, o painel foi construído para resolver distorções analíticas comuns em People Analytics, utilizando DAX avançado para manipular contextos de filtro. 

Os principais desafios de negócio solucionados incluem:

* **Absenteísmo Dinâmico (Regra CLT 220h):** 
  Solucionou a distorção da taxa de faltas ao analisar períodos longos (ex: um ano inteiro). A medida desenvolvida calcula dinamicamente a amplitude do filtro de tempo na tela e ajusta a carga horária da empresa de forma proporcional, garantindo uma taxa real e acionável.
  * *Principais funções utilizadas:* `DATEDIFF`, `MIN`, `MAX`, `DIVIDE`.

* **Tempo de Casa Histórico (Quebra de Contexto):** 
  Desativou o relacionamento ativo do calendário para evitar que o filtro de datas isolasse apenas os recém-contratados. O cálculo varre todo o histórico da empresa para encontrar os funcionários ativos na data selecionada e extrair a média correta de retenção.
  * *Principais funções utilizadas:* `CALCULATE`, `REMOVEFILTERS`, `AVERAGEX`, `FILTER`.

* **Variações YoY (Year-over-Year) com Travas de Segurança:** 
  Criação de indicadores de performance (Headcount, Idade Média, Diversidade) que comparam o cenário atual com o ano anterior. Foram aplicadas regras de tratamento de exceção para evitar erros visuais (falsos positivos) quando o primeiro ano histórico da empresa é selecionado.
  * *Principais funções utilizadas:* `CALCULATE`, `DATEADD`, `ISBLANK`.
