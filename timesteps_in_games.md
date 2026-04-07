# Timesteps in Games

## Fixed timestep

A timestep is chosen (e.g. 16 ms) and simulation logic is run however many whole steps are required to account for time that has passed since the last frame. Leftover time is accumulated and accounted for in the next frame.

This handles occasional slow frames acceptably, but if the engine is never able to deliver frames within the expected timestep then the simulation will only fall further behind.

## Variable timestep (possibly with clamping)

In every frame, the world state advances proportionally with the amount of real time that has passed since the last frame was delivered.

Optionally, this "delta time" can be clamped to prevent too much of a jump in world state between frames (e.g. to avoid phasing through a wall).

## Sub-stepping

For movement or collision that is particularly sensitive (e.g. fast projectiles or interactions that require precision), the engine may run operations repeatedly when the "delta time" is greater than a predefined timestep length. For example, if the delta is 40 ms, run the logic repeatedly: twice with delta 16 ms and once more with delta 8ms.

## Continuous Collision Detection (CCD)

Alternatively or in addition to sub-stepping, CCD "capsule sweeps" perform collision tests across the entire volume or area that an object would have moved.

