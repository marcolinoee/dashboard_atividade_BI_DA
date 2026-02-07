# Dashboard de Análise de E-Commerce (Olist)

Este projeto consiste em um dashboard interativo de **Business Intelligence** desenvolvido com Python e Streamlit. Ele utiliza dados reais do comércio eletrônico brasileiro (Olist) para fornecer uma visão gerencial sobre vendas, performance logística e comportamento do consumidor.

# Objetivo do Projeto
O objetivo principal é transformar dados brutos relacionais em informações estratégicas, permitindo o monitoramento de:
- **Evolução do Faturamento:** Análise temporal das vendas.
- **Performance Regional:** Distribuição de vendas por estados.
- **Top Produtos:** Identificação das categorias mais rentáveis.
- **KPIs:** Métricas essenciais como Ticket Médio e Total de Pedidos.

# Funcionalidades
- **KPIs em Tempo Real:** Visualização instantânea de Faturamento Total, Quantidade de Pedidos e Ticket Médio baseada nos filtros ativos.
- **Filtros Dinâmicos:** Barra lateral para segmentação por **Ano** e **Estado (UF)**.
- **Gráficos Interativos (Plotly):**
  - Linha do tempo de faturamento mensal.
  - Ranking (Gráfico de Barras) das 10 categorias de produtos mais vendidas.
- **Otimização:** Uso de cache (`@st.cache_data`) para carregamento eficiente de dados.

# Tecnologias Utilizadas
- **Linguagem:** Python
- **ETL e Manipulação de Dados:** Pandas
- **Frontend / Dashboard:** Streamlit
- **Visualização de Dados:** Plotly Express

# Estrutura de Arquivos
```text
.
├── app.py                # Aplicação principal (Dashboard)
├── dados_vendas.csv      # Base de dados tratada (Tabela Única Analítica)
├── requirements.txt      # Lista de dependências do projeto
└── README.md             # Documentação do projeto# dashboard_atividade_BI_DA
