# C++ Cheat Sheet

## STL Algorithms

- `std::accumulate(first, last, initial, [op])`: perform summation on a range, optionally with given binary operation.
- `std::reduce(first, last, [initial, [op]])`: perform summation on a range, optionally with given initial value and binary operation.
- `std::transform_reduce(first, last, initial, biop, uop)`: perform the given unary operation followed by a binary operation on a range.
- `std::transform(first, last, output, uop)`: perform the given unary operation on the input range and store the result in the output iterator.
- `std::minmax_element(first, last, [cmp])`: returns a pair of iterators to the minimum and maximum elements according to the optional comparison function.
- `std::all_of(first, last, predicate)`: returns true if all elements evaluate to true.

## STL Modifying Algorithms

- `std::iota(first, last, initial)`: fill a range with incrementing values.
- `std::fill(first, last, value)`: fill a range with the given value.
- `std::generate(first, last, generator)`: fill a range with calls to a given generator.
- `std::generate_n(first, count, generator)`: write a number of values via calls to a given generator.
- `std::sort(first, last, [cmp])`: sort a random-access collection, optionally with a comparator.
- `std::shuffle(first, last, rng)`: shuffle a random-access collection.
- `std::remove_if(first, last, predicate)`: remove elements that match the predicate.
- `std::remove(first, last, value)`: remove elements that equal the value.
- `std::partition(first, last, predicate)`: moves elements to the left or right of the container based on the predicate and returns the pivot.

## Random

- `std::mt19937{seed}`: the Mersene Twister pseudorandom number generator suitable for insecure number generation.
- `std::uniform_real_distribution<T>{min, max}`: range of real numbers with equal probability.
- `std::uniform_int_distribution<T>{min, max}`: sequence of integers with equal probability.
- `std::normal_distribution{mean, stddev}`: a normal distribution.