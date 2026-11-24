#!/usr/bin/env python3
"""Genera il sito e il catalogo di PhysicsApp a partire dalle cartelle in apps/.

Ogni app sta in apps/<categoria>/[<sottocategoria>/]<id>/ con:
  app.json      dati dell'app (titolo, tipo, anno, allegati, materiali del docente, testi in inglese)
  README.md     descrizione e istruzioni d'uso in italiano
  README.en.md  le stesse in inglese
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
    "web": ("App nel browser", "Browser app"),
    "vpython": ("Simulazione VPython", "VPython simulation"),
    "schede": ("Schede di laboratorio", "Lab worksheets"),
}
ICONE = {
    "web": '<svg class="icona" viewBox="0 0 32 32" aria-hidden="true"><rect x="3" y="5" width="26" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 10.5v9l7.5-4.5z" fill="currentColor"/></svg>',
    "vpython": '<svg class="icona" viewBox="0 0 32 32" aria-hidden="true"><path d="M11 6c-3 0-4 1.5-4 4v3c0 1.5-1 3-3 3 2 0 3 1.5 3 3v3c0 2.5 1 4 4 4M21 6c3 0 4 1.5 4 4v3c0 1.5 1 3 3 3-2 0-3 1.5-3 3v3c0 2.5-1 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2.5" fill="currentColor"/></svg>',
    "schede": '<svg class="icona" viewBox="0 0 32 32" aria-hidden="true"><path d="M8 3h11l6 6v20H8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 15h9M12 19h9M12 23h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
}
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">')
ICONA = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cg fill=%22%231d3d8f%22%3E'
         '%3Ccircle cx=%225%22 cy=%2226%22 r=%223%22/%3E%3Ccircle cx=%2212%22 cy=%2212%22 r=%223%22/%3E%3Ccircle cx=%2220%22 cy=%228%22 r=%223%22/%3E'
         '%3Ccircle cx=%2228%22 cy=%2216%22 r=%223%22/%3E%3C/g%3E%3C/svg%3E">')
# Tema e lingua si decidono nell'<head>, prima di disegnare la pagina. La lingua: ?lang=en|it,
# poi la scelta salvata (chiave «lingua», la stessa delle app), poi la lingua del browser.
TESTA_JS = """<script>
(function(){var r=document.documentElement;
try{var t=localStorage.getItem('tema');if(t)r.dataset.tema=t}catch(e){}
var l=null;try{var q=new URLSearchParams(location.search).get('lang');if(q==='en'||q==='it'){l=q;localStorage.setItem('lingua',q)}else{var s=localStorage.getItem('lingua');if(s==='en'||s==='it')l=s}}catch(e){}
if(!l)l=/^it/i.test(navigator.language||'it')?'it':'en';r.lang=l;})();
function cambiaTema(){var r=document.documentElement,s=r.dataset.tema||(matchMedia('(prefers-color-scheme: dark)').matches?'scuro':'chiaro');
r.dataset.tema=s==='scuro'?'chiaro':'scuro';try{localStorage.setItem('tema',r.dataset.tema)}catch(e){}}
function cambiaLingua(){var r=document.documentElement;r.lang=r.lang==='en'?'it':'en';try{localStorage.setItem('lingua',r.lang)}catch(e){}aggiornaTitolo()}
function aggiornaTitolo(){var r=document.documentElement,t=r.dataset['titolo'+(r.lang==='en'?'En':'It')];if(t)document.title=t}
document.addEventListener('DOMContentLoaded',aggiornaTitolo);
</script>"""

e = html.escape


def bi(it, en, tag="span", attr=""):
    """Lo stesso testo nelle due lingue: il CSS mostra solo quella scelta."""
    a = f" {attr}" if attr else ""
    if it == en:
        return f"<{tag}{a}>{e(it)}</{tag}>" if tag != "span" or attr else e(it)
    return f'<{tag}{a} data-l="it">{e(it)}</{tag}><{tag}{a} data-l="en">{e(en)}</{tag}>'


def bih(it, en):
    """Come bi(), ma con HTML già pronto (non viene ripulito)."""
    return f'<div data-l="it">{it}</div><div data-l="en">{en}</div>'


def EN(a, k):
    return a.get("en", {}).get(k, a.get(k))


def voci(lista):
    """Le voci di file, allegati e docente: [percorso, etichetta it, etichetta en, (lingua)]."""
    out = []
    for x in lista:
        out.append({"p": x[0], "it": x[1], "en": x[2] if len(x) > 2 else x[1], "lingua": x[3] if len(x) > 3 else None})
    return out


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
        assert "en" in d and all(k in d["en"] for k in ("titolo", "sommario", "argomento")), f"{f}: mancano i testi inglesi (campo en)"
        for k in ("file", "allegati", "docente"):
            for v in d.get(k, []):
                assert 2 <= len(v) <= 4, f"{f}: voce di {k} non valida {v}"
                assert (f.parent / v[0]).exists(), f"{f}: manca {v[0]}"
        colab = d.get("colab")
        if isinstance(colab, str):
            d["colab"] = {"it": colab}
        for c in (d.get("colab") or {}).values():
            assert (f.parent / c).exists(), f"{f}: manca {c}"
        if d.get("avvio"):
            assert (f.parent / d["avvio"]).exists(), f"{f}: manca {d['avvio']}"
        for r in ("README.md", "README.en.md"):
            assert (f.parent / r).exists(), f"{f.parent}: manca {r}"
        apps.append(d)
    ids = [a["id"] for a in apps]
    assert len(ids) == len(set(ids)), "due app con lo stesso id"
    for a in apps:
        for c in a.get("collegate", []):
            assert c in ids, f"{a['id']}: app collegata sconosciuta {c}"
    return apps


def nome_categoria(apps, chiave, livello, lingua="it"):
    """Il nome leggibile viene da app.json (argomento), la chiave dal nome della cartella."""
    for a in apps:
        arg = a["argomento"] if lingua == "it" else a["en"]["argomento"]
        if livello == 0 and a["categoria"] == chiave:
            return arg[0]
        if livello == 1 and a["sottocategoria"] == chiave:
            return arg[1]
    return chiave


def bi_cat(apps, chiave, livello, tag="span", attr=""):
    return bi(nome_categoria(apps, chiave, livello), nome_categoria(apps, chiave, livello, "en"), tag, attr)


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
            f'<text x="{w}" y="{y0+28}" text-anchor="end" data-l="it">un punto ogni 0,1 s</text>'
            f'<text x="{w}" y="{y0+28}" text-anchor="end" data-l="en">one dot every 0.1 s</text></svg>')


def nome_anno(n, lingua="it"):
    if lingua == "en":
        return f"Year {n}"
    return f"{n}º anno"


def bi_anno(n, tag="span", attr=""):
    return bi(nome_anno(n), nome_anno(n, "en"), tag, attr)


def scheda_url(a):
    return f'{a["cartella"]}/scheda.html'


def riga_app(a, base=""):
    dati = bi(*TIPI[a["tipo"]], "span") + bi(a.get("tema", ""), EN(a, "tema"), "span")
    if a.get("anno"):
        dati += bi_anno(a["anno"], "span", 'class="classe"')
    if a.get("docente"):
        dati += bi("con materiali per il docente", "with teacher's materials", "span")
    if a.get("avvio"):
        apri = f'<a class="bottone pieno" href="{base}{a["cartella"]}/{a["avvio"]}">{bi("Apri l’app", "Open the app")}</a>'
    elif a["tipo"] == "vpython":
        apri = f'<a class="bottone pieno" href="{base}{scheda_url(a)}#materiali">{bi("Prendi il codice", "Get the code")}</a>'
    else:
        apri = f'<a class="bottone pieno" href="{base}{scheda_url(a)}#materiali">{bi("Scarica le schede", "Download the worksheets")}</a>'
    testo = [a["titolo"], a["sommario"], a.get("tema", ""), *a["argomento"],
             a["en"]["titolo"], a["en"]["sommario"], EN(a, "tema") or "", *a["en"]["argomento"]]
    filtri = {
        "data-categoria": a["categoria"],
        "data-anno": str(a.get("anno") or ""),
        "data-tipo": a["tipo"],
        "data-testo": " ".join(testo).lower(),
    }
    attr = " ".join(f'{k}="{e(v)}"' for k, v in filtri.items())
    return f"""<article class="app" {attr}>
  {ICONE[a['tipo']]}
  <div>
    <h4><a href="{base}{scheda_url(a)}">{bi(a['titolo'], a['en']['titolo'])}</a></h4>
    {bi(a['sommario'], a['en']['sommario'], 'p')}
    <div class="dati">{dati}</div>
    <div class="azioni">{apri}<a class="bottone" href="{base}{scheda_url(a)}">{bi("Come si usa", "How to use it")}</a></div>
  </div>
