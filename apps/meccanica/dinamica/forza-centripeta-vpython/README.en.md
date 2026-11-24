# A force always perpendicular to the velocity (VPython)

A ball of mass m starts with speed v₀. A force of constant magnitude acts on it, recomputed at every step perpendicular to the velocity. The result is a circular path with constant |v|, radius r = m v₀²/F and period T = 2πr/v₀. The **Cut the string** button removes the force and the ball leaves along the tangent.

The scripts and the notebook are available in Italian and in English (files ending in `_en`).

## How to use it

**In the browser, with nothing to install (recommended).**

1. Open [glowscript.org](https://glowscript.org), sign in and choose **Create New Program**.
2. Paste the whole `.py` file. The first line must stay `Web VPython 3.2`.
3. Press **Run**.

**Students' version.** `centripetal_force_students_en.py` is completed one step at a time: complete the lines marked `# TODO`, run, observe and answer the questions in the comments. At the top are the parameters (mass, force, initial speed, time step) to change for the experiments.

**Complete version.** In the “For the teacher” section, `docente/centripetal_force_complete_en.py` is the finished simulation, to project.

**In Google Colab.** The notebook `centripetal_force_colab_en.ipynb` uses the same step-by-step method with matplotlib graphs. It opens directly in Colab from the app page.

## Questions to ask

- What happens to the radius if you double the force? And if you double the initial speed?
- Why does the speed stay constant even though the force is never zero?
- Where does the ball go when you cut the string?
