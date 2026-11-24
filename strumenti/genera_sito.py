#!/usr/bin/env python3
"""Genera il sito e il catalogo di PhysicsApp a partire dalle cartelle in apps/.

Ogni app sta in apps/<categoria>/[<sottocategoria>/]<id>/ con:
  app.json   dati dell'app (titolo, tipo, anno, allegati, materiali del docente...)
  README.md  descrizione e istruzioni d'uso
e i suoi file (index.html, .py, .ipynb, PDF...).

Lo script scrive:
  catalogo.json                 elenco di tutte le app (usato anche dal sito)
  index.html                    pagina principale con categorie e filtri
  apps/.../scheda.html          una pagina per app con le istruzioni
  README.md                     indice del repository (tra i segnaposto CATALOGO)

Uso:  python3 strumenti/genera_sito.py            (rigenera)
      python3 strumenti/genera_sito.py --controlla (esce con 1 se qualcosa non è aggiornato)
Serve il modulo markdown:  pip install markdown  (oppure uv run --with markdown ...)
"""
import html, json, sys
from pathlib import Path

import markdown

RADICE = Path(__file__).resolve().parent.parent
APPS = RADICE / "apps"
REPO = "https://github.com/MaxDvTn/PhysicsApp"
SITO = "https://maxdvtn.github.io/PhysicsApp/"

TIPI = {
    "web": ("App nel browser", "Si apre e funziona subito, anche sul telefono."),
    "vpython": ("Simulazione VPython", "Codice Python da lanciare su glowscript.org o in Colab."),
    "schede": ("Schede di laboratorio", "Schede PDF da seguire passo per passo."),
}
ICONE = {
    "web": '<svg class="icona" viewBox="0 0 32 32" aria-hidden="true"><rect x="3" y="5" width="26" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 10.5v9l7.5-4.5z" fill="currentColor"/></svg>',
    "vpython": '<svg class="icona" viewBox="0 0 32 32" aria-hidden="true"><path d="M11 6c-3 0-4 1.5-4 4v3c0 1.5-1 3-3 3 2 0 3 1.5 3 3v3c0 2.5 1 4 4 4M21 6c3 0 4 1.5 4 4v3c0 1.5 1 3 3 3-2 0-3 1.5-3 3v3c0 2.5-1 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2.5" fill="currentColor"/></svg>',
    "schede": '<svg class="icona" viewBox="0 0 32 32" aria-hidden="true"><path d="M8 3h11l6 6v20H8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 15h9M12 19h9M12 23h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
}
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">')
TEMA_JS = """<script>
try{var t=localStorage.getItem('tema');if(t)document.documentElement.dataset.tema=t}catch(e){}
function cambiaTema(){var r=document.documentElement,s=r.dataset.tema||(matchMedia('(prefers-color-scheme: dark)').matches?'scuro':'chiaro');
r.dataset.tema=s==='scuro'?'chiaro':'scuro';try{localStorage.setItem('tema',r.dataset.tema)}catch(e){}}
</script>"""

e = html.escape


