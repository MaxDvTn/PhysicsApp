# Clausius-Clapeyron explorer

A two-part simulation that goes with the lesson “The equation of the mountains and of the climate” (December 2025). In the first part you climb and watch the boiling point of water drop; in the second you warm the atmosphere and watch the vapour it can hold grow.

## How to use it

1. **Water boils sooner at altitude.** Move the altitude slider (from 0 to 8849 m) or use the Trento, Hut at 2500 m, Marmolada, Mont Blanc and Everest buttons. The app computes the pressure with the standard atmosphere and the boiling point with the Clausius-Clapeyron equation, and marks the point on the graph. Ask for a prediction first: at what temperature does water boil in a mountain hut? (At 2500 m about 91.5 °C; on Mont Blanc about 83.6 °C.)
2. **Warmer means more vapour.** Choose the starting temperature and the warming. The graph compares the real saturation vapour pressure (Buck formula) with two models: Clausius-Clapeyron with a constant latent heat and with a latent heat that changes with temperature. The percentage increases are shown below.
3. Open “Where the ‘7 % per degree’ comes from”: with constant L you get about 6 % at 15 °C; taking into account that L is larger at low temperature gives 7.5 % near 0 °C and 6–6.6 % between 15 and 25 °C, as the real data show.

It works in the browser, on phones too, and without a connection (except for the typeface).

## Good to know

- This is the December 2025 simulation, revised on 24 November 2026: before, the 7 % was used as a given (1.07 to the power of the warming); now it is computed from the equation, and “vapour capacity” has become “saturation vapour pressure”.
- The constant-L model also gets the value wrong: at 15 °C it gives 2.1 kPa against a real 1.7 kPa. It is a good example of an assumption to discuss.
- Better to avoid the idea of “the air as a sponge”: the saturation vapour pressure depends only on temperature and would be there even without air.
