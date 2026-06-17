"""Armazenamento simples dos posts favoritos.

Salva os posts que a usuária marcou como favoritos num arquivo JSON, para que
fiquem guardados entre uma sessão e outra. Não precisa de banco de dados — é
uma loja só, com poucos registros.
"""
import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path(__file__).resolve().parent.parent / "data" / "favoritos.json"


def _carregar() -> list[dict]:
    if not ARQUIVO.exists():
        return []
    try:
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _salvar(lista: list[dict]) -> None:
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO.write_text(json.dumps(lista, ensure_ascii=False, indent=2),
                       encoding="utf-8")


def listar() -> list[dict]:
    """Todos os favoritos, do mais recente para o mais antigo."""
    return list(reversed(_carregar()))


def adicionar(post: dict) -> dict:
    """Guarda um post como favorito e devolve o registro salvo."""
    lista = _carregar()
    registro = dict(post)
    registro["id"] = int(datetime.now().timestamp() * 1000)
    registro["salvo_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    lista.append(registro)
    _salvar(lista)
    return registro


def remover(fav_id: int) -> bool:
    """Remove um favorito pelo id. Retorna True se removeu."""
    lista = _carregar()
    nova = [f for f in lista if f.get("id") != fav_id]
    if len(nova) != len(lista):
        _salvar(nova)
        return True
    return False
