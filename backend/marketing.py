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
            "Bora pro arraiá? 🌽 Xadrez, peças leves e muito charme te esperam "
            "na {nome}! 🎉",
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
            "Liquida, liquida! 🛍️ As peças de inverno da {nome} estão com "
            "preços especiais. Aproveita antes que acabe! 🔖",
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
            "Feliz Dia do Cliente! 💛 Você é o motivo de tudo isso. Vem "
            "comemorar com a gente na {nome}! 🤝",
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
            "Primavera é renovação! 🌼 Que tal cores novas no seu guarda-roupa? "
            "Te esperamos na {nome}. 🌸",
        ],
        hashtags=["#primavera", "#novacolecao", "#modafeminina", "#virtuaumodas"],
        ideia_foto="Peças leves e coloridas com flores ao fundo.",
    ),
    Ocasiao(
        "Black Friday", "comemorativa", 11, None, "🖤🔥",
        legendas=[
            "BLACK FRIDAY chegando na {nome}! 🖤 Os melhores looks com os "
            "melhores preços do ano. Já separa sua listinha! 🔥",
            "Chegou a hora! 🔥 Black Friday na {nome} com descontos imperdíveis. "
            "Não vai ficar de fora, né? 🖤",
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
            "Que tal um presente que ela vai amar usar? 🎁 No Natal, a {nome} "
            "tem o look perfeito. Vem conferir! 🎄",
        ],
        hashtags=["#natal", "#presentedenatal", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Look festivo em vermelho/dourado, clima natalino.",
    ),
    Ocasiao(
        "Ano Novo", "comemorativa", 1, 1, "🎆✨",
        legendas=[
            "Ano novo, look novo! 🎆 Comece 2026 com estilo e confiança. A "
            "{nome} tem a peça perfeita pra sua virada. ✨",
            "Que o novo ano venha cheio de estilo! ✨ Vem renovar o guarda-roupa "
            "na {nome}. 🎆",
        ],
        hashtags=["#anonovo", "#reveillon", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Look branco/dourado elegante, clima de festa.",
    ),
    Ocasiao(
        "Carnaval", "comemorativa", 2, None, "🎭🎉",
        legendas=[
            "Carnaval chegando! 🎭 Separa o look pra cair na folia com muito "
            "charme e conforto. Passa na {nome}! 🎉",
        ],
        hashtags=["#carnaval", "#folia", "#modafeminina", "#virtuaumodas",
                  "#macatuba"],
        ideia_foto="Peças leves e coloridas, clima alegre e descontraído.",
    ),
    Ocasiao(
        "Início do Outono", "estacao", 3, 20, "🍂🧣",
        legendas=[
            "O outono chegou! 🍂 Hora de aquecer o look com peças de meia "
            "estação cheias de estilo. Vem ver as novidades da {nome}! 🧣",
        ],
        hashtags=["#outono", "#meiaestacao", "#modafeminina", "#virtuaumodas"],
        ideia_foto="Tons terrosos, cardigãs e peças de meia estação.",
    ),
    Ocasiao(
        "Páscoa", "comemorativa", 4, None, "🐰🍫",
        legendas=[
            "Páscoa é tempo de carinho! 🐰 Que tal se presentear com um look "
            "novo? Te esperamos na {nome}. 🍫",
        ],
        hashtags=["#pascoa", "#modafeminina", "#virtuaumodas", "#macatuba"],
        ideia_foto="Look em tons pastéis, clima leve e delicado.",
    ),
    Ocasiao(
        "Outubro Rosa", "comemorativa", 10, None, "🎀💗",
        legendas=[
            "Outubro Rosa 🎀 Cuidar de si é um ato de amor. A {nome} apoia a "
            "campanha de conscientização e prevenção do câncer de mama. Cuide-se, "
            "você é importante. 💗",
        ],
        hashtags=["#outubrorosa", "#prevencao", "#autocuidado", "#virtuaumodas"],
        ideia_foto="Detalhe em rosa, mensagem de conscientização (tom respeitoso).",
    ),
    Ocasiao(
        "Início do Verão", "estacao", 12, 21, "☀️👙",
        legendas=[
            "Verão chegando! ☀️ Peças fresquinhas, leves e cheias de estilo pra "
            "curtir a estação mais quente do ano. Vem ver a coleção da {nome}! 👗",
        ],
        hashtags=["#verao", "#colecaoverao", "#modafeminina", "#virtuaumodas"],
        ideia_foto="Peças leves e coloridas, clima de sol e leveza.",
    ),
    Ocasiao(
        "Aniversário da Virtuau Modas", "loja", 5, 28, "🎂🎉",
        legendas=[
            "Hoje é dia de festa: a {nome} está de aniversário! 🎂 Obrigada a "
            "cada cliente que faz parte dessa história. Tem novidade e mimo "
            "esperando por você! 🎉",
        ],
        hashtags=["#aniversario", "#virtuaumodas", "#macatuba", "#modafeminina"],
        ideia_foto="Foto comemorativa da loja, clima de celebração.",
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


DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def plano_semana(dias: int = 7, inicio: date | None = None) -> list[dict]:
    """Monta um plano de conteúdo para os próximos `dias`, um post por dia.

    Em dias com data comemorativa/sazonal, usa a sugestão dela; nos demais,
    rodízio das ideias 'coringa' (novidade, look do dia, prova social), para
    garantir constância nas publicações sem repetir sempre o mesmo.
    """
    inicio = inicio or date.today()
    ocasioes = {o["data"]: o for o in proximas_ocasioes(inicio, dias=dias + 1)}

    plano = []
    for i in range(dias):
        d = inicio + timedelta(days=i)
        chave = d.isoformat()
        if chave in ocasioes:
            post = ocasioes[chave]
        else:
            post = gerar_post(TEMAS_LIVRES[i % len(TEMAS_LIVRES)])
            post["data"] = chave
            post["dias_ate"] = i
        post["dia_semana"] = DIAS_SEMANA[d.weekday()]
        plano.append(post)
    return plano


# Palavras pequenas que não viram hashtag
_STOPWORDS = {"de", "da", "do", "das", "dos", "e", "o", "a", "os", "as", "para",
              "pra", "com", "em", "no", "na", "um", "uma"}


def _hashtags_de_tema(tema: str) -> list[str]:
    """Cria hashtags a partir das palavras do tema digitado."""
    import unicodedata
    tags = []
    for palavra in tema.lower().split():
        limpa = "".join(c for c in unicodedata.normalize("NFKD", palavra)
                        if c.isalnum() and not unicodedata.combining(c))
        if limpa and limpa not in _STOPWORDS and len(limpa) > 2:
            tags.append(f"#{limpa}")
    base = ["#modafeminina", "#virtuaumodas", "#macatuba"]
    return list(dict.fromkeys(tags + base))[:6]


def gerar_de_tema(tema: str) -> dict:
    """Gera um post a partir de um tema livre digitado pela usuária.

    Versão por modelos (sem IA). A função fica isolada para, no futuro, um
    modelo de linguagem escrever um texto totalmente personalizado a partir
    do tema, sem mudar o resto da aplicação.
    """
    tema = (tema or "").strip()
    if not tema:
        return {"erro": "Digite um tema para gerar o post."}

    # Se houver chave de API, usa a IA de verdade (Claude). Senão, modelos prontos.
    from backend import ia
    if ia.disponivel():
        try:
            return ia.gerar_post(tema, MARCA)
        except Exception:
            pass  # qualquer falha cai no modelo pronto abaixo

    modelos = [
        "✨ Olha que novidade: {tema}! Vem conferir de pertinho na {nome}. "
        "Você vai amar! 💛",
        "👗 Bora falar de {tema}? Na {nome} tem opção pra você arrasar. "
        "Passa aqui e escolha a sua! ✨",
        "💫 {tema_cap} é com a gente! Conforto, estilo e você na {nome}. "
        "Te esperamos! 🛍️",
    ]
    legenda = random.choice(modelos).format(
        tema=tema, tema_cap=tema.capitalize(), nome=MARCA["nome"],
    )
    return {
        "tema": tema.capitalize(),
        "tipo": "livre",
        "legenda": legenda,
        "hashtags": " ".join(_hashtags_de_tema(tema)),
        "ideia_foto": f"Foto que destaque “{tema}”, no estilo aconchegante da marca.",
        "melhor_horario": random.choice(["12h", "18h", "19h", "20h"]),
        "fonte": "modelo",
    }


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
