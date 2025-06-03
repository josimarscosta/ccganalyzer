# Deploy Rápido no Render - Resumo

## 🚀 Passos Essenciais

### 1. GitHub (5 minutos)
1. Crie um repositório no GitHub
2. Faça upload de todos os arquivos da aplicação
3. Certifique-se que os arquivos estão na raiz do repositório

### 2. Render (10 minutos)
1. Acesse [render.com](https://render.com)
2. Conecte com GitHub
3. Crie "New Web Service"
4. Selecione seu repositório

### 3. Configurações no Render
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT src.main:app
Python Version: 3.11.0
```

### 4. Variáveis de Ambiente
```
FLASK_ENV = production
PYTHONPATH = /opt/render/project/repo
```

### 5. Deploy
- Clique em "Create Web Service"
- Aguarde 5-10 minutos
- Sua aplicação estará online!

## ⚡ Arquivos Importantes Incluídos

✅ `Procfile` - Configuração do servidor  
✅ `runtime.txt` - Versão do Python  
✅ `requirements.txt` - Dependências (com gunicorn)  
✅ `main.py` - Modificado para produção  

## 🔗 Resultado

Sua aplicação ficará disponível em:
`https://[nome-do-seu-app].onrender.com`

## 💡 Dicas

- **Plano Free**: 750 horas/mês grátis
- **Sleep**: App "dorme" após 15min sem uso
- **Wake-up**: Primeiro acesso pode demorar 30s
- **Logs**: Monitore no dashboard do Render

## 🆘 Problemas Comuns

**Build falha?** → Verifique requirements.txt  
**App não inicia?** → Confirme o Start Command  
**Dados não carregam?** → Verifique se web_data.json está no repo  

📖 **Guia completo**: Veja DEPLOY_RENDER.md

