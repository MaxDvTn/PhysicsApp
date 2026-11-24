# The impossible shot

A wildlife photographer-vet aims a dart gun straight at a monkey hanging from a branch. The monkey lets go at the instant of the shot. Does the dart still hit it? It is the classic monkey and hunter problem, turned into an investigation in three acts and a VPython simulation that students build themselves.

The worksheets are in Italian.

## How to use it

1. **Investigation worksheet** (90 minutes, alone or in pairs). In Act 1 each student chooses and justifies their own data: height of the monkey h, distance d, speed of the dart v₀. In Act 2 they make a prediction and justify it with the equations of motion.
2. **Step 1: the dart moving horizontally** (45 minutes). Only the horizontal motion of the dart is simulated, uniform with vₓ = v₀ cos θ, and the simulated time is compared with d/vₓ.
3. **Step 1B: the falling monkey**. The free fall of the monkey is simulated.
4. **Step 2: dart and monkey together** (60 minutes). The two programs are joined: the simulation decides on its own whether the dart hits or misses. The “ghost dart”, which moves without gravity along the line of sight, shows why it works.

The code is written on [glowscript.org](https://glowscript.org) (first line `Web VPython 3.2`) or in Python with `from vpython import *`. Each worksheet has blanks to fill in (`___`), questions to answer in the comments and some challenges: a dart that is too slow, gravity on the Moon and on Jupiter, a large time step, a monkey that jumps downwards.

## Expected result

With the example data (h = 8 m, d = 30 m, v₀ = 60 m/s) the simulation ends at t ≈ 0.52 s with the verdict **HIT**: dart and monkey fall by the same amount compared with where they would be without gravity.

## Notes

The worksheets use g = 9.81 m/s². The teacher's solution (proof, example data and complete simulation) is in the “For the teacher” section.
