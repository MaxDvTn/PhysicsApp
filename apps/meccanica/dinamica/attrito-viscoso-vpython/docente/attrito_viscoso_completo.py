Web VPython 3.2
# ============================================================
#  Attrito viscoso: sferetta d'acciaio che cade nella glicerina
#  Versione completa (docente) - classe 3R
#  Si incolla su https://glowscript.org (nessuna installazione).
#  In Python sul computer: sostituire la prima riga con
#      from vpython import *
# ============================================================

# ---------------- dati (SI) ----------------
g = 9.81          # m/s^2
r = 2.0e-3        # raggio della sferetta (m)
rho_s = 7800      # densita' dell'acciaio (kg/m^3)
rho_f = 1260      # densita' della glicerina (kg/m^3)
eta = 1.4         # viscosita' della glicerina (Pa*s)

V = 4/3*pi*r**3            # volume
m = rho_s*V                # massa
b = 6*pi*eta*r             # coefficiente di Stokes (kg/s)

# grandezze teoriche, per il confronto finale
a0_teo = g*(1 - rho_f/rho_s)
vL_teo = (m - rho_f*V)*g/b
tau_teo = m/b
Re_teo = rho_f*vL_teo*2*r/eta

# ---------------- scena ----------------
H = 0.20                                   # altezza della glicerina (m)
scene = canvas(title="Sferetta nella glicerina", width=500, height=500,
               center=vec(0, -H/2, 0), background=color.white)
cylinder(pos=vec(0, -H, 0), axis=vec(0, H, 0), radius=0.02,
         color=vec(1, 0.85, 0.5), opacity=0.25)
for y_tacca in [-0.05, -0.15]:                     # tacche del cronometro
    box(pos=vec(0.021, y_tacca, 0), size=vec(0.006, 0.0008, 0.0008), color=color.red)
pallina = sphere(pos=vec(0, -0.002, 0), radius=4*r, color=color.gray(0.4))   # disegnata 4 volte piu' grande

gv = graph(title="v (cm/s) in funzione di t (ms)", xtitle="t (ms)", ytitle="v (cm/s)", width=500, height=250)
curva_v = gcurve(graph=gv, color=color.blue, label="simulazione")
curva_teo = gcurve(graph=gv, color=color.red, label="teoria v_L(1 - e^(-t/tau))")
ga = graph(title="a (m/s^2) in funzione di t (ms)", xtitle="t (ms)", ytitle="a (m/s^2)", width=500, height=250)
curva_a = gcurve(graph=ga, color=color.green)

# ---------------- metodo passo per passo ----------------
v = vec(0, 0, 0)        # parte da ferma
t = 0
dt = 1e-4               # 0,1 ms: molto piu' piccolo di tau (circa 5 ms)
asse_y = vec(0, 1, 0)

t63 = None              # istante in cui v arriva al 63% di v_L
t_tacca1 = None
t_tacca2 = None

while pallina.pos.y > -H + 4*r:
    if t < 0.03:
        rate(100)       # al rallentatore nei primi 30 ms (si vede la fase di accelerazione)
    else:
        rate(20000)
    # forze (asse y verso l'alto: il peso ha componente negativa)
    P = -m*g*asse_y                 # peso
    S = rho_f*V*g*asse_y            # spinta di Archimede
    Fv = -b*v                       # attrito viscoso: opposto alla velocita'
    a = (P + S + Fv)/m              # secondo principio
    v = v + a*dt
    pallina.pos = pallina.pos + v*dt
    t = t + dt

    if t < 0.03:
        curva_v.plot(t*1000, mag(v)*100)
        curva_teo.plot(t*1000, vL_teo*(1 - exp(-t/tau_teo))*100)
        curva_a.plot(t*1000, mag(a))
    if t63 is None and mag(v) >= 0.632*vL_teo:
        t63 = t
    if t_tacca1 is None and pallina.pos.y <= -0.05:
        t_tacca1 = t
    if t_tacca2 is None and pallina.pos.y <= -0.15:
        t_tacca2 = t

# ---------------- misure e confronto con la teoria ----------------
v_misurata = 0.10/(t_tacca2 - t_tacca1)       # come in laboratorio: 10 cm tra le tacche
print("a0 teorica =", round(a0_teo, 2), "m/s^2")
print("v_L teorica =", round(vL_teo*100, 2), "cm/s")
print("v finale simulata =", round(mag(v)*100, 2), "cm/s")
print("v tra le tacche (10 cm / tempo) =", round(v_misurata*100, 2), "cm/s")
print("tau teorico =", round(tau_teo*1000, 2), "ms;  t al 63% simulato =", round(t63*1000, 2), "ms")
print("numero di Reynolds =", round(Re_teo, 2), "(minore di 1: Stokes vale)")
print("tempo totale di discesa =", round(t, 2), "s")
