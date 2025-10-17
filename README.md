# The Ads Project (modular monolith)

Estrutura base para uma plataforma unificada de Ads Insights, modular e extensível.
Sem dependência de APIs externas reais — pronto para usar mocks e Databricks.

## Estrutura
```
app/
  backend/
    core/          # config, logging
    domain/        # ports e DTOs
    adapters/      # connectors e warehouse
    application/   # casos de uso
    routers/       # FastAPI endpoints
```

## Rodar
```bash
cd app/backend
uvicorn main:app --reload
```
