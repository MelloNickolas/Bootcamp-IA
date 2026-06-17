import { useEffect, useState } from "react";
import "./App.css";

const API = "http://localhost:8000";

// Cor da etiqueta conforme o tipo de ocasião
const COR_TIPO = {
  comemorativa: "#e2752e",
  estacao: "#4c9a6a",
  loja: "#9b6dff",
};

function PostCard({ post }) {
  const [copiado, setCopiado] = useState(false);

  function copiar() {
    const texto = `${post.legenda}\n\n${post.hashtags}`;
    navigator.clipboard.writeText(texto);
    setCopiado(true);
    setTimeout(() => setCopiado(false), 1800);
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
        {post.dias_ate != null && (
          <span className="contador">
            {post.dias_ate === 0 ? "hoje" : `faltam ${post.dias_ate} dias`}
          </span>
        )}
      </header>

      <h3 className="card-tema">{post.tema}</h3>
      {data && <p className="card-data">📅 {data}</p>}

      <p className="card-legenda">{post.legenda}</p>

      <p className="card-hashtags">{post.hashtags}</p>

      <div className="card-meta">
        <span>📸 {post.ideia_foto}</span>
        <span>⏰ Melhor horário: {post.melhor_horario}</span>
      </div>

      <button className="btn-copiar" onClick={copiar}>
        {copiado ? "✓ Copiado!" : "Copiar legenda + hashtags"}
      </button>
    </article>
  );
}

export default function App() {
  const [marca, setMarca] = useState(null);
  const [ocasioes, setOcasioes] = useState([]);
  const [livre, setLivre] = useState(null);
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
  }, []);

  function gerarLivre() {
    fetch(`${API}/sugestao-livre`)
      .then((r) => r.json())
      .then(setLivre)
      .catch(() => setErro(true));
  }

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

      {erro && (
        <div className="aviso-erro">
          Não consegui falar com o cérebro (Python). Confira se a API está
          rodando em <code>localhost:8000</code>.
        </div>
      )}

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
          <PostCard post={livre} />
        </div>
      )}

      <h2 className="secao-titulo">📅 Próximas datas e sugestões</h2>

      {carregando && <p className="carregando">Carregando ideias…</p>}

      <div className="grade">
        {ocasioes.map((post, i) => (
          <PostCard key={i} post={post} />
        ))}
      </div>

      {marca && (
        <footer className="rodape">
          {marca.nome} · {marca.cidade} · {marca.instagram} — “{marca.slogan}”
        </footer>
      )}
    </div>
  );
}
