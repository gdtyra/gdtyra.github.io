# Refactoring

## Identify problematic areas by measuring churn

Arguably it makes sense to approach refactoring not with the goal identifying and fixing poor design, but rather by identifying code that is causing actual problems or friction. Messy code that works reliably, performs well, and has no reason to change is not necessarily a problem.

Git history can be used to to help identify files, classes, and functions that have frequent, large changes. This signals either an important code path which might benefit from 

One can also look at 2-3 recent features or bug fixes to find ares where substantial or complex changes were needed.

## Read through and actively consider what is confusing

- Did you have to jump around to various functions to understand another?
- Was a name misleading or outright inaccurate?
- Did you have to hold too much state at once?

## Consider classic "code smell" signals

- Long functions and long parameter lists
- "Feature envy", when a function mostly manipulates another object's data
- "Shotgun surgery", when a concept is scattered across many files
- Primitive obsession, when fundamental types are doing the job of a proper type
- Inconsistent vocabulary, when different words refer to the same concept
- Misleading or unclear names
- Deep nesting
- Duplicated logic with or without subtle variations
- Mixed levels of abstraction in one function
- God objects, classes or modules that know about or do far too much
- Data clumps, the same group of variables being passed around together repeatedly
- Divergent change, one module has to be edited for many unrelated reasons
- Speculative generality, over-engineering
- Temporal coupling, methods must be called in a specific and non-obvious order to function correctly
- Inappropriate intimacy, two classes or modules reaching into each other's internal state
- Boolean flag parameters that switch behavior
- Anemic domain model, data classes with no behavior and "manager" or "service" classes that do all the logic
- Message chains, client code asking for an object, which asks for another object, and so on
- Loops that could be replaced with functional paradigms
- Lazy elements, constructs that don't do enough to justify their existence

## Consider computable metrics

- Cyclomatic complexity: a count of independent paths through a function. More than 10 is a commonly cited flag and more than 20 is a strong one.
- Parameter count and nesting depth: a function with 6 parameters or 5 levels of nesting may be problematic.
- Fan-in and fan-out: a function with high fan-out may "know" too much, and one with high fan-in has a lot depending on it.
- Coupling vs. cohesion: cohesion metrics like LCOM (lack of cohesion of methods) measure whether methods in a class actually operate on the same data.
- Law of Demeter violations: count of deep method call chaining.