Web VPython 3.2
# ============================================================
#  Attrito viscoso: una sferetta d'acciaio cade nella glicerina
#  Classe 3R - da completare a passi
#  Si incolla su https://glowscript.org e si preme "Run".
#  Il programma gira gia' cosi' com'e' (passo 1). Poi completa i TODO
#  un passo alla volta e rilancialo ogni volta.
# ============================================================

# ---------------- dati (SI) ----------------
g = 9.81          # m/s^2
r = 2.0e-3        # raggio della sferetta (m)
rho_s = 7800      # densita' dell'acciaio (kg/m^3)
rho_f = 1260      # densita' della glicerina (kg/m^3)
eta = 1.4         # viscosita' della glicerina (Pa*s)

V = 4/3*pi*r**3   # volume della sferetta
m = rho_s*V       # massa della sferetta

# ---------------- scena ----------------
H = 0.20          # altezza della glicerina (m)
scene = canvas(title="Sferetta nella glicerina", width=500, height=500,
               center=vec(0, -H/2, 0), background=color.white)
cylinder(pos=vec(0, -H, 0), axis=vec(0, H, 0), radius=0.02,
         color=vec(1, 0.85, 0.5), opacity=0.25)
for y_tacca in [-0.05, -0.15]:                     # tacche del cronometro
    box(pos=vec(0.021, y_tacca, 0), size=vec(0.006, 0.0008, 0.0008), color=color.red)
pallina = sphere(pos=vec(0, -0.002, 0), radius=4*r, color=color.gray(0.4))   # disegnata 4 volte piu' grande

gv = graph(title="v (cm/s) in funzione di t (ms)", xtitle="t (ms)", ytitle="v (cm/s)", width=500, height=250)
curva_v = gcurve(graph=gv, color=color.blue)

# ---------------- metodo passo per passo ----------------
v = vec(0, 0, 0)        # la sferetta parte da ferma
t = 0
dt = 1e-4               # 0,1 ms
asse_y = vec(0, 1, 0)   # asse y verso l'alto

t_tacca1 = None
t_tacca2 = None

while pallina.pos.y > -H + 4*r and t < 5:
    if t < 0.03:
        rate(100)       # al rallentatore nei primi 30 ms
    else:
        rate(20000)

    # PASSO 1 - solo il peso (gira cosi' com'e')
    P = -m*g*asse_y
    S = vec(0, 0, 0)
    Fv = vec(0, 0, 0)

    # TODO PASSO 2 - la spinta di Archimede: |S| = rho_f*V*g, verso l'alto
    # S = ...

    # TODO PASSO 3 - l'attrito viscoso (legge di Stokes): b = 6*pi*eta*r, Fv = -b*v
    # b = ...
    # Fv = ...

    a = (P + S + Fv)/m              # secondo principio della dinamica
    v = v + a*dt                    # nuova velocita'
    pallina.pos = pallina.pos + v*dt   # nuova posizione
    t = t + dt

    if t < 0.03:
        curva_v.plot(t*1000, mag(v)*100)
    if t_tacca1 is None and pallina.pos.y <= -0.05:
        t_tacca1 = t
    if t_tacca2 is None and pallina.pos.y <= -0.15:
        t_tacca2 = t

print("velocita' finale =", round(mag(v)*100, 2), "cm/s")
print("tempo di discesa =", round(t, 3), "s")

# TODO PASSO 4 - misura come in laboratorio: le tacche distano 10 cm.
# Calcola v_tacche = 0.10/(t_tacca2 - t_tacca1) e stampala in cm/s.
# Poi calcola la velocita' limite teorica
#     vL = 2*r**2*(rho_s - rho_f)*g/(9*eta)
# e confrontale.

# ------------------------------------------------------------
# DOMANDE
# 1. Al passo 1 la sferetta che moto fa? Che forma ha il grafico v(t)?
# 2. Al passo 2 la sferetta accelera di meno: di quanto? Calcola a0 = g*(1 - rho_f/rho_s).
# 3. Al passo 3: dopo quanti millisecondi la velocita' smette di crescere?
#    Quanto vale la forza risultante da quel momento in poi?
#
# TABELLA DELL'ESPERIMENTO (cambia r e rilancia, con tutti i passi completati)
#     r (mm) | v_L simulata (cm/s) | v_L teorica (cm/s) | r^2 (mm^2)
#     1,0    |                     |                    |
#     1,5    |                     |                    |
#     2,0    |                     |                    |
# Che cosa noti se confronti v_L con r^2?
#
# SFIDA
# Metti l'acqua al posto della glicerina (rho_f = 1000, eta = 0.001).
# Quanto viene v_L? Calcola il numero di Reynolds Re = rho_f*v*2*r/eta:
# il modello di Stokes e' ancora valido?
# ------------------------------------------------------------
