Web VPython 3.2
# =====================================================================
#  CENTRIPETAL FORCE — simulation to complete
#  Physics, Year 3 — Liceo Scientifico «L. da Vinci», Trento
#  Name: ______________________   Partner: __________________
# ---------------------------------------------------------------------
#  Where to run it: https://glowscript.org → «Create New Program»,
#  paste the file (the first line must stay «Web VPython 3.2») and press «Run».
#  Work one STEP at a time: complete the lines marked  # TODO , run,
#  observe and answer the questions written in the comments.
# =====================================================================

# ---------------- PARAMETERS ----------------
m  = 0.50     # mass of the ball (kg)
F  = 2.0      # magnitude of the force (N)
v0 = 2.0      # initial speed (m/s)
dt = 0.001    # time step (s)
duration = 10 # how long the simulation lasts (s)

# ---------------- SCENE (ready) ----------------
scene.title = "<b>What does a force that is always perpendicular to the velocity do?</b>\n"
scene.width = 640
scene.height = 480
scene.background = vec(0.13, 0.13, 0.15)
scene.range = 3
scene.center = vec(0, 1, 0)

ball = sphere(pos=vec(0, 0, 0), radius=0.06, color=color.orange,
              make_trail=True, trail_radius=0.01, trail_color=color.yellow)
ball.v = vec(v0, 0, 0)

arrow_v = arrow(pos=ball.pos, axis=0.3*ball.v, color=vec(0.5, 0.8, 1), shaftwidth=0.03)
arrow_F = arrow(pos=ball.pos, axis=vec(0, 0, 0), color=vec(1, 0.45, 0.4), shaftwidth=0.03)

plot = graph(title="Speed (magnitude of the velocity)", xtitle="t (s)", ytitle="|v| (m/s)",
             width=640, height=200, ymin=0)
curve_v = gcurve(color=color.blue)

string_cut = False
def cut_string(b):
    global string_cut
    string_cut = True
    b.disabled = True
button(text="Cut the string", bind=cut_string)
scene.append_to_caption("\n")

# ---------------- STEP-BY-STEP LOOP ----------------
t = 0
y_max = 0
T_meas = 0
x_before = 0

while t < duration:
    rate(1/dt)

    # ===== STEP 1 — No force (done) =====
    # Run the program as it is. How does the ball move? Why?
    a = vec(0, 0, 0)

    # ===== STEP 2 — The perpendicular force =====
    # The vector vec(-v.y, v.x, 0) is the velocity rotated by 90° to the left.
    # hat(...) makes it 1 long (unit vector).
    # TODO: remove the # from the two lines below and run again.
    # perp = hat(vec(-ball.v.y, ball.v.x, 0))
    # a = (F/m)*perp
    #
    # QUESTIONS: what path do you get? Look at the graph: does the speed
    # change? Why does the force neither speed the ball up nor slow it down?

    # ===== STEP 4 — The string is cut (do it after step 3) =====
    # TODO: if string_cut is true, the force disappears: write below
    #       an «if» that sets a = vec(0, 0, 0) in that case.
    # QUESTION: press «Cut the string» while the ball is turning. Where does it go? Why?

    # step-by-step update (done)
    ball.v = ball.v + a*dt
    ball.pos = ball.pos + ball.v*dt
    t = t + dt

    arrow_v.pos = ball.pos
    arrow_v.axis = 0.3*ball.v
    arrow_F.pos = ball.pos
    arrow_F.axis = 0.3*m*a
    curve_v.plot(t, mag(ball.v))

    # ===== STEP 3 — Measure radius and period on the first lap =====
    # The ball starts at (0, 0) moving to the right and turns to the left:
    # the highest point of the circle has y = diameter.
    if T_meas == 0:
        y_max = max(y_max, ball.pos.y)
        # TODO: the ball has completed a lap when x goes from negative to positive.
        #       Remove the # from the two lines below.
        # if x_before < 0 and ball.pos.x >= 0 and t > 0.1:
        #     T_meas = t
        x_before = ball.pos.x

# ---------------- RESULTS ----------------
r_meas = y_max/2
print("radius r =", round(r_meas, 3), "m      period T =", round(T_meas, 3), "s")
# TODO: also print the number  F*r_meas/(m*v0**2) . What is its value?

# =====================================================================
#  EXPERIMENT (in pairs) — what does the radius depend on?
#  Change ONE parameter at a time at the top, run and fill in the table.
#
#   m (kg) | F (N) | v0 (m/s) | r (m) | T (s) | F*r/(m*v0^2)
#   0.50   | 2.0   | 1.0      |       |       |
#   0.50   | 2.0   | 2.0      |       |       |
#   0.50   | 2.0   | 3.0      |       |       |
#   0.50   | 2.0   | 4.0      |       |       |
#   0.50   | 4.0   | 2.0      |       |       |
#   1.00   | 2.0   | 2.0      |       |       |
#
#  QUESTIONS: if v0 doubles, how does r change? And if F doubles? And if m doubles?
#  Write a formula linking F, m, v0 and r.
#  CHALLENGE: set dt = 0.1. What happens to the path and to |v|? Is it physics
#  or an error of the method? How do you fix it?
# =====================================================================
