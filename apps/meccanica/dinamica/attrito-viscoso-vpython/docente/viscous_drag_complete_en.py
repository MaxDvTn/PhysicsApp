Web VPython 3.2
# ============================================================
#  Viscous drag: a small steel ball falling through glycerine
#  Complete version (teacher) - Year 3
#  Paste it into https://glowscript.org (nothing to install).
#  In Python on your computer: replace the first line with
#      from vpython import *
# ============================================================

# ---------------- data (SI) ----------------
g = 9.81          # m/s^2
r = 2.0e-3        # radius of the ball (m)
rho_s = 7800      # density of steel (kg/m^3)
rho_f = 1260      # density of glycerine (kg/m^3)
eta = 1.4         # viscosity of glycerine (Pa*s)

V = 4/3*pi*r**3            # volume
m = rho_s*V                # mass
b = 6*pi*eta*r             # Stokes coefficient (kg/s)

# theoretical values, for the final comparison
a0_th = g*(1 - rho_f/rho_s)
vL_th = (m - rho_f*V)*g/b
tau_th = m/b
Re_th = rho_f*vL_th*2*r/eta

# ---------------- scene ----------------
H = 0.20                                   # height of the glycerine (m)
scene = canvas(title="Small ball in glycerine", width=500, height=500,
               center=vec(0, -H/2, 0), background=color.white)
cylinder(pos=vec(0, -H, 0), axis=vec(0, H, 0), radius=0.02,
         color=vec(1, 0.85, 0.5), opacity=0.25)
for y_mark in [-0.05, -0.15]:                      # stopwatch marks
    box(pos=vec(0.021, y_mark, 0), size=vec(0.006, 0.0008, 0.0008), color=color.red)
ball = sphere(pos=vec(0, -0.002, 0), radius=4*r, color=color.gray(0.4))   # drawn 4 times bigger

gv = graph(title="v (cm/s) as a function of t (ms)", xtitle="t (ms)", ytitle="v (cm/s)", width=500, height=250)
curve_v = gcurve(graph=gv, color=color.blue, label="simulation")
curve_th = gcurve(graph=gv, color=color.red, label="theory v_L(1 - e^(-t/tau))")
ga = graph(title="a (m/s^2) as a function of t (ms)", xtitle="t (ms)", ytitle="a (m/s^2)", width=500, height=250)
curve_a = gcurve(graph=ga, color=color.green)

# ---------------- step-by-step method ----------------
v = vec(0, 0, 0)        # starts at rest
t = 0
dt = 1e-4               # 0.1 ms: much smaller than tau (about 5 ms)
y_axis = vec(0, 1, 0)

t63 = None              # instant when v reaches 63% of v_L
t_mark1 = None
t_mark2 = None

while ball.pos.y > -H + 4*r:
    if t < 0.03:
        rate(100)       # slow motion during the first 30 ms (you can see the acceleration phase)
    else:
        rate(20000)
    # forces (y axis pointing up: the weight has a negative component)
    W = -m*g*y_axis                 # weight
    B = rho_f*V*g*y_axis            # buoyancy (Archimedes)
    Fv = -b*v                       # viscous drag: opposite to the velocity
    a = (W + B + Fv)/m              # Newton's second law
    v = v + a*dt
    ball.pos = ball.pos + v*dt
    t = t + dt

    if t < 0.03:
        curve_v.plot(t*1000, mag(v)*100)
        curve_th.plot(t*1000, vL_th*(1 - exp(-t/tau_th))*100)
        curve_a.plot(t*1000, mag(a))
    if t63 is None and mag(v) >= 0.632*vL_th:
        t63 = t
    if t_mark1 is None and ball.pos.y <= -0.05:
        t_mark1 = t
    if t_mark2 is None and ball.pos.y <= -0.15:
        t_mark2 = t

# ---------------- measurements and comparison with theory ----------------
v_measured = 0.10/(t_mark2 - t_mark1)       # as in the lab: 10 cm between the marks
print("theoretical a0 =", round(a0_th, 2), "m/s^2")
print("theoretical v_L =", round(vL_th*100, 2), "cm/s")
print("simulated final v =", round(mag(v)*100, 2), "cm/s")
print("v between the marks (10 cm / time) =", round(v_measured*100, 2), "cm/s")
print("theoretical tau =", round(tau_th*1000, 2), "ms;  simulated t at 63% =", round(t63*1000, 2), "ms")
print("Reynolds number =", round(Re_th, 2), "(less than 1: Stokes' law holds)")
print("total time to reach the bottom =", round(t, 2), "s")
