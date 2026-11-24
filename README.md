# PhysicsApp

*In Italian and English. Physics apps built for the lessons of Prof. Massimo Bosetti at the Liceo «L. da Vinci» in Trento, Italy: browser simulations, video analyses, VPython programs and lab worksheets, each with instructions for using it in class. Website: https://maxdvtn.github.io/PhysicsApp/?lang=en*

Le app di fisica costruite per le lezioni del prof. Massimo Bosetti al Liceo «L. da Vinci» di Trento: simulazioni nel browser, videoanalisi, programmi VPython e schede di laboratorio. Ogni app ha le istruzioni per usarla in classe e, quando c'è, la lezione collegata (sintesi e slide in PDF).

**Sito:** https://maxdvtn.github.io/PhysicsApp/

## Come è organizzato

```
apps/
  <categoria>/                 meccanica, astronomia, matematica, intelligenza-artificiale…
    <sottocategoria>/          cinematica, dinamica… (solo dove serve)
      <app>/
        app.json               titolo, tipo, classi, file e allegati
        README.md              che cos'è e come si usa
        README.en.md           lo stesso, in inglese
        index.html             l'app (per le app nel browser)
        scheda.html            pagina del sito con le istruzioni (generata)
        allegati/              sintesi e slide della lezione, in PDF
        docente/               versioni complete e soluzioni, per il docente
sito/stile.css                 aspetto del sito
strumenti/genera_sito.py       genera index.html, le schede, catalogo.json e l'elenco qui sotto
strumenti/lingua_snippet.html  commutatore italiano/inglese da incollare nelle app
catalogo.json                  elenco di tutte le app (generato)
```

Le categorie seguono l'argomento; l'anno di corso è un'etichetta, così la stessa app può servire a più classi. Nel sito si filtra per argomento, anno e tipo. I materiali per il docente (versioni complete delle simulazioni, soluzioni) stanno nella sottocartella `docente/` di ogni app e, nel sito, in una parte separata della scheda.

Sito, schede e app sono in italiano e in inglese: il pulsante «English / Italiano» cambia lingua ovunque, e la scelta resta per tutte le pagine. Le slide e le sintesi in PDF sono in italiano.

Tre tipi di app:

