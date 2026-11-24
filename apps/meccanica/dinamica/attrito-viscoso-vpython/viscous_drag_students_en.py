Web VPython 3.2
# ============================================================
#  Viscous drag: a small steel ball falling through glycerine
#  Year 3 - to be completed step by step
#  Paste it into https://glowscript.org and press "Run".
#  The program already runs as it is (step 1). Then complete the TODOs
#  one step at a time and run it again each time.
# ============================================================

# ---------------- data (SI) ----------------
g = 9.81          # m/s^2
r = 2.0e-3        # radius of the ball (m)
rho_s = 7800      # density of steel (kg/m^3)
rho_f = 1260      # density of glycerine (kg/m^3)
eta = 1.4         # viscosity of glycerine (Pa*s)

V = 4/3*pi*r**3   # volume of the ball
m = rho_s*V       # mass of the ball

# ---------------- scene ----------------
H = 0.20          # height of the glycerine (m)
scene = canvas(title="Small ball in glycerine", width=500, height=500,
               center=vec(0, -H/2, 0), background=color.white)
cylinder(pos=vec(0, -H, 0), axis=vec(0, H, 0), radius=0.02,
         color=vec(1, 0.85, 0.5), opacity=0.25)
for y_mark in [-0.05, -0.15]:                      # stopwatch marks
    box(pos=vec(0.021, y_mark, 0), size=vec(0.006, 0.0008, 0.0008), color=color.red)
ball = sphere(pos=vec(0, -0.002, 0), radius=4*r, color=color.gray(0.4))   # drawn 4 times bigger

gv = graph(title="v (cm/s) as a function of t (ms)", xtitle="t (ms)", ytitle="v (cm/s)", width=500, height=250)
curve_v = gcurve(graph=gv, color=color.blue)

# ---------------- step-by-step method ----------------
v = vec(0, 0, 0)        # the ball starts at rest
t = 0
dt = 1e-4               # 0.1 ms
y_axis = vec(0, 1, 0)   # y axis pointing up

t_mark1 = None
t_mark2 = None

while ball.pos.y > -H + 4*r and t < 5:
    if t < 0.03:
        rate(100)       # slow motion during the first 30 ms
    else:
        rate(20000)

    # STEP 1 - weight only (runs as it is)
    W = -m*g*y_axis
    B = vec(0, 0, 0)
    Fv = vec(0, 0, 0)

    # TODO STEP 2 - buoyancy (Archimedes): |B| = rho_f*V*g, pointing up
    # B = ...

    # TODO STEP 3 - viscous drag (Stokes' law): b = 6*pi*eta*r, Fv = -b*v
    # b = ...
    # Fv = ...

    a = (W + B + Fv)/m              # Newton's second law
    v = v + a*dt                    # new velocity
    ball.pos = ball.pos + v*dt      # new position
    t = t + dt

    if t < 0.03:
        curve_v.plot(t*1000, mag(v)*100)
    if t_mark1 is None and ball.pos.y <= -0.05:
        t_mark1 = t
    if t_mark2 is None and ball.pos.y <= -0.15:
        t_mark2 = t

print("final speed =", round(mag(v)*100, 2), "cm/s")
print("time to reach the bottom =", round(t, 3), "s")

# TODO STEP 4 - measure it as in the lab: the marks are 10 cm apart.
# Compute v_marks = 0.10/(t_mark2 - t_mark1) and print it in cm/s.
# Then compute the theoretical terminal velocity
#     vL = 2*r**2*(rho_s - rho_f)*g/(9*eta)
# and compare them.

# ------------------------------------------------------------
# QUESTIONS
# 1. In step 1, how does the ball move? What shape is the v(t) graph?
# 2. In step 2 the ball accelerates less: by how much? Compute a0 = g*(1 - rho_f/rho_s).
# 3. In step 3: after how many milliseconds does the speed stop increasing?
#    What is the net force from that moment on?
#
# EXPERIMENT TABLE (change r and run again, with all steps completed)
#     r (mm) | simulated v_L (cm/s) | theoretical v_L (cm/s) | r^2 (mm^2)
#     1.0    |                      |                        |
#     1.5    |                      |                        |
#     2.0    |                      |                        |
# What do you notice when you compare v_L with r^2?
#
# CHALLENGE
# Use water instead of glycerine (rho_f = 1000, eta = 0.001).
# What is v_L now? Compute the Reynolds number Re = rho_f*v*2*r/eta:
# is Stokes' model still valid?
# ------------------------------------------------------------
