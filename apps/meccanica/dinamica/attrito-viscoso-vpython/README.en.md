# Small ball in glycerine (VPython)

A small steel ball (radius 2 mm) falls through a cylinder of glycerine. The program computes the motion step by step with Newton's second law, draws the v(t) and a(t) graphs, measures the speed between two marks and compares it with Stokes' formula.

The scripts and the notebook are available in Italian and in English (files ending in `_en`).

## How to use it

**In the browser, with nothing to install (recommended).**

1. Open [glowscript.org](https://glowscript.org), sign in with a Google account and choose **Create New Program**.
2. Copy the whole `.py` file and paste it. The first line must stay `Web VPython 3.2`.
3. Press **Run**.

**Students' version.** `viscous_drag_students_en.py` already runs as it is (step 1: weight only). Students complete the `TODO`s one step at a time, running the program each time: weight, then buoyancy, then viscous drag, then the measurement between the marks. The questions are in the comments; at the end there are the v_L – r² table and the challenge (steel in water and the Reynolds number).

**Complete version.** In the “For the teacher” section, `docente/viscous_drag_complete_en.py` is the finished simulation, to project or to check against.

**In Google Colab.** VPython does not work in Colab: the notebook `viscous_drag_colab_en.ipynb` does the same calculation with numpy and the graphs with matplotlib. It opens directly in Colab from the app page.

**On your computer.** With `pip install vpython`, replace the first line with `from vpython import *`.

## Expected results

Terminal velocity 4.07 cm/s (simulated, measured between the marks and theoretical all agree), characteristic time τ ≈ 5 ms, Reynolds number 0.15.

## Notes

The program uses g = 9.81 m/s².
