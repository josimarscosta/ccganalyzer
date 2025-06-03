# Deploy no Render - Aplicação ENADE UNIFOR

## Pré-requisitos
- Conta no GitHub
- Conta no Render (render.com)
- Código da aplicação em um repositório GitHub

## Passo 1: Preparar o Repositório GitHub

### 1.1 Criar Repositório
1. Acesse [GitHub](https://github.com)
2. Clique em "New repository"
3. Nome: `enade-unifor-analyzer`
4. Marque como "Public" ou "Private"
5. Clique em "Create repository"

### 1.2 Fazer Upload dos Arquivos
1. **Opção A - Via GitHub Web:**
   - Clique em "uploading an existing file"
   - Arraste todos os arquivos da pasta `enade_analyzer_app`
   - Commit as mudanças

2. **Opção B - Via Git (se tiver instalado):**
   ```bash
   git clone [URL_DO_SEU_REPOSITORIO]
   cd enade-unifor-analyzer
   # Copie todos os arquivos da pasta enade_analyzer_app para aqui
   git add .
   git commit -m "Aplicação ENADE UNIFOR"
   git push origin main
   ```

## Passo 2: Deploy no Render

### 2.1 Criar Conta no Render
1. Acesse [render.com](https://render.com)
2. Clique em "Get Started for Free"
3. Conecte com sua conta GitHub

### 2.2 Criar Web Service
1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório `enade-unifor-analyzer`

### 2.3 Configurar o Deploy
Preencha as configurações:

**Configurações Básicas:**
- **Name**: `enade-unifor-analyzer`
- **Region**: `Oregon (US West)` ou mais próximo
- **Branch**: `main`
- **Root Directory**: deixe vazio
- **Runtime**: `Python 3`

**Configurações de Build:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`

**Configurações Avançadas:**
- **Python Version**: `3.11.0`
- **Auto-Deploy**: `Yes` (para deploy automático)

### 2.4 Variáveis de Ambiente
Adicione as seguintes variáveis de ambiente:
- **FLASK_ENV**: `production`
- **PYTHONPATH**: `/opt/render/project/repo`

### 2.5 Finalizar Deploy
1. Clique em "Create Web Service"
2. Aguarde o build (pode levar 5-10 minutos)
3. Sua aplicação estará disponível em: `https://enade-unifor-analyzer.onrender.com`

## Passo 3: Verificar o Deploy

### 3.1 Logs de Build
- Monitore os logs durante o build
- Verifique se não há erros de dependências

### 3.2 Testar a Aplicação
1. Acesse a URL fornecida pelo Render
2. Teste todas as funcionalidades:
   - Dashboard principal
   - Seleção de áreas
   - Análise de extremos
   - Gráficos interativos

## Estrutura de Arquivos Necessária

Certifique-se de que seu repositório tenha esta estrutura:

```
enade-unifor-analyzer/
├── src/
│   ├── main.py
│   ├── enade_analyzer.py
│   ├── web_data.json
│   ├── ResumoQuestionário.xlsx
│   ├── routes/
│   │   ├── enade.py
│   │   └── user.py
│   ├── models/
│   │   └── user.py
│   └── static/
│       ├── index.html
│       └── app.js
├── requirements.txt
├── Procfile
├── runtime.txt
├── README.md
└── INSTALACAO.md
```

## Solução de Problemas

### Erro de Build
- Verifique se `requirements.txt` está correto
- Confirme se `gunicorn` está listado nas dependências

### Erro de Start
- Verifique se o comando start está correto: `gunicorn --bind 0.0.0.0:$PORT src.main:app`
- Confirme se o arquivo `src/main.py` existe

### Aplicação não Carrega
- Verifique os logs no dashboard do Render
- Confirme se os arquivos de dados estão no repositório

### Timeout de Build
- O Render tem limite de 15 minutos para build
- Se necessário, otimize as dependências

## Configurações Opcionais

### Custom Domain
1. No dashboard do Render, vá em "Settings"
2. Clique em "Custom Domains"
3. Adicione seu domínio personalizado

### Monitoramento
- O Render fornece métricas básicas gratuitamente
- Configure alertas para downtime

### Backup
- Mantenha o código sempre atualizado no GitHub
- Faça backup dos dados regularmente

## Custos

**Plano Free do Render:**
- 750 horas/mês gratuitas
- Sleep após 15 minutos de inatividade
- Adequado para demonstrações e testes

**Plano Paid (se necessário):**
- Sem sleep automático
- Mais recursos de CPU/RAM
- A partir de $7/mês

## Atualizações

Para atualizar a aplicação:
1. Faça as mudanças no código local
2. Commit e push para o GitHub
3. O Render fará deploy automático (se configurado)

## Suporte

Em caso de problemas:
1. Verifique os logs no dashboard do Render
2. Consulte a documentação: [render.com/docs](https://render.com/docs)
3. Verifique se todos os arquivos estão no repositório GitHub

