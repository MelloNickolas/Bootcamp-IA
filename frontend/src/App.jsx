import { useEffect, useState } from "react";
import "./App.css";

const API = "http://localhost:8000";

// Cor da etiqueta conforme o tipo de ocasião
const COR_TIPO = {
  comemorativa: "#e2752e",
  estacao: "#4c9a6a",
  loja: "#9b6dff",
  livre: "#e2752e",
};

function PostCard({ post, onFavoritar, onRemover }) {
  const [copiado, setCopiado] = useState(false);
  const [salvo, setSalvo] = useState(false);

  function copiar() {
    const texto = `${post.legenda}\n\n${post.hashtags}`;
    navigator.clipboard.writeText(texto);
    setCopiado(true);
    setTimeout(() => setCopiado(false), 1800);
  }

  function favoritar() {
    onFavoritar(post);
    setSalvo(true);
    setTimeout(() => setSalvo(false), 1800);
  }

  const data = post.data
    ? new Date(post.data + "T00:00:00").toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "long",
      })
    : null;

  return (
    <article className="card">
      <header className="card-top">
        <span className="tag" style={{ background: COR_TIPO[post.tipo] || "#888" }}>
          {post.tipo}
        </span>
        <div className="card-top-dir">
          {post.dia_semana && <span className="dia-semana">{post.dia_semana}</span>}
          {post.dias_ate != null && (
            <span className="contador">
              {post.dias_ate === 0 ? "hoje" : `faltam ${post.dias_ate} dias`}
            </span>
          )}
        </div>
      </header>

      <h3 className="card-tema">
        {post.tema}
        {post.fonte === "ia" && <span className="selo-ia">✨ por IA</span>}
      </h3>
      {data && <p className="card-data">📅 {data}</p>}

      <p className="card-legenda">{post.legenda}</p>
      <p className="card-hashtags">{post.hashtags}</p>

      <div className="card-meta">
        <span>📸 {post.ideia_foto}</span>
        <span>⏰ Melhor horário: {post.melhor_horario}</span>
        {post.salvo_em && <span>💾 Salvo em {post.salvo_em}</span>}
      </div>

      <div className="card-acoes">
        <button className="btn-copiar" onClick={copiar}>
          {copiado ? "✓ Copiado!" : "Copiar"}
        </button>
        {onFavoritar && (
          <button className="btn-fav" onClick={favoritar}>
            {salvo ? "♥ Salvo!" : "♡ Favoritar"}
          </button>
        )}
        {onRemover && (
          <button className="btn-remover" onClick={() => onRemover(post.id)}>
            🗑 Remover
          </button>
        )}
      </div>
    </article>
  );
}

const MESES = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];
const CABECALHO_DIAS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

