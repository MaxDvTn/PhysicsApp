# Il tiro impossibile

Un fotografo-veterinario mira con un fucile a dardi dritto a una scimmia appesa a un ramo. La scimmia si lascia cadere nell'istante dello sparo. La colpisce lo stesso? È il classico problema del cacciatore e della scimmia, trasformato in un'indagine in tre atti e in una simulazione VPython che gli studenti costruiscono da soli.

## Come si usa

1. **Scheda dell'indagine** (90 minuti, da soli o in coppia). Nell'Atto 1 ogni studente sceglie e motiva i propri dati: quota della scimmia h, distanza d, velocità del dardo v₀. Nell'Atto 2 fa una previsione e la giustifica con le leggi orarie.
2. **Passo 1: il dardo in orizzontale** (45 minuti). Si simula solo il moto orizzontale del dardo, rettilineo uniforme con vₓ = v₀ cos θ, e si confronta il tempo simulato con d/vₓ.
3. **Passo 1B: la scimmia che cade**. Si simula la caduta libera della scimmia.
4. **Passo 2: dardo e scimmia insieme** (60 minuti). Si uniscono i due programmi: la simulazione decide da sola se il dardo colpisce o manca. Il «dardo fantasma», che si muove senza gravità lungo la linea di mira, fa capire perché funziona.

Il codice si scrive su [glowscript.org](https://glowscript.org) (prima riga `Web VPython 3.2`) oppure in Python con `from vpython import *`. Ogni scheda ha le parti da completare (`___`), le domande da rispondere nei commenti e alcune sfide: dardo troppo lento, gravità della Luna e di Giove, passo temporale grande, scimmia che si lancia verso il basso.

## Risultato atteso

Con i dati di esempio (h = 8 m, d = 30 m, v₀ = 60 m/s) la simulazione finisce a t ≈ 0,52 s con il verdetto **COLPITA**: dardo e scimmia cadono della stessa quantità rispetto a dove sarebbero senza gravità.

## Note

Le schede usano g = 9,81 m/s². La soluzione per il docente non è pubblicata qui.
