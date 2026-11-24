# Somme di sigmoidi

Un neurone con un peso grande è quasi un gradino; tanti gradini disegnano qualsiasi funzione continua. È l'idea del teorema di approssimazione universale, qui in tre schede da esplorare.

## Come si usa

1. **Un neurone.** Muovi i cursori di peso, posizione e altezza di ogni neurone c·σ(w(x − m)) e guarda come cambia la somma. Scegli una sfida (una gobba, una scala, un gradino in giù) e muovi i cursori finché la curva verde copre quella rossa: sotto 0,15 di errore la sfida è vinta.
2. **La dimostrazione.** Segui la costruzione passo per passo con i pulsanti Griglia, Scala, Rete e Neuroni. Scegli la funzione (o scrivila tu, con x, sin, cos, exp, abs, sqrt, log) e il numero N di neuroni; «Usa il w del teorema» imposta il peso che la dimostrazione garantisce.
3. **Addestramento.** Premi **Avvia**: una rete si addestra nel browser con la discesa del gradiente (Adam). Confronta la rete addestrata con quella costruita a mano con lo stesso numero di neuroni, cambia attivazione (sigmoide o ReLU), numero di campioni e rumore.

## Da osservare

- Di solito la rete addestrata batte quella costruita con lo stesso N, perché usa pesi diversi per ogni neurone e mette i gradini dove servono.
- Con «Mostra [−6, 6]» si vede che fuori dall'intervallo dei dati non c'è alcuna garanzia.
- Con pochi campioni, rumore e molti neuroni compare il sovradattamento: la rete segue anche gli errori dei dati.

Tutto il calcolo avviene nel browser: non serve connessione oltre al caricamento della pagina.
