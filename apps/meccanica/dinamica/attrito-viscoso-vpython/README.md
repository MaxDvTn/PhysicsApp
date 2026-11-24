# Sferetta nella glicerina (VPython)

Una sferetta d'acciaio (raggio 2 mm) cade in un cilindro di glicerina. Il programma calcola il moto passo per passo con il secondo principio, disegna i grafici v(t) e a(t), misura la velocità tra due tacche e la confronta con la formula di Stokes.

## Come si usa

**Nel browser, senza installare niente (consigliato).**

1. Apri [glowscript.org](https://glowscript.org), accedi con un account Google e scegli **Create New Program**.
2. Copia tutto il file `.py` e incollalo. La prima riga deve restare `Web VPython 3.2`.
3. Premi **Run**.

**Versione studenti.** Il file `attrito_viscoso_studenti.py` gira già così com'è (passo 1: solo il peso). Si completano i `TODO` un passo alla volta, rilanciando ogni volta: peso, poi spinta di Archimede, poi attrito viscoso, poi misura tra le tacche. Le domande sono nei commenti; in fondo ci sono la tabella v_L – r² e la sfida (acciaio in acqua e numero di Reynolds).

**Versione completa.** Nella parte «Per il docente», `docente/attrito_viscoso_completo.py` è la simulazione finita, da proiettare o da usare per controllare.

**In Google Colab.** VPython non funziona in Colab: il notebook `attrito_viscoso_colab.ipynb` fa lo stesso calcolo con numpy e i grafici con matplotlib. Dalla scheda dell'app si apre direttamente in Colab.

**Sul computer.** Con `pip install vpython`, sostituisci la prima riga con `from vpython import *`.

## Risultati attesi

Velocità limite 4,07 cm/s (simulata, misurata tra le tacche e teorica coincidono), tempo caratteristico τ ≈ 5 ms, numero di Reynolds 0,15.

## Note

Nel programma l'accelerazione di gravità vale 9,81 m/s².
