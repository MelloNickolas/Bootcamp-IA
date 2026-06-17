# Virtuau Inteligente — Agente de Marketing

Plataforma de **Inteligência Artificial** que gera ideias e conteúdos de posts
para o **Instagram** da loja **Virtuau Modas** (varejo de moda feminina —
Macatuba/SP), com base em **datas comemorativas** e **temas** relevantes para o
negócio.

> Projeto do **Bootcamp Desenvolvimento em Inteligência Artificial** —
> Ciência da Computação (Grupo 11).

---

## 🎯 O problema

A Virtuau Modas não tinha um marketing estruturado nas redes sociais: as
publicações eram feitas "no improviso", sem planejamento e sem aproveitar as
datas certas. A plataforma resolve isso sugerindo, **no tom da marca**, o que
postar e quando — entregando **legenda pronta, hashtags, ideia de foto e melhor
horário**.

---

## ✨ Funcionalidades

| Recurso | O que faz |
|--------|-----------|
| 🗓️ **Calendário de conteúdo** | Lista as próximas datas comemorativas/sazonais com a sugestão de post pronta |
| ✍️ **Gerador de posts** | Legenda, hashtags, ideia de foto e melhor horário, no tom da Virtuau |
| 💬 **Tema livre** | Você digita um assunto e a plataforma cria o post correspondente |
| 🤖 **IA generativa (opcional)** | Usa o **Claude** para escrever textos personalizados quando há chave de API |
| 📅 **Plano da semana** | Gera 7 posts (um por dia) e permite **exportar** em arquivo de texto |
| ♥ **Favoritos** | Salva e organiza os posts preferidos (guardados entre sessões) |
| 📆 **Calendário visual** | Mês em grade, com os dias de publicação destacados por tipo |

A interface é organizada em abas: **Início · Plano da Semana · Calendário · Favoritos**.

---

## 🧩 Como funciona (duas partes)

```
┌─────────────────┐      API (HTTP)      ┌──────────────────┐
│   Site (React)  │  ⇆  localhost:8000  │  Cérebro (Python) │
│  localhost:5173 │                      │   FastAPI + IA    │
└─────────────────┘                      └──────────────────┘
```

- **Cérebro (Python)** — gera o conteúdo. Pasta `backend/`.
- **Site (React)** — a interface que a loja usa. Pasta `frontend/`.
- A geração de texto funciona por **modelos prontos** (sem custo) e pode usar
  **IA generativa (Claude)** quando uma chave de API é configurada — sem alterar
  o restante da aplicação.

---

## 🛠️ Tecnologias

- **Back-end:** Python · FastAPI · Uvicorn
- **Front-end:** React · Vite · JavaScript (JSX)
- **IA (opcional):** Anthropic Claude (`claude-opus-4-8`)
- **Dados:** arquivo JSON (favoritos) — sem necessidade de banco
- **Versionamento:** Git / GitHub

---

## 🚀 Como executar

### Preparar o ambiente (apenas na primeira vez)

```powershell
# Back-end (Python)
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Front-end (React)
cd frontend
npm install
cd ..
```

### Rodar (toda vez) — abra dois terminais

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
(deixe as duas janelas abertas; para parar, `Ctrl + C` em cada uma).

### (Opcional) Ligar a IA de verdade (Claude)

Por padrão, os textos usam modelos prontos (sem custo). Para que o **Claude**
escreva os posts, defina a chave de API **antes** de iniciar o cérebro, no mesmo
terminal:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."   # sua chave
.\.venv\Scripts\python.exe -m uvicorn backend.api:app --port 8000
```

Com a chave ativa, a tela mostra **✨ IA ativada** e os posts gerados ganham o
selo **✨ por IA**. A chave é lida do ambiente — **nunca** fica salva no código.

---

## 🌐 Endpoints da API (referência)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/marca` | Identidade da marca (nome, cidade, vibe, slogan) |
| `GET` | `/ocasioes?dias=180` | Próximas datas comemorativas com sugestão |
| `GET` | `/sugestao-livre` | Uma ideia "coringa" para qualquer dia |
| `GET` | `/gerar-tema?tema=...` | Cria um post a partir de um tema livre |
| `GET` | `/ia-status` | Informa se a IA (Claude) está ligada |
| `GET` | `/plano-semana?dias=7` | Plano de conteúdo da semana |
| `GET` / `POST` / `DELETE` | `/favoritos` | Lista, salva e remove favoritos |

---

## 📁 Estrutura do projeto

```
Bootcamp-IA/
├── backend/
│   ├── marketing.py     Datas, temas e geração dos posts (cérebro)
│   ├── ia.py            Integração opcional com o Claude
│   ├── favoritos.py     Armazenamento dos favoritos (JSON)
│   └── api.py           API (FastAPI) que liga o site ao cérebro
├── frontend/
│   ├── src/App.jsx      Tela principal (abas, cards, calendário)
│   └── src/App.css      Estilo com a identidade da Virtuau
├── data/                Favoritos salvos em execução (fora do versionamento)
├── docs/                Documentação e evidências da entrega
├── requirements.txt     Dependências Python
├── Proposta_Entrega1_Virtuau_Modas.docx
└── Relatorio_Entrega2_Virtuau_Modas.docx
```

---

## 👥 Equipe

- **Nickolas Passos Homem de Mello** — levantamento de requisitos, back-end
  (Python/FastAPI), base de datas, geração de conteúdo e integração da IA.
- **Vitor Gabriel Pompollo** — interface React (calendário, plano, favoritos),
  integração com a API, ajuste de tom dos textos e documentação.

---

## 🏪 Instituição atendida

**Virtuau Modas** — varejo de moda feminina, Macatuba/SP.
Instagram: [@mvirtuau](https://instagram.com/mvirtuau) ·
Representante: Flaviane Passos Homem de Mello (proprietária).
