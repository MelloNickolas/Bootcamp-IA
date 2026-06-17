"""Cérebro do agente de marketing da Virtuau Modas.

Gera ideias de posts para o Instagram com base em datas comemorativas e temas
relevantes para uma loja de moda feminina. Cada sugestão traz: tema, legenda
pronta (no tom da marca), hashtags, ideia de foto e melhor dia/horário.

Nesta primeira versão a geração é feita por modelos/exemplos (sem chave de API).
A função `gerar_post()` concentra a criação do texto, de modo que, no futuro,
um modelo de linguagem (ex.: Claude API) possa substituí-la sem mexer no resto.
"""
import random
from dataclasses import dataclass, field
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Identidade da marca (o que ensina o "jeito" da Virtuau ao agente)
# ---------------------------------------------------------------------------
MARCA = {
    "nome": "Virtuau Modas",
    "cidade": "Macatuba",
    "instagram": "@mvirtuau",
    "publico": "mulheres adultas",
    "vibe": "aconchegante e elegante",
    "slogan": "conforto, estilo e você",
}


# ---------------------------------------------------------------------------
# Datas e temas relevantes para a loja
# ---------------------------------------------------------------------------
@dataclass
class Ocasiao:
    nome: str
    tipo: str                      # "comemorativa", "estacao", "loja"
    mes: int
    dia: int | None = None         # None = data móvel/aproximada do mês
    emojis: str = ""
    legendas: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    ideia_foto: str = ""