function Calendario({ ocasioes, onFavoritar }) {
  const hoje = new Date();
  const [mes, setMes] = useState(new Date(hoje.getFullYear(), hoje.getMonth(), 1));
  const [selecionado, setSelecionado] = useState(null);

  // Mapa de datas (YYYY-MM-DD) -> post
  const porData = {};
  ocasioes.forEach((o) => {
    if (o.data) porData[o.data] = o;
  });

  const ano = mes.getFullYear();
  const m = mes.getMonth();
  const inicioOffset = new Date(ano, m, 1).getDay();
  const diasNoMes = new Date(ano, m + 1, 0).getDate();
  const pad = (n) => String(n).padStart(2, "0");

  const celulas = [];
  for (let i = 0; i < inicioOffset; i++) celulas.push(null);
  for (let d = 1; d <= diasNoMes; d++) celulas.push(d);

  function mudarMes(delta) {
    setMes(new Date(ano, m + delta, 1));
    setSelecionado(null);
  }

  const hojeStr = `${hoje.getFullYear()}-${pad(hoje.getMonth() + 1)}-${pad(hoje.getDate())}`;

  return (
    <div className="calendario">
      <div className="cal-topo">
        <button className="cal-nav" onClick={() => mudarMes(-1)}>‹</button>
        <h2>{MESES[m]} de {ano}</h2>
        <button className="cal-nav" onClick={() => mudarMes(1)}>›</button>
      </div>

      <div className="cal-grade">
        {CABECALHO_DIAS.map((d) => (
          <div key={d} className="cal-cab">{d}</div>
        ))}
        {celulas.map((d, i) => {
          if (d === null) return <div key={`v${i}`} className="cal-vazio" />;
          const ds = `${ano}-${pad(m + 1)}-${pad(d)}`;
          const post = porData[ds];
          return (
            <button
              key={ds}
              className={
                "cal-dia" +
                (post ? ` tem-post tipo-${post.tipo}` : "") +
                (ds === hojeStr ? " hoje" : "") +
                (selecionado && selecionado.data === ds ? " sel" : "")
              }
              onClick={() => post && setSelecionado(post)}
              disabled={!post}
            >
              <span className="cal-num">{d}</span>
              {post && <span className="cal-ponto" />}
            </button>
          );
        })}
      </div>

      <p className="cal-dica">
        Os dias destacados têm uma sugestão de post. Clique para ver.
      </p>

      {selecionado && (
        <div className="livre-resultado">
          <PostCard post={selecionado} onFavoritar={onFavoritar} />
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [aba, setAba] = useState("inicio");
  const [marca, setMarca] = useState(null);
  const [ocasioes, setOcasioes] = useState([]);
  const [livre, setLivre] = useState(null);
  const [tema, setTema] = useState("");
  const [postTema, setPostTema] = useState(null);
  const [iaLigada, setIaLigada] = useState(false);
  const [gerando, setGerando] = useState(false);
  const [plano, setPlano] = useState([]);
  const [gerandoPlano, setGerandoPlano] = useState(false);
  const [favoritos, setFavoritos] = useState([]);
  const [erro, setErro] = useState(false);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/marca`).then((r) => r.json()),
      fetch(`${API}/ocasioes?dias=180`).then((r) => r.json()),
    ])
      .then(([m, o]) => {
        setMarca(m);
        setOcasioes(o);
      })
      .catch(() => setErro(true))
      .finally(() => setCarregando(false));

    fetch(`${API}/ia-status`)
      .then((r) => r.json())
      .then((s) => setIaLigada(s.ia_ligada))
      .catch(() => {});

    carregarFavoritos();
  }, []);

  function carregarFavoritos() {
    fetch(`${API}/favoritos`)
      .then((r) => r.json())
      .then(setFavoritos)
      .catch(() => {});
  }

  function favoritar(post) {
    fetch(`${API}/favoritos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(post),
    })
      .then(() => carregarFavoritos())
      .catch(() => setErro(true));
  }

  function removerFavorito(id) {
    fetch(`${API}/favoritos/${id}`, { method: "DELETE" })
      .then(() => carregarFavoritos())
      .catch(() => setErro(true));
  }

  function gerarLivre() {
    fetch(`${API}/sugestao-livre`)
      .then((r) => r.json())
      .then(setLivre)
      .catch(() => setErro(true));
  }

  function gerarTema() {
    if (!tema.trim()) return;
    setGerando(true);
    setPostTema(null);
    fetch(`${API}/gerar-tema?tema=${encodeURIComponent(tema)}`)
      .then((r) => r.json())
      .then(setPostTema)
      .catch(() => setErro(true))
      .finally(() => setGerando(false));
  }

  function gerarPlano() {
    setGerandoPlano(true);
    fetch(`${API}/plano-semana?dias=7`)
      .then((r) => r.json())
      .then(setPlano)
      .catch(() => setErro(true))
      .finally(() => setGerandoPlano(false));
  }

  function exportarPlano() {
    if (!plano.length) return;
    const linhas = plano.map((p) => {
      const d = new Date(p.data + "T00:00:00").toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "long",
      });
      return (
        `${p.dia_semana} (${d}) — ${p.tema}\n` +
        `${p.legenda}\n${p.hashtags}\n` +
        `Foto: ${p.ideia_foto} | Melhor horário: ${p.melhor_horario}\n`
      );
    });
    const texto =
      "PLANO DE CONTEÚDO — Virtuau Modas\n" +
      "==================================\n\n" +
      linhas.join("\n");
    const blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "plano-virtuau-modas.txt";
    a.click();
    URL.revokeObjectURL(url);
  }

  const ABAS = [
    { id: "inicio", rotulo: "🏠 Início" },
    { id: "plano", rotulo: "🗓️ Plano da Semana" },
    { id: "calendario", rotulo: "📆 Calendário" },
    { id: "favoritos", rotulo: `♥ Favoritos${favoritos.length ? ` (${favoritos.length})` : ""}` },
  ];

  return (
    <div className="app">
      <header className="topo">
        <div className="logo">VM</div>
        <div>
          <h1>Virtuau Modas</h1>
          <p className="subtitulo">
            Agente de Marketing · ideias de post no piloto automático
          </p>
        </div>
      </header>

      <nav className="abas">
        {ABAS.map((a) => (
          <button
            key={a.id}
            className={`aba ${aba === a.id ? "ativa" : ""}`}
            onClick={() => setAba(a.id)}
          >
            {a.rotulo}
          </button>
        ))}
      </nav>

      {erro && (
        <div className="aviso-erro">
          Não consegui falar com o cérebro (Python). Confira se a API está
          rodando em <code>localhost:8000</code>.
        </div>
      )}

      {/* ----------------------- INÍCIO ----------------------- */}
      {aba === "inicio" && (
        <>
          <section className="bloco-livre">
            <div>
              <h2>Precisa postar hoje?</h2>
              <p>Gere uma ideia rápida pra qualquer dia.</p>
            </div>
            <button className="btn-gerar" onClick={gerarLivre}>
              ✨ Gerar ideia agora
            </button>
          </section>

          {livre && (
            <div className="livre-resultado">
              <PostCard post={livre} onFavoritar={favoritar} />
            </div>
          )}

          <section className="bloco-tema">
            <div>
              <h2>Tem um assunto específico?</h2>
              <p>
                Digite o tema e a plataforma cria o post pra você.{" "}
                {iaLigada ? (
                  <strong className="ia-on">✨ IA ativada</strong>
                ) : (
                  <span className="ia-off">(usando modelos prontos)</span>
                )}
              </p>
            </div>
            <div className="tema-form">
              <input
                type="text"
                className="tema-input"
                placeholder="Ex: promoção de tricô, vestido novo, frete grátis…"
                value={tema}
                onChange={(e) => setTema(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && gerarTema()}
              />
              <button className="btn-gerar" onClick={gerarTema} disabled={gerando}>
                {gerando ? "Criando…" : "Criar post"}
              </button>
            </div>
          </section>

          {postTema &&
            (postTema.erro ? (
              <p className="carregando">{postTema.erro}</p>
            ) : (
              <div className="livre-resultado">
                <PostCard post={postTema} onFavoritar={favoritar} />
              </div>
            ))}

          <h2 className="secao-titulo">📅 Próximas datas e sugestões</h2>
          {carregando && <p className="carregando">Carregando ideias…</p>}
          <div className="grade">
            {ocasioes.map((post, i) => (
              <PostCard key={i} post={post} onFavoritar={favoritar} />
            ))}
          </div>
        </>
      )}

      {/* ----------------------- PLANO DA SEMANA ----------------------- */}
      {aba === "plano" && (
        <>
          <section className="bloco-livre">
            <div>
              <h2>Plano da semana</h2>
              <p>7 posts prontos, um pra cada dia. Aproveita as datas e mantém a constância.</p>
            </div>
            <div className="plano-botoes">
              <button className="btn-gerar" onClick={gerarPlano} disabled={gerandoPlano}>
                {gerandoPlano ? "Montando…" : "🗓️ Montar plano"}
              </button>
              {plano.length > 0 && (
                <button className="btn-exportar" onClick={exportarPlano}>
                  ⬇️ Exportar (.txt)
                </button>
              )}
            </div>
          </section>

          {plano.length === 0 && !gerandoPlano && (
            <p className="carregando">Clique em “Montar plano” para gerar a semana.</p>
          )}
          <div className="grade">
            {plano.map((post, i) => (
              <PostCard key={i} post={post} onFavoritar={favoritar} />
            ))}
          </div>
        </>
      )}

      {/* ----------------------- CALENDÁRIO ----------------------- */}
      {aba === "calendario" && (
        <Calendario ocasioes={ocasioes} onFavoritar={favoritar} />
      )}

      {/* ----------------------- FAVORITOS ----------------------- */}
      {aba === "favoritos" && (
        <>
          <h2 className="secao-titulo">♥ Seus posts favoritos</h2>
          {favoritos.length === 0 ? (
            <p className="carregando">
              Você ainda não salvou nenhum post. Clique em “♡ Favoritar” em qualquer
              sugestão para guardá-la aqui.
            </p>
          ) : (
            <div className="grade">
              {favoritos.map((post) => (
                <PostCard key={post.id} post={post} onRemover={removerFavorito} />
              ))}
            </div>
          )}
        </>
      )}

      {marca && (
        <footer className="rodape">
          {marca.nome} · {marca.cidade} · {marca.instagram} — “{marca.slogan}”
        </footer>
      )}
    </div>
  );
}
