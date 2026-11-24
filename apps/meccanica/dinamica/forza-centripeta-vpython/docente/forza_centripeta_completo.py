Web VPython 3.2
# =====================================================================
#  LA FORZA CENTRIPETA — simulazione completa (versione del docente)
#  Fisica 3R — Liceo Scientifico «L. da Vinci», Trento — novembre 2026
# ---------------------------------------------------------------------
#  Come si usa
#   - Nel browser: https://glowscript.org → Sign in → «Create New Program»,
#     incolla tutto il file (la prima riga deve restare «Web VPython 3.2»).
#   - In Python sul computer (pip install vpython): sostituisci la prima riga
#     con  «from vpython import *».
#   - In Google Colab VPython NON funziona: usa il notebook
#     forza_centripeta_colab.ipynb (stesso metodo, grafici con matplotlib).
# ---------------------------------------------------------------------
#  Che cosa fa
#   Una pallina di massa m parte con velocità v0. Su di lei agisce una forza
#   di modulo costante F, ricalcolata a ogni passo PERPENDICOLARE alla
#   velocità (verso sinistra). Metodo passo per passo (lo stesso
#   dell'attrito viscoso):
#        a = F/m          v = v + a*dt          x = x + v*dt
#   Risultati attesi: traiettoria circolare, |v| costante,
#   raggio r = m*v0^2/F, periodo T = 2*pi*r/v0.
#   Il pulsante «Taglia il filo» toglie la forza: la pallina parte lungo
#   la tangente (principio d'inerzia).
# =====================================================================

# ---------------- PARAMETRI (si cambiano qui) ----------------
m  = 0.50     # massa della pallina (kg)
F  = 2.0      # modulo della forza (N)
v0 = 2.0      # velocità iniziale (m/s)
dt = 0.001    # passo temporale (s): prova anche 0.01 e 0.1 → spirale!
giri = 3      # quanti giri simulare

# valori previsti dalla teoria (servono solo per inquadrare la scena e per il confronto)
r_teo = m*v0**2/F
T_teo = 2*pi*r_teo/v0

# ---------------- SCENA ----------------
scene.title = "<b>La forza centripeta</b> — forza sempre perpendicolare alla velocità\n"
scene.width = 640
scene.height = 480
scene.background = vec(0.13, 0.13, 0.15)
scene.range = 1.4*r_teo
scene.center = vec(0, r_teo, 0)

pallina = sphere(pos=vec(0, 0, 0), radius=0.05*r_teo, color=color.orange,
                 make_trail=True, trail_radius=0.008*r_teo, trail_color=color.yellow)
pallina.v = vec(v0, 0, 0)

scala_v = 0.35*r_teo/v0          # lunghezza delle frecce in proporzione
scala_F = 0.35*r_teo/F
freccia_v = arrow(pos=pallina.pos, axis=scala_v*pallina.v, color=vec(0.5, 0.8, 1), shaftwidth=0.02*r_teo)
freccia_F = arrow(pos=pallina.pos, axis=vec(0, 0, 0), color=vec(1, 0.45, 0.4), shaftwidth=0.02*r_teo)
label(pos=vec(-1.25*r_teo, 2.25*r_teo, 0), text="azzurro: velocità   rosso: forza", height=12, box=False, color=color.white)

# grafico del modulo della velocità: deve restare costante
grafico = graph(title="Modulo della velocità", xtitle="t (s)", ytitle="|v| (m/s)",
                width=640, height=200, ymin=0)
curva_v = gcurve(color=color.blue)

# ---------------- PULSANTE «TAGLIA IL FILO» ----------------
filo_tagliato = False
def taglia_filo(b):
    global filo_tagliato
    filo_tagliato = True
    b.disabled = True
button(text="Taglia il filo", bind=taglia_filo)
scene.append_to_caption("\n")

# ---------------- CICLO PASSO PER PASSO ----------------
t = 0
y_max = 0          # punto più lontano dalla partenza → diametro
T_mis = 0          # periodo misurato (0 = non ancora misurato)
x_prima = 0

while t < giri*T_teo:
    rate(1/dt)                                 # passi al secondo (animazione in tempo reale)

    if filo_tagliato:
        a = vec(0, 0, 0)                       # niente forza: moto rettilineo uniforme
    else:
        perp = hat(vec(-pallina.v.y, pallina.v.x, 0))   # versore perpendicolare a v (verso sinistra)
        a = (F/m)*perp                         # seconda legge di Newton: a = F/m

    pallina.v = pallina.v + a*dt               # nuova velocità
    pallina.pos = pallina.pos + pallina.v*dt   # nuova posizione
    t = t + dt

    # frecce e grafico
    freccia_v.pos = pallina.pos
    freccia_v.axis = scala_v*pallina.v
    freccia_F.pos = pallina.pos
    freccia_F.axis = scala_F*m*a
    curva_v.plot(t, mag(pallina.v))

    # misure sul primo giro: diametro e periodo
    if T_mis == 0:
        y_max = max(y_max, pallina.pos.y)
        if x_prima < 0 and pallina.pos.x >= 0 and t > 0.1:
            T_mis = t                          # la pallina è tornata al punto di partenza
        x_prima = pallina.pos.x

# ---------------- RISULTATI ----------------
r_mis = y_max/2
print("Risultati sul primo giro")
print("  raggio misurato  r =", round(r_mis, 3), "m     teoria m*v0^2/F =", round(r_teo, 3), "m")
if T_mis > 0:
    print("  periodo misurato T =", round(T_mis, 3), "s     teoria 2*pi*r/v0 =", round(T_teo, 3), "s")
print("  |v| alla fine      =", round(mag(pallina.v), 3), "m/s   (all'inizio", v0, "m/s)")
print("  F*r/(m*v0^2)       =", round(F*r_mis/(m*v0**2), 3), "  ← deve venire circa 1")