OCASIOES: list[Ocasiao] = [
    Ocasiao(
        "Dia Internacional da Mulher", "comemorativa", 3, 8, "💜👑",
        legendas=[
            "Hoje é dia de celebrar VOCÊ. 💜 Toda mulher merece se sentir linda "
            "e confiante — e a {nome} tem a peça perfeita pra isso. Vem se "
            "presentear! ✨",
            "Força, leveza e estilo. 👑 Feliz Dia da Mulher! Passa aqui e "
            "escolha um look que combina com a sua história. 💜",
        ],
        hashtags=["#diadamulher", "#modafeminina", "#mulheres", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Cliente sorrindo com um look que valoriza, tom acolhedor.",
    ),
    Ocasiao(
        "Dia das Mães", "comemorativa", 5, None, "🌷💐",
        legendas=[
            "O presente que toda mãe ama: se sentir especial. 🌷 Na {nome} você "
            "encontra looks cheios de carinho pra presentear (ou se presentear!). "
            "Corre que o Dia das Mães está chegando! 💐",
            "Mãe é sinônimo de amor — e de bom gosto. 💐 Escolha um presente "
            "que ela vai amar usar. Te esperamos na {nome}! 🌷",
        ],
        hashtags=["#diadasmaes", "#presenteparamae", "#modafeminina",
                  "#virtuaumodas", "#macatuba"],
        ideia_foto="Peça embrulhada para presente + look elegante de mãe.",
    ),
    Ocasiao(
        "Dia dos Namorados", "comemorativa", 6, 12, "❤️🌹",
        legendas=[
            "Pro date perfeito, o look também importa. ❤️ Vem encontrar aquela "
            "peça que vai arrasar no Dia dos Namorados! 🌹 {nome}.",
            "Amor próprio também é se vestir bem. ❤️ Seja pra um date ou pra "
            "você mesma, temos o look ideal. 🌹",
        ],
        hashtags=["#diadosnamorados", "#look", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Look romântico em tons quentes, clima aconchegante.",
    ),
    Ocasiao(
        "Início do Inverno", "estacao", 6, 21, "🧥❄️",
        legendas=[
            "Chegou o friozinho e a gente já preparou tudo! 🧥 Tricôs, casacos "
            "e peças quentinhas que aquecem com muito estilo. Vem conferir a "
            "coleção de inverno da {nome}! ❄️",
            "Conforto e estilo pra encarar o frio. ❄️ Nova coleção de inverno "
            "chegando na {nome} — quentinha e linda! 🧥",
        ],
        hashtags=["#inverno", "#colecaoinverno", "#tricot", "#modafeminina",
                  "#virtuaumodas"],
        ideia_foto="Tricôs e casacos em flatlay aconchegante, velas e tons neutros.",
    ),
    Ocasiao(
        "Festa Junina", "comemorativa", 6, 24, "🎉🌽",
        legendas=[
            "Arraiá com estilo! 🎉 Separa o look pra cair na quadrilha com muito "
            "charme. Passa na {nome}! 🌽",
        ],
        hashtags=["#festajunina", "#arraia", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Look com xadrez ou peças leves, clima festivo e divertido.",
    ),
    Ocasiao(
        "Liquidação de Inverno", "loja", 7, None, "🔖🛍️",
        legendas=[
            "É agora! 🔖 Liquidação de inverno na {nome}: aquela peça que você "
            "namorava com um precinho especial. Corre que é por tempo limitado! 🛍️",
        ],
        hashtags=["#liquidacao", "#promocao", "#saldao", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Etiqueta de desconto em destaque sobre as peças.",
    ),
    Ocasiao(
        "Dia do Cliente", "comemorativa", 9, 15, "💛🤝",
        legendas=[
            "Hoje o dia é de quem faz a {nome} acontecer: VOCÊ! 💛 Obrigada por "
            "tanto carinho. Passa aqui que tem novidade esperando por você! 🤝",
        ],
        hashtags=["#diadocliente", "#obrigada", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Foto calorosa da loja ou de clientes felizes (autorizadas).",
    ),
    Ocasiao(
        "Início da Primavera", "estacao", 9, 22, "🌸🌼",
        legendas=[
            "A estação das flores chegou! 🌸 Cores, leveza e peças novas pra "
            "renovar o guarda-roupa. Vem ver a coleção de primavera da {nome}! 🌼",
        ],
        hashtags=["#primavera", "#novacolecao", "#modafeminina", "#virtuaumodas"],
        ideia_foto="Peças leves e coloridas com flores ao fundo.",
    ),
    Ocasiao(
        "Black Friday", "comemorativa", 11, None, "🖤🔥",
        legendas=[
            "BLACK FRIDAY chegando na {nome}! 🖤 Os melhores looks com os "
            "melhores preços do ano. Já separa sua listinha! 🔥",
        ],
        hashtags=["#blackfriday", "#promocao", "#ofertas", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Arte escura com destaque para os descontos.",
    ),
    Ocasiao(
        "Natal", "comemorativa", 12, 25, "🎄🎁",
        legendas=[
            "O Natal está chegando! 🎄 Presenteie quem você ama (e você também!) "
            "com looks cheios de estilo. Te esperamos na {nome}! 🎁",
        ],
        hashtags=["#natal", "#presentedenatal", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Look festivo em vermelho/dourado, clima natalino.",
    ),
]

# Posts "coringa" para usar em qualquer dia sem data especial
TEMAS_LIVRES: list[Ocasiao] = [
    Ocasiao(
        "Novidade da semana", "loja", 0, None, "✨🆕",
        legendas=[
            "Chegou peça nova na {nome}! ✨ {vibe} do jeitinho que você gosta. "
            "Corre ver antes que acabe! 🆕",
            "Novidades fresquinhas pra você arrasar. ✨ Passa na {nome} e "
            "garanta a sua! 🆕",
        ],
        hashtags=["#novidade", "#modafeminina", "#look", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Destaque da peça nova, foto clean e bem iluminada.",
    ),
    Ocasiao(
        "Look do dia", "loja", 0, None, "👗💫",
        legendas=[
            "Look do dia pra inspirar! 💫 {slogan}. Qual é o seu favorito? "
            "Conta aqui nos comentários! 👗",
        ],
        hashtags=["#lookdodia", "#ootd", "#modafeminina", "#virtuaumodas"],
        ideia_foto="Modelo com look completo, pose natural.",
    ),
    Ocasiao(
        "Prova social / Prêmio", "loja", 0, None, "🏆💛",
        legendas=[
            "Eleita a melhor loja de roupa feminina de {cidade}! 🏆 Isso é "
            "graças a você. Obrigada pela confiança — vem fazer parte da "
            "{nome}! 💛",
        ],
        hashtags=["#melhorloja", "#obrigada", "#virtuaumodas", "#macatuba"],
        ideia_foto="Selo do prêmio + fachada ou interior da loja.",
    ),
]


# ---------------------------------------------------------------------------
# Geração
# ---------------------------------------------------------------------------
def _data_no_ano(oc: Ocasiao, ano: int) -> date | None:
    if oc.mes == 0 or oc.dia is None:
        return date(ano, oc.mes, 15) if oc.mes else None
    return date(ano, oc.mes, oc.dia)


def gerar_post(ocasiao: Ocasiao) -> dict:
    """Cria um post a partir de uma ocasião (versão por modelos, sem API)."""
    legenda = random.choice(ocasiao.legendas).format(
        nome=MARCA["nome"], cidade=MARCA["cidade"], vibe=MARCA["vibe"],
        slogan=MARCA["slogan"],
    )
    return {
        "tema": ocasiao.nome,
        "tipo": ocasiao.tipo,
        "legenda": f"{ocasiao.emojis} {legenda}".strip(),
        "hashtags": " ".join(ocasiao.hashtags),
        "ideia_foto": ocasiao.ideia_foto,
        "melhor_horario": random.choice(["12h", "18h", "19h", "20h"]),
    }


def proximas_ocasioes(a_partir_de: date | None = None, dias: int = 90) -> list[dict]:
    """Lista as datas comemorativas/estações dos próximos `dias`, com a sugestão."""
    hoje = a_partir_de or date.today()
    limite = hoje + timedelta(days=dias)
    resultado = []
    for oc in OCASIOES:
        for ano in (hoje.year, hoje.year + 1):
            d = _data_no_ano(oc, ano)
            if d and hoje <= d <= limite:
                post = gerar_post(oc)
                post["data"] = d.isoformat()
                post["dias_ate"] = (d - hoje).days
                resultado.append(post)
                break
    return sorted(resultado, key=lambda p: p["data"])


def sugestao_livre() -> dict:
    """Uma ideia de post 'coringa' para qualquer dia."""
    return gerar_post(random.choice(TEMAS_LIVRES))


if __name__ == "__main__":
    print(f"=== Agente de Marketing — {MARCA['nome']} ({MARCA['cidade']}) ===\n")
    print(">>> Próximas datas e sugestões de post:\n")
    for p in proximas_ocasioes(dias=120):
        print(f"📅 {p['data']}  (faltam {p['dias_ate']} dias) — {p['tema']}")
        print(f"   Legenda: {p['legenda']}")
        print(f"   Hashtags: {p['hashtags']}")
        print(f"   Foto: {p['ideia_foto']}  | Melhor horário: {p['melhor_horario']}")
        print()
    print(">>> Ideia 'coringa' para hoje:\n")
    s = sugestao_livre()
    print(f"   {s['tema']}: {s['legenda']}")
    print(f"   {s['hashtags']}")
