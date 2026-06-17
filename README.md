# Virtuau Inteligente — Agente de Marketing

Plataforma de IA que **gera ideias de posts para o Instagram** da loja
**Virtuau Modas** (moda feminina — Macatuba/SP), com base em datas
comemorativas e temas relevantes para o negócio.

Projeto do Bootcamp de Desenvolvimento em Inteligência Artificial —
Ciência da Computação (Grupo 11).

A loja não tem um marketing estruturado e posta "no improviso". A plataforma
resolve isso sugerindo, no tom da marca, **o que postar e quando**: legenda
pronta, hashtags, ideia de foto e melhor horário.

## Como funciona (em duas partes)

- **Cérebro (Python)** — gera as ideias de post. Pasta `backend/`.
- **Cara (React)** — o site bonito que a loja usa. Pasta `frontend/`.

O site conversa com o cérebro por uma API (FastAPI). A geração de texto hoje
usa modelos/exemplos (sem custo); está preparada para, no futuro, usar um
modelo de linguagem (ex.: Claude API) sem mudar o resto.

## Como executar

Abra **dois terminais**.

**Terminal 1 — o cérebro (Python):**
```powershell
cd C:\Users\nicko\Documents\GitHub\Bootcamp-IA
.\.venv\Scripts\python.exe -m uvicorn backend.api:app --port 8000
```

**Terminal 2 — o site (React):**
```powershell
cd C:\Users\nicko\Documents\GitHub\Bootcamp-IA\frontend
npm run dev
```

Depois abra no navegador: **http://localhost:5173**

### (Opcional) Ligar a IA de verdade (Claude)

Por padrão os textos usam modelos prontos (sem custo). Para que o **Claude**
escreva os posts, defina a chave de API **antes** de iniciar o cérebro, no
mesmo terminal:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."   # sua chave
.\.venv\Scripts\python.exe -m uvicorn backend.api:app --port 8000
```

Com a chave ativa, a tela mostra **✨ IA ativada** e os posts gerados ganham o
selo **✨ por IA**. A chave é lida do ambiente — nunca fica salva no código.

> Primeira vez? Prepare o ambiente uma única vez:
> ```powershell
> # Python
> python -m venv .venv
> .\.venv\Scripts\python.exe -m pip install -r requirements.txt
> # React
> cd frontend; npm install
> ```

## Estrutura

```
backend/
  marketing.py   Cérebro: datas, temas e geração dos posts
  api.py         API que liga o site ao cérebro
frontend/
  src/App.jsx    Tela principal (calendário de posts)
  src/App.css    Estilo com a identidade da Virtuau
docs/            Documentação e evidências da entrega
```

## Equipe

- **Nickolas Passos Homem de Mello**
- **Vitor Gabriel Pompollo**