- **App nel browser**: si apre e funziona subito, anche sul telefono.
- **Simulazione VPython**: codice da incollare su [glowscript.org](https://glowscript.org) (o notebook per Google Colab), di solito in due versioni: da completare per gli studenti e completa per il docente (in `docente/`).
- **Schede di laboratorio**: schede PDF da seguire passo per passo.

## Le app

<!-- CATALOGO:INIZIO -->
### Meccanica · Mechanics


**Cinematica · Kinematics**

| App | English | Tipo / Type | Anno / Year | Cartella / Folder |
|---|---|---|---|---|
| [Il tiro impossibile](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/cinematica/tiro-impossibile/scheda.html) | [The impossible shot](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/cinematica/tiro-impossibile/scheda.html?lang=en) | Schede di laboratorio / Lab worksheets | 3 | [`apps/meccanica/cinematica/tiro-impossibile`](apps/meccanica/cinematica/tiro-impossibile) |

**Dinamica · Dynamics**

| App | English | Tipo / Type | Anno / Year | Cartella / Folder |
|---|---|---|---|---|
| [Dal poligono al cerchio](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/dal-poligono-al-cerchio/scheda.html) | [From polygon to circle](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/dal-poligono-al-cerchio/scheda.html?lang=en) | App nel browser / Browser app | 3 | [`apps/meccanica/dinamica/dal-poligono-al-cerchio`](apps/meccanica/dinamica/dal-poligono-al-cerchio) |
| [Forza sempre perpendicolare alla velocità (VPython)](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/forza-centripeta-vpython/scheda.html) | [A force always perpendicular to the velocity (VPython)](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/forza-centripeta-vpython/scheda.html?lang=en) | Simulazione VPython / VPython simulation | 3 | [`apps/meccanica/dinamica/forza-centripeta-vpython`](apps/meccanica/dinamica/forza-centripeta-vpython) |
| [La pallina da golf nell'olio](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/pallina-nell-olio/scheda.html) | [The golf ball in oil](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/pallina-nell-olio/scheda.html?lang=en) | App nel browser / Browser app | 3 | [`apps/meccanica/dinamica/pallina-nell-olio`](apps/meccanica/dinamica/pallina-nell-olio) |
| [Sferetta nella glicerina (VPython)](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/attrito-viscoso-vpython/scheda.html) | [Small ball in glycerine (VPython)](https://maxdvtn.github.io/PhysicsApp/apps/meccanica/dinamica/attrito-viscoso-vpython/scheda.html?lang=en) | Simulazione VPython / VPython simulation | 3 | [`apps/meccanica/dinamica/attrito-viscoso-vpython`](apps/meccanica/dinamica/attrito-viscoso-vpython) |

### Termodinamica · Thermodynamics

| App | English | Tipo / Type | Anno / Year | Cartella / Folder |
|---|---|---|---|---|
| [Esploratore Clausius-Clapeyron](https://maxdvtn.github.io/PhysicsApp/apps/termodinamica/clausius-clapeyron/scheda.html) | [Clausius-Clapeyron explorer](https://maxdvtn.github.io/PhysicsApp/apps/termodinamica/clausius-clapeyron/scheda.html?lang=en) | App nel browser / Browser app | 4 | [`apps/termodinamica/clausius-clapeyron`](apps/termodinamica/clausius-clapeyron) |

### Astronomia · Astronomy

| App | English | Tipo / Type | Anno / Year | Cartella / Folder |
|---|---|---|---|---|
| [Giorno solare e giorno siderale](https://maxdvtn.github.io/PhysicsApp/apps/astronomia/giorno-solare-siderale/scheda.html) | [Solar day and sidereal day](https://maxdvtn.github.io/PhysicsApp/apps/astronomia/giorno-solare-siderale/scheda.html?lang=en) | App nel browser / Browser app | 3 | [`apps/astronomia/giorno-solare-siderale`](apps/astronomia/giorno-solare-siderale) |

### Matematica · Mathematics

| App | English | Tipo / Type | Anno / Year | Cartella / Folder |
|---|---|---|---|---|
| [La mappa della dimostrazione di Riemann](https://maxdvtn.github.io/PhysicsApp/apps/matematica/mappa-riemann/scheda.html) | [A map of the Riemann proof](https://maxdvtn.github.io/PhysicsApp/apps/matematica/mappa-riemann/scheda.html?lang=en) | App nel browser / Browser app | – | [`apps/matematica/mappa-riemann`](apps/matematica/mappa-riemann) |

### Intelligenza artificiale · Artificial intelligence

| App | English | Tipo / Type | Anno / Year | Cartella / Folder |
|---|---|---|---|---|
| [Somme di sigmoidi](https://maxdvtn.github.io/PhysicsApp/apps/intelligenza-artificiale/somme-di-sigmoidi/scheda.html) | [Sums of sigmoids](https://maxdvtn.github.io/PhysicsApp/apps/intelligenza-artificiale/somme-di-sigmoidi/scheda.html?lang=en) | App nel browser / Browser app | – | [`apps/intelligenza-artificiale/somme-di-sigmoidi`](apps/intelligenza-artificiale/somme-di-sigmoidi) |
<!-- CATALOGO:FINE -->

## Aggiungere un'app

Vedi [CONTRIBUIRE.md](CONTRIBUIRE.md).

## Licenza

Il codice è distribuito con licenza MIT (vedi [LICENSE](LICENSE)). Video, schede e slide sono materiali didattici del prof. Massimo Bosetti: si possono usare a scuola citando la fonte. Le simulazioni esterne collegate da alcune app appartengono ai rispettivi autori.
