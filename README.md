# Sistema de Acompanhamento de TPV e Markup

Este repositório contém um **exemplo** de sistema para acompanhar indicadores
financeiros como **TPV (Total Payment Volume)** e **markup** de vários
clientes.  A solução utiliza Python, a biblioteca Pandas para ler e
processar planilhas de Excel/CSV e Plotly para construir gráficos
interativos.

## Motivação

Ao trabalhar com várias planilhas que contêm valores de TPV e markup,
é comum precisar de um método estruturado para:

* **Consolidar dados** de múltiplas planilhas num único conjunto de dados.
* **Calcular métricas** como soma de TPV por cliente, média de markup
  ou variações ao longo do tempo.
* **Visualizar tendências** de forma intuitiva e interativa para
  facilitar o acompanhamento dos resultados.

O `pandas` é uma das bibliotecas mais populares no ecossistema Python
para manipulação e análise de dados.  Conforme explica um artigo da
Rockeseat, o DataFrame é uma estrutura de dados bidimensional (como
uma planilha) e o pandas facilita a leitura de dados de arquivos CSV,
Excel, bancos de dados e outras fontes【478079940494884†L61-L65】.  Após
carregar os dados, é possível limpá-los, organizar e filtrar o
conjunto para analisar apenas as informações relevantes【478079940494884†L89-L117】.
Os scripts deste repositório utilizam essas funcionalidades para
consolidar e analisar os dados.

Além disso, recomenda‑se armazenar dados em formatos baseados em
texto, como CSV, e usar sistemas de controle de versão como Git para
acompanhar as alterações.  Um artigo do iMasters explica que
controlar versões de dados permite colaboração descentralizada,
rastreamento da origem das alterações e sincronização eficiente dos
arquivos【490708602298591†L61-L83】.  O mesmo artigo sugere guardar
conjuntos de dados como CSV e incluir os scripts de processamento no
mesmo repositório【490708602298591†L106-L132】.

Para criar dashboards interativos, a biblioteca Plotly é uma boa
opção.  Plotly é uma biblioteca de código aberto voltada para
visualizações interativas; ela permite explorar os dados com zoom e
outros recursos, enquanto a interatividade é gerenciada em
JavaScript para que possamos focar em escrever o código em
Python【51578518484915†L27-L33】.

## Estrutura do Projeto

```
tpv_markup_dashboard/
├── data/                # Local onde as planilhas devem ser colocadas
├── reports/             # Saída dos gráficos e relatórios gerados
├── src/
│   ├── process_data.py  # Script principal de processamento e geração de gráficos
│   └── utils.py         # Funções auxiliares (agregações etc.)
└── README.md            # Este arquivo de instruções
```

* **`data/`** – Coloque aqui as suas planilhas em formato `.xlsx` ou `.csv`.
  Para melhor controle de versão no GitHub, recomenda‑se converter
  arquivos grandes de Excel para CSV antes de enviar para o repositório.
* **`reports/`** – Após executar o script, os relatórios e
  gráficos serão exportados para esta pasta em formato HTML.
* **`src/process_data.py`** – Script principal que lê os arquivos da
  pasta `data/`, consolida os dados, calcula métricas de TPV e markup
  e gera gráficos interativos usando Plotly.
* **`src/utils.py`** – Funções auxiliares usadas pelo script principal.

## Pré-requisitos

* Python 3.8 ou superior
* Pacotes Python:
  - `pandas` (para manipulação de dados)
  - `openpyxl` (para leitura de arquivos Excel `.xlsx`)
  - `plotly` (para gráficos interativos)

Para instalar as dependências, execute:

```bash
pip install pandas openpyxl plotly
```

## Utilização

1. Clone ou faça download deste repositório e coloque suas planilhas na
   pasta `data/`.  Cada planilha deve ter, no mínimo, as colunas
   `Cliente`, `TPV`, `Markup` e `Data` (esta última opcional para
   análise temporal).  O script aceita arquivos CSV ou Excel (`.xlsx`).

2. Abra um terminal na raiz do repositório e execute o script de
   processamento:

```bash
python src/process_data.py
```

3. O script irá consolidar todas as planilhas da pasta `data/` em um
   DataFrame único, realizar cálculos de soma e média de TPV e
   markup por cliente e gerar gráficos interativos.  Os arquivos
   HTML serão salvos na pasta `reports/`.  Basta abrir um deles no
   navegador para visualizar os resultados.

4. Opcional: você pode personalizar os gráficos ou adicionar novas
   métricas editando o código em `src/process_data.py`.  É
   recomendável versionar suas alterações no GitHub para acompanhar
   a evolução do projeto e permitir colaboração【490708602298591†L61-L83】.

## Próximos Passos

* Integrar o script a um _GitHub Actions_ para gerar relatórios
  automaticamente sempre que novas planilhas forem adicionadas.
* Usar o GitHub Pages para publicar os relatórios interativos
  diretamente na web.
* Expandir as análises, incluindo gráficos temporais de TPV/markup
  por período e indicadores personalizados conforme necessidade.

## Licença

Este projeto é apenas um exemplo e não possui restrições de uso.
Sinta‑se livre para adaptá‑lo às suas necessidades.