</article>"""


def bottone_lingua():
    return ('<button class="tema-btn lingua-btn" type="button" onclick="cambiaLingua()">'
            '<span data-l="it" lang="en">English</span><span data-l="en" lang="it">Italiano</span></button>')


def pagina_indice(apps):
    alb = albero(apps)
    indice = "".join(
        f'<li><a href="#{k}">{bi_cat(apps, k, 0)}</a> <small>{sum(len(v) for v in sub.values())}</small></li>'
        for k, sub in alb)
    sezioni = []
    for k, sub in alb:
        blocchi = []
        for s, lista in sorted(sub.items(), key=lambda kv: kv[0] or ""):
            titolo = bi_cat(apps, s, 1, "h3") if s else ""
            righe = "\n".join(riga_app(a) for a in sorted(lista, key=lambda a: a["titolo"]))
            blocchi.append(f'<div class="sotto">{titolo}{righe}</div>')
        sezioni.append(f'<section class="categoria" id="{k}" data-categoria="{k}">{bi_cat(apps, k, 0, "h2")}{"".join(blocchi)}</section>')

    anni = sorted({a["anno"] for a in apps if a.get("anno")})
    def bottoni(nome, voci_, tutte=("Tutte", "All")):
        b = [f'<button type="button" data-filtro="{nome}" data-valore="" aria-pressed="true">{bi(*tutte)}</button>']
        b += [f'<button type="button" data-filtro="{nome}" data-valore="{e(v)}" aria-pressed="false">{t}</button>' for v, t in voci_]
        return "".join(b)
    f_cat = bottoni("categoria", [(k, bi_cat(apps, k, 0)) for k, _ in alb])
    f_cla = bottoni("anno", [(str(n), bi_anno(n)) for n in anni], ("Tutti", "All"))
    f_tip = bottoni("tipo", [(t, bi(*TIPI[t])) for t in TIPI if any(a["tipo"] == t for a in apps)])
    titolo_it, titolo_en = "App di fisica · Liceo «L. da Vinci» di Trento", "Physics apps · Liceo «L. da Vinci», Trento"

    return f"""<!DOCTYPE html>
