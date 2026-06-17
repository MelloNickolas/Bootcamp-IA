"""Motor de IA generativa (Claude) para escrever os posts.

Quando há uma chave de API configurada (variável de ambiente
ANTHROPIC_API_KEY), os textos passam a ser escritos pelo Claude, no tom da
marca. Sem a chave, o restante da aplicação continua funcionando com os
modelos prontos — esta camada é totalmente opcional e isolada.
"""
import os

from pydantic import BaseModel

# Modelo mais capaz da Anthropic (ver skill claude-api).
MODELO = "claude-opus-4-8"


class PostIA(BaseModel):
    """Formato de saída que pedimos ao Claude (JSON validado)."""
    legenda: str
    hashtags: str
    ideia_foto: str
    melhor_horario: str


def disponivel() -> bool:
    """Há chave de API configurada?"""
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _sistema(marca: dict) -> str:
    return (
        f"Você é especialista em marketing de moda e social media da loja "
        f"{marca['nome']}, em {marca['cidade']}. Escreve posts de Instagram para "
        f"o público de {marca['publico']}, com uma voz {marca['vibe']} "
        f"(lema: \"{marca['slogan']}\").\n\n"
        "Escreva uma legenda curta e cativante em português do Brasil, com 2 a 4 "
        "emojis bem colocados, uma chamada para ação (convidar a visitar a loja), "
        "e sem inventar promoções ou preços específicos. Gere também hashtags "
        "relevantes (incluindo #virtuaumodas e #macatuba), uma ideia de foto e o "
        "melhor horário de postagem."
    )


def gerar_post(tema: str, marca: dict) -> dict:
    """Gera um post com o Claude. Lança exceção se algo der errado."""
    import anthropic

    client = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do ambiente
    resposta = client.messages.parse(
        model=MODELO,
        max_tokens=1024,
        system=_sistema(marca),
        messages=[{
            "role": "user",
            "content": f"Crie um post de Instagram sobre o tema: {tema}",
        }],
        output_format=PostIA,
    )
    post = resposta.parsed_output
    return {
        "tema": tema.capitalize(),
        "tipo": "livre",
        "legenda": post.legenda,
        "hashtags": post.hashtags,
        "ideia_foto": post.ideia_foto,
        "melhor_horario": post.melhor_horario,
        "fonte": "ia",
    }
