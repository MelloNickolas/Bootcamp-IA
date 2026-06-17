"""API do agente de marketing da Virtuau Modas.

É a "portinha" que liga o site (React) ao cérebro (marketing.py). Expõe os
endpoints que a tela consome para mostrar o calendário de datas, as sugestões
de post e as ideias "coringa".

Rodar:  ./.venv/Scripts/python.exe -m uvicorn backend.api:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import marketing

app = FastAPI(title="Virtuau Marketing API", version="1.0")

# Libera o acesso a partir do site React (rodando em outra porta, no navegador)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {"status": "ok", "marca": marketing.MARCA["nome"]}


@app.get("/marca")
def marca():
    """Identidade da marca (nome, cidade, vibe, slogan)."""
    return marketing.MARCA


@app.get("/ocasioes")
def ocasioes(dias: int = 120):
    """Próximas datas comemorativas/estações com sugestão de post."""
    return marketing.proximas_ocasioes(dias=dias)


@app.get("/sugestao-livre")
def sugestao_livre():
    """Uma ideia de post 'coringa' para qualquer dia."""
    return marketing.sugestao_livre()
