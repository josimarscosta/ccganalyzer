# Instruções de Instalação e Uso

## Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Navegue até o diretório da aplicação
```bash
cd enade_analyzer_app
```

### 2. Ative o ambiente virtual
```bash
source venv/bin/activate
```

### 3. Instale as dependências (se necessário)
```bash
pip install -r requirements.txt
```

## Execução

### 1. Inicie a aplicação
```bash
python src/main.py
```

### 2. Acesse no navegador
Abra seu navegador e acesse: `http://localhost:5000`

## Uso da Aplicação

### Dashboard Principal
1. **Visão Geral**: Visualize estatísticas gerais e comparações
2. **Gráficos Interativos**: Explore os dados através de visualizações

### Análise por Área
1. **Selecione uma área**: Use o dropdown "Área de Avaliação"
2. **Clique em "Atualizar Análise"**: Carregue dados específicos da área
3. **Visualize extremos**: Analise os 4 menores e maiores valores

### Interpretação dos Dados
- **Escala**: Valores de 1 a 6 (quanto maior, melhor)
- **Cores**: Verde para valores altos, vermelho para baixos
- **Comparações**: UNIFOR vs Ceará vs Nordeste vs Brasil

## Estrutura dos Dados

### Dimensões Analisadas
1. **NOC**: Organização Didático-Pedagógica
2. **NFC**: Infraestrutura e Instalações Físicas
3. **NAC**: Oportunidades de Ampliação da Formação

### Questões por Dimensão
- **NOC**: Q27, Q29, Q30, Q31, Q33, Q34, Q35, Q36, Q37, Q38, Q42, Q49, Q56
- **NFC**: Q55, Q58, Q59, Q60, Q61, Q62, Q63, Q64, Q65, Q66, Q68
- **NAC**: Q43, Q44, Q45, Q46, Q47, Q52, Q53, Q67

## Solução de Problemas

### Erro de Módulo Não Encontrado
```bash
pip install pandas openpyxl numpy flask
```

### Porta em Uso
Se a porta 5000 estiver em uso, modifique em `src/main.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Dados Não Carregam
Verifique se os arquivos estão presentes:
- `src/web_data.json`
- `src/ResumoQuestionário.xlsx`

## Contato e Suporte

Para dúvidas ou problemas, verifique:
1. Se todas as dependências estão instaladas
2. Se os arquivos de dados estão no local correto
3. Se a porta 5000 está disponível

## Próximos Passos

### Possíveis Melhorias
1. **Exportação de Relatórios**: PDF, Excel
2. **Filtros Avançados**: Por ano, modalidade
3. **Comparações Personalizadas**: Selecionar universidades específicas
4. **Alertas Automáticos**: Identificação de tendências

### Atualização de Dados
Para atualizar com novos dados do ENADE:
1. Substitua o arquivo `ResumoQuestionário.xlsx`
2. Execute `python src/generate_web_data.py`
3. Reinicie a aplicação

