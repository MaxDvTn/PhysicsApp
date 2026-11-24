# Aggiungere un'app

1. **Scegli la cartella** per argomento: `apps/<categoria>/<sottocategoria>/<id-app>/`, con nomi in minuscolo e trattini (`apps/meccanica/dinamica/piano-inclinato/`). Se la categoria non esiste ancora, creala. La classe non va nel percorso: si scrive in `app.json`.
2. **Copia i file dell'app**: `index.html` per un'app nel browser (con eventuali video e immagini nella stessa cartella), i `.py` e il notebook per una simulazione VPython, i PDF per le schede.
3. **Allegati della lezione**: sintesi e slide in PDF vanno in `allegati/`. Solo prodotti finiti, mai sorgenti, soluzioni riservate al docente o dati degli studenti.
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
     "classi": ["2P"],
     "anno": 2,
     "data": "2026-12-01",
     "file": [],
     "allegati": [["allegati/sintesi_piano_inclinato.pdf", "Sintesi della lezione"]],
     "collegate": []
   }
   ```

   - `tipo`: `web`, `vpython` o `schede`.
   - `avvio`: il file da aprire (solo per `web`), altrimenti `null`.
   - `file`: coppie `[percorso, descrizione]` dei file da scaricare (script, notebook, schede).
   - `colab` (facoltativo): il notebook da aprire con il pulsante «Apri in Colab».
   - `argomento`: categoria e sottocategoria, con i nomi da mostrare nel sito.
   - `collegate`: gli `id` delle app della stessa lezione.

5. **Scrivi `README.md`** con un titolo, due righe su che cos'è, la sezione `## Come si usa` (passi numerati, pensati per la classe) e, se serve, `## Da sapere` o `## Note`.
6. **Rigenera il sito**: `python3 strumenti/genera_sito.py` (serve `pip install markdown`, oppure `uv run --with markdown python strumenti/genera_sito.py`). Il comando controlla anche che tutti i file citati esistano.
7. **Prima del commit**: `python3 strumenti/genera_sito.py --controlla` deve dire «OK». Poi commit e push: il sito si aggiorna da solo in un paio di minuti.

## Regole per i materiali

- Vettori con il ket (`|v⟩`, modulo `|v|`) per 2P, 3P, 3R; con la freccia per la 5R.
- |g| = 9,8 m/s² nei problemi normali.
- Niente nomi di studenti, foto di studenti o dati personali, in nessun file.