def leggi_app():
    apps = []
    for f in sorted(APPS.rglob("app.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        cartella = f.parent.relative_to(RADICE).as_posix()
        d["cartella"] = cartella
        rel = f.parent.relative_to(APPS).parts
        d["categoria"] = rel[0]
        d["sottocategoria"] = rel[1] if len(rel) > 2 else None
        assert d["id"] == rel[-1], f"{f}: id diverso dal nome della cartella"
        assert d["tipo"] in TIPI, f"{f}: tipo sconosciuto {d['tipo']}"
        for p, _ in d.get("file", []) + d.get("allegati", []) + d.get("docente", []):
            assert (f.parent / p).exists(), f"{f}: manca {p}"
        if d.get("avvio"):
            assert (f.parent / d["avvio"]).exists(), f"{f}: manca {d['avvio']}"
        assert (f.parent / "README.md").exists(), f"{f.parent}: manca README.md"
        apps.append(d)
    ids = [a["id"] for a in apps]
    assert len(ids) == len(set(ids)), "due app con lo stesso id"
    for a in apps:
        for c in a.get("collegate", []):
            assert c in ids, f"{a['id']}: app collegata sconosciuta {c}"
    return apps


def nome_categoria(apps, chiave, livello):
    """Il nome leggibile viene da app.json (argomento), la chiave dal nome della cartella."""
    for a in apps:
        if livello == 0 and a["categoria"] == chiave:
            return a["argomento"][0]
        if livello == 1 and a["sottocategoria"] == chiave:
            return a["argomento"][1]
    return chiave


def albero(apps):
    cat = {}
    for a in apps:
        cat.setdefault(a["categoria"], {}).setdefault(a["sottocategoria"], []).append(a)
    ordine = ["meccanica", "termodinamica", "onde", "elettromagnetismo", "fisica-moderna",
              "astronomia", "matematica", "intelligenza-artificiale"]
    return sorted(cat.items(), key=lambda kv: (ordine.index(kv[0]) if kv[0] in ordine else 99, kv[0]))


def stroboscopio():
    """Traiettoria parabolica fotografata con un lampo ogni 0,1 s (come nella videoanalisi con Tracker)."""
    g, vx, vy, dt = 9.8, 3.1, 4.9, 0.1
    sx, sy, x0, y0 = 105, 105, 20, 230
    punti = []
    t = 0.0
    while True:
        x, y = vx * t, vy * t - g * t * t / 2
        if y < -0.02 and t > 0:
            break
        punti.append((x0 + sx * x, y0 - sy * y))
        t = round(t + dt, 10)
    w = int(punti[-1][0] + 30)
    cerchi = "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" style="--i:{i}"/>' for i, (px, py) in enumerate(punti))
    scia = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in punti)
    return (f'<svg class="strobo" viewBox="0 0 {w} 262" role="img" aria-label="Una pallina lanciata: '
            f'un punto ogni 0,1 secondi lungo una parabola">'
            f'<line class="suolo" x1="0" y1="{y0+8}" x2="{w}" y2="{y0+8}"/>'
            f'<path class="scia" d="{scia}"/>{cerchi}'
            f'<text x="{w}" y="{y0+28}" text-anchor="end">un punto ogni 0,1 s</text></svg>')


def nome_anno(n):
    return f"{n}º anno"


def scheda_url(a):
    return f'{a["cartella"]}/scheda.html'


def riga_app(a, base=""):
    tipo = TIPI[a["tipo"]][0]
    classi = f'<span class="classe">{e(nome_anno(a["anno"]))}</span>' if a.get("anno") else ""
    if a.get("docente"):
        classi += '<span>con materiali per il docente</span>'
    apri = ""
    if a.get("avvio"):
        apri = f'<a class="bottone pieno" href="{base}{a["cartella"]}/{a["avvio"]}">Apri l\'app</a>'
    elif a["tipo"] == "vpython":
        apri = f'<a class="bottone pieno" href="{base}{scheda_url(a)}#materiali">Prendi il codice</a>'
    else:
        apri = f'<a class="bottone pieno" href="{base}{scheda_url(a)}#materiali">Scarica le schede</a>'
    filtri = {
        "data-categoria": a["categoria"],
        "data-anno": str(a.get("anno") or ""),
        "data-tipo": a["tipo"],
        "data-testo": " ".join([a["titolo"], a["sommario"], a.get("tema", ""), *a["argomento"]]).lower(),
    }
    attr = " ".join(f'{k}="{e(v)}"' for k, v in filtri.items())
    return f"""<article class="app" {attr}>
  {ICONE[a['tipo']]}
  <div>
    <h4><a href="{base}{scheda_url(a)}">{e(a['titolo'])}</a></h4>
    <p>{e(a['sommario'])}</p>
    <div class="dati"><span>{e(tipo)}</span><span>{e(a.get('tema',''))}</span>{classi}</div>
    <div class="azioni">{apri}<a class="bottone" href="{base}{scheda_url(a)}">Come si usa</a></div>
  </div>
</article>"""


def pagina_indice(apps):
    alb = albero(apps)
    indice = "".join(
        f'<li><a href="#{k}">{e(nome_categoria(apps, k, 0))}</a> <small>{sum(len(v) for v in sub.values())}</small></li>'
        for k, sub in alb)
    sezioni = []
    for k, sub in alb:
        blocchi = []
        for s, lista in sorted(sub.items(), key=lambda kv: kv[0] or ""):
            titolo = f'<h3>{e(nome_categoria(apps, s, 1))}</h3>' if s else ""
            righe = "\n".join(riga_app(a) for a in sorted(lista, key=lambda a: a["titolo"]))
            blocchi.append(f'<div class="sotto">{titolo}{righe}</div>')
        sezioni.append(f'<section class="categoria" id="{k}" data-categoria="{k}"><h2>{e(nome_categoria(apps, k, 0))}</h2>{"".join(blocchi)}</section>')

    anni = sorted({a["anno"] for a in apps if a.get("anno")})
    def bottoni(nome, voci, tutte="Tutte"):
        b = [f'<button type="button" data-filtro="{nome}" data-valore="" aria-pressed="true">{tutte}</button>']
        b += [f'<button type="button" data-filtro="{nome}" data-valore="{e(v)}" aria-pressed="false">{e(t)}</button>' for v, t in voci]
        return "".join(b)
    f_cat = bottoni("categoria", [(k, nome_categoria(apps, k, 0)) for k, _ in alb])
    f_cla = bottoni("anno", [(str(n), nome_anno(n)) for n in anni], "Tutti")
    f_tip = bottoni("tipo", [(t, TIPI[t][0]) for t in TIPI if any(a["tipo"] == t for a in apps)])

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cg fill=%22%231d3d8f%22%3E%3Ccircle cx=%225%22 cy=%2226%22 r=%223%22/%3E%3Ccircle cx=%2212%22 cy=%2212%22 r=%223%22/%3E%3Ccircle cx=%2220%22 cy=%228%22 r=%223%22/%3E%3Ccircle cx=%2228%22 cy=%2216%22 r=%223%22/%3E%3C/g%3E%3C/svg%3E">
<title>App di fisica · Liceo «L. da Vinci» di Trento</title>
<meta name="description" content="Simulazioni, videoanalisi e schede di laboratorio per le lezioni di fisica, con le istruzioni per usarle in classe.">
{FONT}
<link rel="stylesheet" href="sito/stile.css">
{TEMA_JS}
</head>
<body>
<div class="pagina">
  <nav class="margine" aria-label="Argomenti">
    <a class="marchio" href="./">PhysicsApp</a>
    <ul class="indice">{indice}</ul>
    <button class="tema-btn" type="button" onclick="cambiaTema()">Carta o lavagna</button>
  </nav>
  <main class="foglio">
    <header class="testata">
      {stroboscopio()}
      <h1>App di fisica</h1>
      <p>Simulazioni, videoanalisi e schede di laboratorio costruite per le lezioni del prof. Massimo Bosetti al Liceo «L. da Vinci» di Trento. Ogni app ha le istruzioni per usarla in classe e, quando c'è, la lezione collegata.</p>
    </header>
    <div class="filtri" role="group" aria-label="Filtra le app">
      <div class="filtro"><span>Argomento</span>{f_cat}</div>
      <div class="filtro"><span>Anno</span>{f_cla}</div>
      <div class="filtro"><span>Tipo</span>{f_tip}</div>
      <div class="filtro"><span><label for="cerca">Cerca</label></span><input id="cerca" class="cerca" type="search" placeholder="velocità limite, forza centripeta…"></div>
    </div>
    <p class="vuoto" id="vuoto" hidden>Nessuna app con questi filtri. Togli un filtro o cambia la ricerca.</p>
    {''.join(sezioni)}
    <footer>{len(apps)} app. Il codice di tutte le app è nel repository <a href="{REPO}">MaxDvTn/PhysicsApp</a>.</footer>
  </main>
</div>
<script>
{{
const stato={{categoria:'',anno:'',tipo:'',testo:''}};
const app=[...document.querySelectorAll('.app')];
function aggiorna(){{
  let n=0;
  for(const a of app){{
    const ok=(!stato.categoria||a.dataset.categoria===stato.categoria)
      &&(!stato.anno||a.dataset.anno===stato.anno)
      &&(!stato.tipo||a.dataset.tipo===stato.tipo)
      &&(!stato.testo||a.dataset.testo.includes(stato.testo));
    a.hidden=!ok; if(ok)n++;
  }}
  document.querySelectorAll('.sotto,.categoria').forEach(s=>s.hidden=!s.querySelector('.app:not([hidden])'));
  document.getElementById('vuoto').hidden=n>0;
}}
document.querySelectorAll('[data-filtro]').forEach(b=>b.addEventListener('click',()=>{{
  stato[b.dataset.filtro]=b.dataset.valore;
  document.querySelectorAll(`[data-filtro="${{b.dataset.filtro}}"]`).forEach(x=>x.setAttribute('aria-pressed',x===b));
  aggiorna();
}}));
document.getElementById('cerca').addEventListener('input',e=>{{stato.testo=e.target.value.trim().toLowerCase();aggiorna()}});
}}
</script>
</body>
</html>
"""


def dimensione(p):
    n = p.stat().st_size
    return f"{n/1e6:.1f} MB".replace(".", ",") if n >= 1e6 else f"{max(1, round(n/1e3))} kB"


def pagina_scheda(a, apps):
    cartella = RADICE / a["cartella"]
    su = "../" * len(Path(a["cartella"]).parts)
    readme = (cartella / "README.md").read_text(encoding="utf-8")
    corpo = markdown.markdown(readme, extensions=["extra", "sane_lists"])
    corpo = corpo.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')

    azioni = []
    if a.get("avvio"):
        azioni.append(f'<a class="bottone pieno" href="{a["avvio"]}">Apri l\'app</a>')
    py = [p for p, _ in a.get("file", []) if p.endswith(".py")]
    if py:
        azioni.append(f'<button class="bottone pieno" type="button" data-copia="{e(py[0])}">Copia il codice e apri GlowScript</button>')
    if a.get("colab"):
        azioni.append(f'<a class="bottone" target="_blank" rel="noopener" href="https://colab.research.google.com/github/MaxDvTn/PhysicsApp/blob/main/{a["cartella"]}/{a["colab"]}">Apri in Colab</a>')
    azioni.append(f'<a class="bottone" href="{REPO}/tree/main/{a["cartella"]}">Codice su GitHub</a>')

    def voce(p, t):
        extra = ""
        if p.endswith(".py"):
            extra = f' <button class="bottone" type="button" data-copia="{e(p)}">Copia e apri GlowScript</button>'
        return f'<li><span><a href="{e(p)}" download>{e(t)}</a> <small>{e(Path(p).suffix[1:].upper())}, {dimensione(cartella / p)}</small></span>{extra}</li>'

    materiali = ""
    if a.get("file"):
        materiali += "<h2>File dell'app</h2><ul class=\"materiali\">" + "".join(voce(p, t) for p, t in a["file"]) + "</ul>"
    if a.get("allegati"):
        materiali += "<h2>Lezione collegata</h2><ul class=\"materiali\">" + "".join(
            f'<li><span><a href="{e(p)}">{e(t)}</a> <small>PDF, {dimensione(cartella / p)}</small></span></li>' for p, t in a["allegati"]) + "</ul>"
    if a.get("docente"):
        materiali += ('<h2 id="docente">Per il docente</h2><p>Versioni complete e soluzioni: '
                      'utili per preparare la lezione o per proiettarle. Agli studenti conviene dare prima le versioni da completare.</p>'
                      '<ul class="materiali docente">' + "".join(voce(p, t) for p, t in a["docente"]) + "</ul>")
    collegate = [b for b in apps if b["id"] in a.get("collegate", [])]
    if collegate:
        materiali += "<h2>App collegate</h2><ul class=\"materiali\">" + "".join(
            f'<li><a href="{su}{scheda_url(b)}">{e(b["titolo"])}</a><small>{e(TIPI[b["tipo"]][0])}</small></li>' for b in collegate) + "</ul>"

    classi = f'<span class="classe">{e(nome_anno(a["anno"]))}</span>' if a.get("anno") else "tutti"
    data = "/".join(reversed(a["data"].split("-")))
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cg fill=%22%231d3d8f%22%3E%3Ccircle cx=%225%22 cy=%2226%22 r=%223%22/%3E%3Ccircle cx=%2212%22 cy=%2212%22 r=%223%22/%3E%3Ccircle cx=%2220%22 cy=%228%22 r=%223%22/%3E%3Ccircle cx=%2228%22 cy=%2216%22 r=%223%22/%3E%3C/g%3E%3C/svg%3E">
<title>{e(a['titolo'])} · App di fisica</title>
<meta name="description" content="{e(a['sommario'])}">
{FONT}
<link rel="stylesheet" href="{su}sito/stile.css">
{TEMA_JS}
</head>
<body>
<div class="pagina">
  <aside class="margine">
    <a class="marchio" href="{su}index.html">PhysicsApp</a>
    <dl class="scheda-dati">
      <dt>Argomento</dt><dd>{e(' › '.join(a['argomento']))}<br>{e(a.get('tema',''))}</dd>
      <dt>Anno</dt><dd>{classi}</dd>
      <dt>Tipo</dt><dd>{e(TIPI[a['tipo']][0])}</dd>
      <dt>Data</dt><dd>{data}</dd>
    </dl>
    <button class="tema-btn" type="button" onclick="cambiaTema()">Carta o lavagna</button>
  </aside>
  <main class="foglio scheda">
    <p><a href="{su}index.html#{a['categoria']}">Torna a tutte le app</a></p>
    <h1>{e(a['titolo'])}</h1>
    <p class="lead">{e(a['sommario'])}</p>
    <div class="azioni">{''.join(azioni)}<span class="copiato" id="copiato" role="status"></span></div>
    <div class="testo">{corpo}</div>
    <div class="testo" id="materiali">{materiali}</div>
    <footer>Liceo «L. da Vinci» di Trento, prof. Massimo Bosetti.</footer>
  </main>
</div>
<script>
// Il codice si scarica subito, così al clic si copia e si apre GlowScript nello stesso gesto.
const codici={{}};
document.querySelectorAll('[data-copia]').forEach(b=>{{
  const f=b.dataset.copia;
  if(!(f in codici)) codici[f]=fetch(f).then(r=>r.ok?r.text():null).catch(()=>null).then(t=>codici[f]=t);
  b.addEventListener('click',()=>{{
    const msg=document.getElementById('copiato'), t=codici[f];
    const fatto=()=>msg.textContent='Codice copiato: su GlowScript scegli «Create New Program» e incollalo con Cmd+V o Ctrl+V.';
    const errore=()=>msg.textContent='Non sono riuscito a copiare: scarica il file qui sotto e incollalo a mano.';
    if(typeof t==='string'&&navigator.clipboard) navigator.clipboard.writeText(t).then(fatto,errore); else errore();
    window.open('https://glowscript.org/','_blank','noopener');
  }});
}});
</script>
</body>
</html>
"""


def readme_catalogo(apps):
    righe = []
    for k, sub in albero(apps):
        righe.append(f"\n### {nome_categoria(apps, k, 0)}\n")
        for s, lista in sorted(sub.items(), key=lambda kv: kv[0] or ""):
            if s:
                righe.append(f"\n**{nome_categoria(apps, s, 1)}**\n")
            righe.append("| App | Tipo | Anno | Cartella |\n|---|---|---|---|")
            for a in sorted(lista, key=lambda a: a["titolo"]):
                righe.append(f"| [{a['titolo']}]({SITO}{scheda_url(a)}) | {TIPI[a['tipo']][0]} | {nome_anno(a['anno']) if a.get('anno') else '–'} | [`{a['cartella']}`]({a['cartella']}) |")
    return "\n".join(righe).strip()


def main():
    controlla = "--controlla" in sys.argv
    apps = leggi_app()
    uscite = {
        RADICE / "catalogo.json": json.dumps(
            [{k: v for k, v in a.items()} for a in apps], ensure_ascii=False, indent=2) + "\n",
        RADICE / "index.html": pagina_indice(apps),
    }
    for a in apps:
        uscite[RADICE / a["cartella"] / "scheda.html"] = pagina_scheda(a, apps)
    rd = RADICE / "README.md"
    testo = rd.read_text(encoding="utf-8")
    ini, fin = "<!-- CATALOGO:INIZIO -->", "<!-- CATALOGO:FINE -->"
    if ini in testo:
        a_, b_ = testo.index(ini) + len(ini), testo.index(fin)
        uscite[rd] = testo[:a_] + "\n" + readme_catalogo(apps) + "\n" + testo[b_:]

    diversi = [p for p, t in uscite.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    if controlla:
        for p in diversi:
            print("da rigenerare:", p.relative_to(RADICE))
        print("OK: sito aggiornato" if not diversi else "Lancia: python3 strumenti/genera_sito.py")
        sys.exit(1 if diversi else 0)
    for p in diversi:
        p.write_text(uscite[p], encoding="utf-8")
        print("scritto:", p.relative_to(RADICE))
    print(f"{len(apps)} app, {len(diversi)} file aggiornati")


if __name__ == "__main__":
    main()