<html lang="it" data-titolo-it="{e(titolo_it)}" data-titolo-en="{e(titolo_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ICONA}
<title>{e(titolo_it)}</title>
<meta name="description" content="Simulazioni, videoanalisi e schede di laboratorio per le lezioni di fisica, con le istruzioni per usarle in classe. Physics simulations, video analyses and lab worksheets, in Italian and English.">
{FONT}
<link rel="stylesheet" href="sito/stile.css">
{TESTA_JS}
</head>
<body>
<div class="pagina">
  <nav class="margine" aria-label="Argomenti / Topics">
    <a class="marchio" href="./">PhysicsApp</a>
    <ul class="indice">{indice}</ul>
    <div class="comandi">{bottone_lingua()}<button class="tema-btn" type="button" onclick="cambiaTema()">{bi("Carta o lavagna", "Paper or blackboard")}</button></div>
  </nav>
  <main class="foglio">
    <header class="testata">
      {stroboscopio()}
      {bi("App di fisica", "Physics apps", "h1")}
      {bi("Simulazioni, videoanalisi e schede di laboratorio costruite per le lezioni del prof. Massimo Bosetti al Liceo «L. da Vinci» di Trento. Ogni app ha le istruzioni per usarla in classe e, quando c'è, la lezione collegata. Le app sono in italiano e in inglese.",
          "Simulations, video analyses and lab worksheets built for Prof. Massimo Bosetti's physics lessons at the Liceo «L. da Vinci» in Trento, Italy. Every app comes with instructions for using it in class and, where there is one, the related lesson. The apps are in Italian and in English.", "p")}
    </header>
    <div class="filtri" role="group" aria-label="Filtra le app / Filter the apps">
      <div class="filtro">{bi("Argomento", "Topic")}{f_cat}</div>
      <div class="filtro">{bi("Anno", "Year")}{f_cla}</div>
      <div class="filtro">{bi("Tipo", "Type")}{f_tip}</div>
      <div class="filtro"><label for="cerca">{bi("Cerca", "Search")}</label><input id="cerca" class="cerca" type="search" data-segnaposto-it="velocità limite, forza centripeta…" data-segnaposto-en="terminal velocity, centripetal force…"></div>
    </div>
    {bi("Nessuna app con questi filtri. Togli un filtro o cambia la ricerca.", "No apps match these filters. Remove a filter or change the search.", "p", 'class="vuoto" id="vuoto" hidden')}
    {''.join(sezioni)}
    <footer>{bi(f"{len(apps)} app. Il codice di tutte le app è nel repository", f"{len(apps)} apps. The code of every app is in the repository")} <a href="{REPO}">MaxDvTn/PhysicsApp</a>.</footer>
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
  document.querySelectorAll('.vuoto').forEach(v=>v.hidden=n>0);
}}
document.querySelectorAll('[data-filtro]').forEach(b=>b.addEventListener('click',()=>{{
  stato[b.dataset.filtro]=b.dataset.valore;
  document.querySelectorAll(`[data-filtro="${{b.dataset.filtro}}"]`).forEach(x=>x.setAttribute('aria-pressed',x===b));
  aggiorna();
}}));
const cerca=document.getElementById('cerca');
cerca.addEventListener('input',e=>{{stato.testo=e.target.value.trim().toLowerCase();aggiorna()}});
const segnaposto=()=>{{cerca.placeholder=cerca.dataset[document.documentElement.lang==='en'?'segnapostoEn':'segnapostoIt']}};
segnaposto();new MutationObserver(segnaposto).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
}}
</script>
</body>
</html>
"""


def dimensione(p, lingua="it"):
    n = p.stat().st_size
    if n >= 1e6:
        s = f"{n/1e6:.1f} MB"
        return s if lingua == "en" else s.replace(".", ",")
    return f"{max(1, round(n/1e3))} kB"


def readme_html(cartella, nome):
    corpo = markdown.markdown((cartella / nome).read_text(encoding="utf-8"), extensions=["extra", "sane_lists"])
    return corpo.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')


def pagina_scheda(a, apps):
    cartella = RADICE / a["cartella"]
    su = "../" * len(Path(a["cartella"]).parts)
    corpo = bih(readme_html(cartella, "README.md"), readme_html(cartella, "README.en.md"))
    tutti = voci(a.get("file", []))

    def py_di(lingua):
        """Lo script per studenti da copiare: quello della lingua scelta, se c'è."""
        py = [v["p"] for v in tutti if v["p"].endswith(".py")]
        adatti = [v["p"] for v in tutti if v["p"].endswith(".py") and v["lingua"] in (None, lingua)]
        return (adatti or py or [None])[0]

    azioni = []
    if a.get("avvio"):
        azioni.append(f'<a class="bottone pieno" href="{a["avvio"]}">{bi("Apri l’app", "Open the app")}</a>')
    for lingua, testo in (("it", "Copia il codice e apri GlowScript"), ("en", "Copy the code and open GlowScript")):
        p = py_di(lingua)
        if p:
            azioni.append(f'<button class="bottone pieno" type="button" data-l="{lingua}" data-copia="{e(p)}">{testo}</button>')
    colab = a.get("colab") or {}
    for lingua, testo in (("it", "Apri in Colab"), ("en", "Open in Colab")):
        c = colab.get(lingua) or colab.get("it")
        if c:
            azioni.append(f'<a class="bottone" data-l="{lingua}" target="_blank" rel="noopener" '
                          f'href="https://colab.research.google.com/github/MaxDvTn/PhysicsApp/blob/main/{a["cartella"]}/{c}">{testo}</a>')
    azioni.append(f'<a class="bottone" href="{REPO}/tree/main/{a["cartella"]}">{bi("Codice su GitHub", "Code on GitHub")}</a>')

    def voce(v):
        extra = ""
        if v["p"].endswith(".py"):
            extra = f' <button class="bottone" type="button" data-copia="{e(v["p"])}">{bi("Copia e apri GlowScript", "Copy and open GlowScript")}</button>'
        tipo = e(Path(v["p"]).suffix[1:].upper())
        dim = f'<small data-l="it">{tipo}, {dimensione(cartella / v["p"])}</small><small data-l="en">{tipo}, {dimensione(cartella / v["p"], "en")}</small>'
        return f'<li><span><a href="{e(v["p"])}" download>{bi(v["it"], v["en"])}</a> {dim}</span>{extra}</li>'

    materiali = ""
    if tutti:
        materiali += bi("File dell'app", "App files", "h2") + '<ul class="materiali">' + "".join(voce(v) for v in tutti) + "</ul>"
    if a.get("allegati"):
        materiali += bi("Lezione collegata", "Related lesson", "h2") + '<ul class="materiali">' + "".join(voce(v) for v in voci(a["allegati"])) + "</ul>"
    if a.get("docente"):
        materiali += (bi("Per il docente", "For the teacher", "h2", 'id="docente"')
                      + bi("Versioni complete e soluzioni: utili per preparare la lezione o per proiettarle. Agli studenti conviene dare prima le versioni da completare.",
                           "Complete versions and solutions: useful for preparing the lesson or for projecting. It is better to give students the versions to complete first.", "p")
                      + '<ul class="materiali docente">' + "".join(voce(v) for v in voci(a["docente"])) + "</ul>")
    collegate = [b for b in apps if b["id"] in a.get("collegate", [])]
    if collegate:
        materiali += bi("App collegate", "Related apps", "h2") + '<ul class="materiali">' + "".join(
            f'<li><a href="{su}{scheda_url(b)}">{bi(b["titolo"], b["en"]["titolo"])}</a><small>{bi(*TIPI[b["tipo"]])}</small></li>' for b in collegate) + "</ul>"

    anno = bi_anno(a["anno"], "span", 'class="classe"') if a.get("anno") else bi("tutti", "all")
    data = "/".join(reversed(a["data"].split("-")))
    arg = bi(" › ".join(a["argomento"]), " › ".join(a["en"]["argomento"])) + "<br>" + bi(a.get("tema", ""), EN(a, "tema") or "")
    t_it, t_en = f"{a['titolo']} · App di fisica", f"{a['en']['titolo']} · Physics apps"
    return f"""<!DOCTYPE html>
<html lang="it" data-titolo-it="{e(t_it)}" data-titolo-en="{e(t_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ICONA}
<title>{e(t_it)}</title>
<meta name="description" content="{e(a['sommario'])}">
{FONT}
<link rel="stylesheet" href="{su}sito/stile.css">
{TESTA_JS}
</head>
<body>
<div class="pagina">
  <aside class="margine">
    <a class="marchio" href="{su}index.html">PhysicsApp</a>
    <dl class="scheda-dati">
      <dt>{bi("Argomento", "Topic")}</dt><dd>{arg}</dd>
      <dt>{bi("Anno", "Year")}</dt><dd>{anno}</dd>
      <dt>{bi("Tipo", "Type")}</dt><dd>{bi(*TIPI[a['tipo']])}</dd>
      <dt>{bi("Data", "Date")}</dt><dd>{data}</dd>
    </dl>
    <div class="comandi">{bottone_lingua()}<button class="tema-btn" type="button" onclick="cambiaTema()">{bi("Carta o lavagna", "Paper or blackboard")}</button></div>
  </aside>
  <main class="foglio scheda">
    <p><a href="{su}index.html#{a['categoria']}">{bi("Torna a tutte le app", "Back to all the apps")}</a></p>
    {bi(a['titolo'], a['en']['titolo'], 'h1')}
    {bi(a['sommario'], a['en']['sommario'], 'p', 'class="lead"')}
    <div class="azioni">{''.join(azioni)}<span class="copiato" id="copiato" role="status"></span></div>
    <div class="testo">{corpo}</div>
    <div class="testo" id="materiali">{materiali}</div>
    <footer>{bi("Liceo «L. da Vinci» di Trento, prof. Massimo Bosetti.", "Liceo «L. da Vinci», Trento, Prof. Massimo Bosetti.")}</footer>
  </main>
</div>
<script>
// Il codice si scarica subito, così al clic si copia e si apre GlowScript nello stesso gesto.
const codici={{}};
document.querySelectorAll('[data-copia]').forEach(b=>{{
  const f=b.dataset.copia;
  if(!(f in codici)) codici[f]=fetch(f).then(r=>r.ok?r.text():null).catch(()=>null).then(t=>codici[f]=t);
  b.addEventListener('click',()=>{{
    const msg=document.getElementById('copiato'), t=codici[f], en=document.documentElement.lang==='en';
    const fatto=()=>msg.textContent=en?'Code copied: on GlowScript choose “Create New Program” and paste it with Cmd+V or Ctrl+V.':'Codice copiato: su GlowScript scegli «Create New Program» e incollalo con Cmd+V o Ctrl+V.';
    const errore=()=>msg.textContent=en?'Could not copy: download the file below and paste it by hand.':'Non sono riuscito a copiare: scarica il file qui sotto e incollalo a mano.';
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
        righe.append(f"\n### {nome_categoria(apps, k, 0)} · {nome_categoria(apps, k, 0, 'en')}\n")
        for s, lista in sorted(sub.items(), key=lambda kv: kv[0] or ""):
            if s:
                righe.append(f"\n**{nome_categoria(apps, s, 1)} · {nome_categoria(apps, s, 1, 'en')}**\n")
            righe.append("| App | English | Tipo / Type | Anno / Year | Cartella / Folder |\n|---|---|---|---|---|")
            for a in sorted(lista, key=lambda a: a["titolo"]):
                anno = f"{a['anno']}" if a.get("anno") else "–"
                righe.append(f"| [{a['titolo']}]({SITO}{scheda_url(a)}) | [{a['en']['titolo']}]({SITO}{scheda_url(a)}?lang=en) | "
                             f"{TIPI[a['tipo']][0]} / {TIPI[a['tipo']][1]} | {anno} | [`{a['cartella']}`]({a['cartella']}) |")
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
