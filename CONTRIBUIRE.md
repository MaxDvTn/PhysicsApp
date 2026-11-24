# Aggiungere un'app

1. **Scegli la cartella** per argomento: `apps/<categoria>/<sottocategoria>/<id-app>/`, con nomi in minuscolo e trattini (`apps/meccanica/dinamica/piano-inclinato/`). Se la categoria non esiste ancora, creala. La classe non va nel percorso: si scrive in `app.json`.
2. **Copia i file dell'app**: `index.html` per un'app nel browser (con eventuali video e immagini nella stessa cartella), i `.py` e il notebook per una simulazione VPython, i PDF per le schede.
3. **Allegati della lezione**: sintesi e slide in PDF vanno in `allegati/`. Solo prodotti finiti, mai sorgenti o dati degli studenti. Soluzioni e versioni complete vanno in `docente/`.
4. **Scrivi `app.json`**:

   ```json
   {
     "id": "piano-inclinato",
     "titolo": "Il piano inclinato",
     "tipo": "web",
     "avvio": "index.html",
     "sommario": "Una frase che dice che cosa fa l'app.",
     "argomento": ["Meccanica", "Dinamica"],
     "tema": "Forze e piano inclinato",
     "anno": 2,
     "data": "2026-12-01",
     "file": [],
     "allegati": [["allegati/sintesi_piano_inclinato.pdf", "Sintesi della lezione"]],
     "docente": [],
     "en": {
       "titolo": "The inclined plane",
       "sommario": "One sentence saying what the app does.",
       "tema": "Forces on an inclined plane",
       "argomento": ["Mechanics", "Dynamics"]
     },
     "collegate": []
   }
   ```

   - `tipo`: `web`, `vpython` o `schede`.
   - `avvio`: il file da aprire (solo per `web`), altrimenti `null`.
   - `file`, `allegati`, `docente`: voci `[percorso, descrizione in italiano, descrizione in inglese]`; per un file scritto in una sola lingua si aggiunge `"it"` o `"en"` come quarto elemento (il pulsante «Copia e apri GlowScript» sceglie lo script della lingua del sito).
   - `en`: titolo, sommario, tema e argomento in inglese.
   - `colab` (facoltativo): il notebook da aprire con il pulsante «Apri in Colab», per lingua: `{"it": "...ipynb", "en": "..._en.ipynb"}`.
   - `argomento`: categoria e sottocategoria, con i nomi da mostrare nel sito.
   - `anno`: l'anno di corso (1–5) per cui è pensata, oppure `null` se va bene per tutti.
   - `docente`: coppie `[percorso, descrizione]` dei materiali per il docente (versioni complete, soluzioni), messi nella sottocartella `docente/`. Nel sito stanno in una parte separata.
   - `collegate`: gli `id` delle app della stessa lezione.

5. **Scrivi `README.md` e `README.en.md`** con un titolo, due righe su che cos'è, la sezione `## Come si usa` (passi numerati, pensati per la classe) e, se serve, `## Da sapere` o `## Note`. `README.en.md` è la stessa cosa in inglese (`## How to use it`, `## Good to know`, `## Notes`).
6. **Rigenera il sito**: `python3 strumenti/genera_sito.py` (serve `pip install markdown`, oppure `uv run --with markdown python strumenti/genera_sito.py`). Il comando controlla anche che tutti i file citati esistano.
7. **Prima del commit**: `python3 strumenti/genera_sito.py --controlla` deve dire «OK». Poi commit e push: il sito si aggiorna da solo in un paio di minuti.

## Le app in due lingue

Ogni app web ha il commutatore italiano/inglese e la barra di navigazione (‹ Come si usa, sezione, Tutte le app) di `strumenti/lingua_snippet.html`: si incolla subito dopo `<body>` (tra i commenti `LINGUA:INIZIO` e `LINGUA:FINE`). Poi:

- ai testi fissi si aggiunge `data-en="testo inglese"` (il contenuto dell'elemento resta l'italiano); alle etichette per i lettori di schermo `data-en-label`;
- nel codice si usano `I18N.t('italiano', 'english')` per i testi e `I18N.num(x, cifre)` per i numeri (virgola in italiano, punto in inglese);
- l'app ridisegna quando arriva l'evento `lingua` (`window.addEventListener('lingua', ridisegna)`);
- alla fine si chiama `I18N.applica()`.

Per un'app con molti testi creati dal codice si può usare `I18N.dizionario({italiano: inglese}, [[RegExp, sostituzione]])`, che traduce anche i testi aggiunti dopo. La lingua è la stessa del sito (chiave `lingua` nel browser) e si può forzare con `?lang=en` o `?lang=it`.

## Regole per i materiali

- Vettori con il ket (`|v⟩`, modulo `|v|`) per 2P, 3P, 3R; con la freccia per la 5R.
- |g| = 9,8 m/s² nei problemi normali.
- Niente nomi di studenti, foto di studenti o dati personali, in nessun file.
