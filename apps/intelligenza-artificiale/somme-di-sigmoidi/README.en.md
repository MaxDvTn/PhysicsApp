# Sums of sigmoids

A neuron with a large weight is almost a step; many steps can draw any continuous function. That is the idea behind the universal approximation theorem, here in three tabs to explore.

## How to use it

1. **One neuron.** Move the weight, position and height sliders of each neuron c·σ(w(x − m)) and watch how the sum changes. Pick a challenge (a bump, a staircase, a step down) and move the sliders until the green curve covers the red one: with an error below 0.15 the challenge is won.
2. **The proof.** Follow the construction step by step with the Grid, Staircase, Network and Neurons buttons. Choose the function (or write your own, with x, sin, cos, exp, abs, sqrt, log) and the number N of neurons; “Use the theorem's w” sets the weight that the proof guarantees.
3. **Training.** Press **Start**: a network trains in the browser with gradient descent (Adam). Compare the trained network with the one built by hand with the same number of neurons, change the activation (sigmoid or ReLU), the number of samples and the noise.

## What to look for

- The trained network usually beats the constructed one with the same N, because it uses different weights for each neuron and puts the steps where they are needed.
- With “Show [−6, 6]” you can see that outside the range of the data there is no guarantee at all.
- With few samples, noise and many neurons, overfitting appears: the network also follows the errors in the data.

All the computation happens in the browser: no connection is needed after the page has loaded.
