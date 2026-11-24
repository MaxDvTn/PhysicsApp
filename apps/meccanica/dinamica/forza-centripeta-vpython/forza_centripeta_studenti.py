Web VPython 3.2
# =====================================================================
#  LA FORZA CENTRIPETA — simulazione da completare
#  Fisica 3R — Liceo Scientifico «L. da Vinci», Trento
#  Nome e cognome: ______________________   Compagno/a: __________________
# ---------------------------------------------------------------------
#  Dove si lancia: https://glowscript.org → «Create New Program»,
#  incolla il file (la prima riga deve restare «Web VPython 3.2») e premi «Run».
#  Lavora un PASSO alla volta: completa le righe con  # TODO , lancia,
#  osserva e rispondi alle domande scritte nei commenti.
# =====================================================================

# ---------------- PARAMETRI ----------------
m  = 0.50     # massa della pallina (kg)
F  = 2.0      # modulo della forza (N)
v0 = 2.0      # velocità iniziale (m/s)
dt = 0.001    # passo temporale (s)
durata = 10   # quanto dura la simulazione (s)

# ---------------- SCENA (già pronta) ----------------
scene.title = "<b>Che cosa fa una forza sempre perpendicolare alla velocità?</b>\n"
scene.width = 640
scene.height = 480
scene.background = vec(0.13, 0.13, 0.15)
scene.range = 3
scene.center = vec(0, 1, 0)

pallina = sphere(pos=vec(0, 0, 0), radius=0.06, color=color.orange,
                 make_trail=True, trail_radius=0.01, trail_color=color.yellow)
pallina.v = vec(v0, 0, 0)

freccia_v = arrow(pos=pallina.pos, axis=0.3*pallina.v, color=vec(0.5, 0.8, 1), shaftwidth=0.03)
freccia_F = arrow(pos=pallina.pos, axis=vec(0, 0, 0), color=vec(1, 0.45, 0.4), shaftwidth=0.03)

grafico = graph(title="Modulo della velocità", xtitle="t (s)", ytitle="|v| (m/s)",
                width=640, height=200, ymin=0)
curva_v = gcurve(color=color.blue)

filo_tagliato = False
def taglia_filo(b):
    global filo_tagliato
    filo_tagliato = True
    b.disabled = True
button(text="Taglia il filo", bind=taglia_filo)
scene.append_to_caption("\n")

# ---------------- CICLO PASSO PER PASSO ----------------
t = 0
y_max = 0
T_mis = 0
x_prima = 0

while t < durata:
    rate(1/dt)

    # ===== PASSO 1 — Senza forza (già fatto) =====
    # Lancia il programma così com'è. Che moto fa la pallina? Perché?
    a = vec(0, 0, 0)

    # ===== PASSO 2 — La forza perpendicolare =====
    # Il vettore vec(-v.y, v.x, 0) è la velocità ruotata di 90° verso sinistra.
    # hat(...) lo rende lungo 1 (versore).
    # TODO: togli il # alle due righe qui sotto e lancia di nuovo.
    # perp = hat(vec(-pallina.v.y, pallina.v.x, 0))
    # a = (F/m)*perp
    #
    # DOMANDE: che traiettoria ottieni? Guarda il grafico: il modulo della
    # velocità cambia? Perché la forza non accelera né frena la pallina?

    # ===== PASSO 4 — Il filo si taglia (fallo dopo il passo 3) =====
    # TODO: se filo_tagliato è vero, la forza sparisce: scrivi qui sotto
    #       un «if» che in quel caso mette a = vec(0, 0, 0).
    # DOMANDA: premi «Taglia il filo» mentre la pallina gira. Dove va? Perché?

    # aggiornamento passo per passo (già fatto)
    pallina.v = pallina.v + a*dt
    pallina.pos = pallina.pos + pallina.v*dt
    t = t + dt

    freccia_v.pos = pallina.pos
    freccia_v.axis = 0.3*pallina.v
    freccia_F.pos = pallina.pos
    freccia_F.axis = 0.3*m*a
    curva_v.plot(t, mag(pallina.v))

    # ===== PASSO 3 — Misuriamo raggio e periodo sul primo giro =====
    # La pallina parte da (0, 0) andando verso destra e gira verso sinistra:
    # il punto più alto della circonferenza ha y = diametro.
    if T_mis == 0:
        y_max = max(y_max, pallina.pos.y)
        # TODO: la pallina ha finito un giro quando x passa da negativo a positivo.
        #       Togli il # alle due righe qui sotto.
        # if x_prima < 0 and pallina.pos.x >= 0 and t > 0.1:
        #     T_mis = t
        x_prima = pallina.pos.x

# ---------------- RISULTATI ----------------
r_mis = y_max/2
print("raggio r =", round(r_mis, 3), "m      periodo T =", round(T_mis, 3), "s")
# TODO: stampa anche il numero  F*r_mis/(m*v0**2) . Quanto vale?

# =====================================================================
#  ESPERIMENTO (a coppie) — da che cosa dipende il raggio?
#  Cambia UN parametro alla volta in alto, lancia e compila la tabella.
#
#   m (kg) | F (N) | v0 (m/s) | r (m) | T (s) | F*r/(m*v0^2)
#   0,50   | 2,0   | 1,0      |       |       |
#   0,50   | 2,0   | 2,0      |       |       |
#   0,50   | 2,0   | 3,0      |       |       |
#   0,50   | 2,0   | 4,0      |       |       |
#   0,50   | 4,0   | 2,0      |       |       |
#   1,00   | 2,0   | 2,0      |       |       |
#
#  DOMANDE: se v0 raddoppia, come cambia r? E se raddoppia F? E se raddoppia m?
#  Scrivi una formula che leghi F, m, v0 e r.
#  SFIDA: metti dt = 0.1. Che cosa succede alla traiettoria e a |v|? È fisica
#  o è un errore del metodo? Come lo correggi?
# =====================================================================
