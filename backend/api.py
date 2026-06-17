"""API do agente de marketing da Virtuau Modas.

É a "portinha" que liga o site (React) ao cérebro (marketing.py). Expõe os
endpoints que a tela consome para mostrar o calendário de datas, as sugestões
de post e as ideias "coringa".

Rodar:  ./.venv/Scripts/python.exe -m uvicorn backend.api:app --reload
"""
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import favoritos, marketing

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


@app.get("/gerar-tema")
def gerar_tema(tema: str = ""):
    """Gera um post a partir de um tema livre digitado pela usuária."""
    return marketing.gerar_de_tema(tema)


@app.get("/ia-status")
def ia_status():
    """Informa se a IA de verdade (Claude) está ligada."""
    from backend import ia
    return {"ia_ligada": ia.disponivel()}


@app.get("/plano-semana")
def plano_semana(dias: int = 7):
    """Plano de conteúdo para os próximos dias (um post por dia)."""
    return marketing.plano_semana(dias=dias)


@app.get("/favoritos")
def listar_favoritos():
    """Lista os posts salvos como favoritos."""
    return favoritos.listar()


@app.post("/favoritos")
def salvar_favorito(post: dict = Body(...)):
    """Salva um post nos favoritos."""
    return favoritos.adicionar(post)


@app.delete("/favoritos/{fav_id}")
def remover_favorito(fav_id: int):
    """Remove um favorito pelo id."""
    return {"removido": favoritos.remover(fav_id)}
