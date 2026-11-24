# Esploratore Clausius-Clapeyron

Una simulazione in due parti che accompagna la lezione «L'equazione della montagna e del clima» (dicembre 2025). Nella prima si sale di quota e si vede scendere la temperatura di ebollizione dell'acqua; nella seconda si riscalda l'atmosfera e si vede crescere il vapore che può contenere.

## Come si usa

1. **L'acqua bolle prima in quota.** Muovi il cursore della quota (da 0 a 8849 m) o usa i pulsanti Trento, Rifugio a 2500 m, Marmolada, Monte Bianco ed Everest. L'app calcola la pressione con l'atmosfera standard e la temperatura di ebollizione con l'equazione di Clausius-Clapeyron, e segna il punto sul grafico. Chiedi prima una previsione: a che temperatura bolle l'acqua in un rifugio? (A 2500 m circa 91,5 °C; sul Monte Bianco circa 83,6 °C.)
2. **Più caldo, più vapore.** Scegli la temperatura di partenza e il riscaldamento. Il grafico confronta la pressione di vapore saturo vera (formula di Buck) con due modelli: Clausius-Clapeyron con il calore latente costante e con il calore latente che cambia con la temperatura. Sotto ci sono gli aumenti percentuali.
3. Apri «Da dove viene il "7 % per grado"»: con L costante viene circa il 6 % a 15 °C; tenendo conto che a bassa temperatura L è più grande si ottiene il 7,5 % vicino a 0 °C e il 6–6,6 % tra 15 e 25 °C, come i dati veri.

Funziona nel browser, anche sul telefono e senza rete (a parte il carattere).

## Da sapere

- È la simulazione del dicembre 2025, rivista il 24/11/2026: prima il 7 % era usato come dato (1,07 elevato al riscaldamento), ora si calcola dall'equazione; i decimali sono con la virgola; «capacità di vapore» è diventato «pressione di vapore saturo».
- Il modello con L costante sbaglia anche il valore: a 15 °C dà 2,1 kPa contro 1,7 kPa veri. È un buon esempio di ipotesi da discutere.
- Meglio evitare l'idea dell'«aria come una spugna»: la pressione di vapore saturo dipende solo dalla temperatura e ci sarebbe anche senza aria.
