Web VPython 3.2
# =====================================================================
#  CENTRIPETAL FORCE — complete simulation (teacher version)
#  Physics, Year 3 — Liceo Scientifico «L. da Vinci», Trento — November 2026
# ---------------------------------------------------------------------
#  How to use it
#   - In the browser: https://glowscript.org → Sign in → «Create New Program»,
#     paste the whole file (the first line must stay «Web VPython 3.2»).
#   - In Python on your computer (pip install vpython): replace the first line
#     with  «from vpython import *».
#   - VPython does NOT work in Google Colab: use the notebook
#     centripetal_force_colab_en.ipynb (same method, graphs with matplotlib).
# ---------------------------------------------------------------------
#  What it does
#   A ball of mass m starts with speed v0. A force of constant magnitude F acts
#   on it, recomputed at every step PERPENDICULAR to the velocity (to the
#   left). Step-by-step method (the same as for viscous drag):
#        a = F/m          v = v + a*dt          x = x + v*dt
#   Expected results: circular path, constant |v|,
#   radius r = m*v0^2/F, period T = 2*pi*r/v0.
#   The «Cut the string» button removes the force: the ball leaves along
#   the tangent (law of inertia).
# =====================================================================

# ---------------- PARAMETERS (change them here) ----------------
m  = 0.50     # mass of the ball (kg)
F  = 2.0      # magnitude of the force (N)
v0 = 2.0      # initial speed (m/s)
dt = 0.001    # time step (s): also try 0.01 and 0.1 → spiral!
laps = 3      # how many laps to simulate

# values predicted by theory (only used to frame the scene and for the comparison)
r_th = m*v0**2/F
T_th = 2*pi*r_th/v0

# ---------------- SCENE ----------------
scene.title = "<b>Centripetal force</b> — a force always perpendicular to the velocity\n"
scene.width = 640
scene.height = 480
scene.background = vec(0.13, 0.13, 0.15)
scene.range = 1.4*r_th
scene.center = vec(0, r_th, 0)

ball = sphere(pos=vec(0, 0, 0), radius=0.05*r_th, color=color.orange,
              make_trail=True, trail_radius=0.008*r_th, trail_color=color.yellow)
ball.v = vec(v0, 0, 0)

scale_v = 0.35*r_th/v0          # arrow lengths in proportion
scale_F = 0.35*r_th/F
arrow_v = arrow(pos=ball.pos, axis=scale_v*ball.v, color=vec(0.5, 0.8, 1), shaftwidth=0.02*r_th)
arrow_F = arrow(pos=ball.pos, axis=vec(0, 0, 0), color=vec(1, 0.45, 0.4), shaftwidth=0.02*r_th)
label(pos=vec(-1.25*r_th, 2.25*r_th, 0), text="light blue: velocity   red: force", height=12, box=False, color=color.white)

# graph of the speed: it must stay constant
plot = graph(title="Speed (magnitude of the velocity)", xtitle="t (s)", ytitle="|v| (m/s)",
             width=640, height=200, ymin=0)
curve_v = gcurve(color=color.blue)

# ---------------- «CUT THE STRING» BUTTON ----------------
string_cut = False
def cut_string(b):
    global string_cut
    string_cut = True
    b.disabled = True
button(text="Cut the string", bind=cut_string)
scene.append_to_caption("\n")

# ---------------- STEP-BY-STEP LOOP ----------------
t = 0
y_max = 0          # farthest point from the start → diameter
T_meas = 0         # measured period (0 = not measured yet)
x_before = 0

while t < laps*T_th:
    rate(1/dt)                                 # steps per second (real-time animation)

    if string_cut:
        a = vec(0, 0, 0)                       # no force: uniform straight-line motion
    else:
        perp = hat(vec(-ball.v.y, ball.v.x, 0))   # unit vector perpendicular to v (to the left)
        a = (F/m)*perp                         # Newton's second law: a = F/m

    ball.v = ball.v + a*dt                     # new velocity
    ball.pos = ball.pos + ball.v*dt            # new position
    t = t + dt

    # arrows and graph
    arrow_v.pos = ball.pos
    arrow_v.axis = scale_v*ball.v
    arrow_F.pos = ball.pos
    arrow_F.axis = scale_F*m*a
    curve_v.plot(t, mag(ball.v))

    # measurements on the first lap: diameter and period
    if T_meas == 0:
        y_max = max(y_max, ball.pos.y)
        if x_before < 0 and ball.pos.x >= 0 and t > 0.1:
            T_meas = t                         # the ball is back at the starting point
        x_before = ball.pos.x

# ---------------- RESULTS ----------------
r_meas = y_max/2
print("Results on the first lap")
print("  measured radius  r =", round(r_meas, 3), "m     theory m*v0^2/F =", round(r_th, 3), "m")
if T_meas > 0:
    print("  measured period  T =", round(T_meas, 3), "s     theory 2*pi*r/v0 =", round(T_th, 3), "s")
print("  |v| at the end     =", round(mag(ball.v), 3), "m/s   (at the start", v0, "m/s)")
print("  F*r/(m*v0^2)       =", round(F*r_meas/(m*v0**2), 3), "  ← should be about 1")
