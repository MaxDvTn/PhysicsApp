# Forza sempre perpendicolare alla velocità (VPython)

Una pallina di massa m parte con velocità v₀. Su di lei agisce una forza di modulo costante, ricalcolata a ogni passo perpendicolare alla velocità. Il risultato è una traiettoria circolare con |v| costante, raggio r = m v₀²/F e periodo T = 2πr/v₀. Il pulsante **Taglia il filo** toglie la forza e la pallina parte lungo la tangente.

## Come si usa

**Nel browser, senza installare niente (consigliato).**

1. Apri [glowscript.org](https://glowscript.org), accedi e scegli **Create New Program**.
2. Incolla tutto il file `.py`. La prima riga deve restare `Web VPython 3.2`.
3. Premi **Run**.

**Versione studenti.** `forza_centripeta_studenti.py` si completa un passo alla volta: completa le righe con `# TODO`, lancia, osserva e rispondi alle domande nei commenti. In cima ci sono i parametri (massa, forza, velocità iniziale, passo temporale) da cambiare per le prove.

**Versione completa.** `forza_centripeta_completo.py` è la simulazione finita, da proiettare.

**In Google Colab.** Il notebook `forza_centripeta_colab.ipynb` usa lo stesso metodo passo per passo con i grafici di matplotlib. Dalla scheda dell'app si apre direttamente in Colab.

## Domande da fare

- Che cosa succede al raggio se raddoppi la forza? E se raddoppi la velocità iniziale?
- Perché il modulo della velocità resta costante anche se la forza non è mai nulla?
- Dove va la pallina quando tagli il filo?
