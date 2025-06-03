# Aplicação de Análise ENADE - Universidade de Fortaleza

## Visão Geral

Esta aplicação web foi desenvolvida para análise dos microdados do ENADE da Universidade de Fortaleza, permitindo identificar gargalos e comparar o desempenho dos cursos com diferentes níveis (estado, região, país) e outras universidades.

## Funcionalidades Principais

### 1. Dashboard Interativo
- **Resumo Executivo**: Estatísticas gerais dos dados
- **Comparação por Níveis**: Gráficos comparativos entre UNIFOR, Ceará, Nordeste e Brasil
- **Performance por Dimensão**: Visualização radar das três dimensões do CPC
- **Distribuição de Cursos**: Gráfico de pizza com todos os cursos da UNIFOR

### 2. Análise por Área Específica
- Seleção de área de avaliação específica
- Comparação focada na área selecionada
- Análise de extremos (4 menores e 4 maiores valores por questão)

### 3. Dimensões Analisadas
Conforme a Nota Técnica nº 4/2023 do INEP:

#### Organização Didático-Pedagógica (NOC)
- Questões: Q27, Q29, Q30, Q31, Q33, Q34, Q35, Q36, Q37, Q38, Q42, Q49, Q56

#### Infraestrutura e Instalações Físicas (NFC)
- Questões: Q55, Q58, Q59, Q60, Q61, Q62, Q63, Q64, Q65, Q66, Q68

#### Oportunidades de Ampliação da Formação (NAC)
- Questões: Q43, Q44, Q45, Q46, Q47, Q52, Q53, Q67

### 4. Identificação de Gargalos
- Análise dos 4 menores valores por questão (identificação de pontos fracos)
- Análise dos 4 maiores valores por questão (identificação de benchmarks)
- Comparação com médias estaduais, regionais e nacionais

## Dados Analisados

### Cursos da Universidade de Fortaleza
1. ADMINISTRAÇÃO
2. CIÊNCIAS CONTÁBEIS
3. CIÊNCIAS ECONÔMICAS
4. DIREITO
5. JORNALISMO
6. PSICOLOGIA
7. PUBLICIDADE E PROPAGANDA
8. TECNOLOGIA EM DESIGN DE MODA
9. TECNOLOGIA EM GESTÃO FINANCEIRA
10. TECNOLOGIA EM MARKETING

### Comparações Disponíveis
- **UNIFOR**: Dados específicos da Universidade de Fortaleza
- **Ceará**: Média de todos os cursos do estado
- **Nordeste**: Média de todos os cursos da região
- **Brasil**: Média nacional

## Estrutura Técnica

### Backend (Flask)
- **API RESTful** com endpoints para:
  - `/api/enade/metadata` - Metadados da análise
  - `/api/enade/comparisons` - Comparações por área
  - `/api/enade/unifor-courses` - Dados dos cursos da UNIFOR
  - `/api/enade/extremes` - Análise de extremos
  - `/api/enade/dashboard-data` - Dados consolidados para dashboard

### Frontend
- **Interface responsiva** com HTML5, CSS3 e JavaScript
- **Gráficos interativos** usando Chart.js
- **Design moderno** com gradientes e efeitos visuais
- **Compatibilidade mobile** com design responsivo

### Processamento de Dados
- **Classe ENADEAnalyzer**: Processamento e análise dos microdados
- **Estruturação automática** das dimensões conforme nota técnica
- **Cálculos estatísticos** para comparações e rankings

## Como Usar

### 1. Visão Geral
- Acesse a aplicação para ver o dashboard principal
- Visualize as estatísticas gerais e comparações

### 2. Análise por Área
- Selecione uma área específica no dropdown
- Clique em "Atualizar Análise"
- Visualize a análise de extremos para a área selecionada

### 3. Interpretação dos Resultados
- **Valores maiores** indicam melhor desempenho
- **Diferenças positivas** vs Brasil indicam performance superior
- **Análise de extremos** identifica instituições com melhor e pior desempenho

## Insights Principais

### Performance Geral da UNIFOR
- **Organização Didático-Pedagógica**: 5.646 (superior à média nacional: 5.258)
- **Infraestrutura e Instalações**: 5.763 (superior à média nacional: 5.180)
- **Oportunidades de Ampliação**: 5.507 (superior à média nacional: 4.532)
- **Média Geral**: 5.649 (superior à média nacional: 5.071)

### Pontos Fortes
- A UNIFOR supera consistentemente as médias estaduais, regionais e nacionais
- Melhor performance na dimensão de Infraestrutura e Instalações
- Forte desempenho em Oportunidades de Ampliação da Formação

### Áreas de Atenção
- Monitoramento contínuo das questões com menores valores
- Benchmarking com instituições de melhor desempenho
- Foco nas dimensões com menor diferencial competitivo

## Arquivos Principais

```
enade_analyzer_app/
├── src/
│   ├── main.py                 # Aplicação Flask principal
│   ├── enade_analyzer.py       # Classe de análise dos dados
│   ├── web_data.json          # Dados pré-processados
│   ├── routes/
│   │   └── enade.py           # Rotas da API
│   └── static/
│       ├── index.html         # Interface principal
│       └── app.js             # JavaScript da aplicação
├── requirements.txt           # Dependências Python
└── README.md                 # Esta documentação
```

## Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **Flask** - Framework web
- **Pandas** - Processamento de dados
- **Chart.js** - Visualizações interativas
- **HTML5/CSS3/JavaScript** - Frontend moderno

## Conclusão

Esta aplicação fornece uma ferramenta completa para análise dos dados do ENADE da Universidade de Fortaleza, permitindo:

1. **Identificação de gargalos** através da análise de extremos
2. **Comparações contextualizadas** com diferentes níveis geográficos
3. **Visualizações intuitivas** para tomada de decisão
4. **Análise por dimensões** conforme metodologia oficial do INEP

A ferramenta está pronta para uso e pode ser facilmente expandida para incluir novos dados ou funcionalidades conforme necessário.

