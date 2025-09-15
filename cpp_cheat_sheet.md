# C++ Cheat Sheet

## STL Algorithms

- `std::accumulate(first, last, initial, [op])`: perform summation on a range, optionally with given binary operation.
- `std::reduce(first, last, [initial, [op]])`: perform summation on a range, optionally with given initial value and binary operation.
- `std::transform_reduce(first, last, initial, biop, uop)`: perform the given unary operation followed by a binary operation on a range.
- `std::transform(first, last, output, uop)`: perform the given unary operation on the input range and store the result in the output iterator.
- `std::minmax_element(first, last, [cmp])`: returns a pair of iterators to the minimum and maximum elements according to the optional comparison function.
- `std::all_of(first, last, predicate)`: returns true if all elements evaluate to true.
- `std::lower_bound(first, last, value, [cmp])`: returns an iterator to the first value less than or equal the given one in a sorted range.
- `std::upper_bound(first, last, value, [cmp])`: returns an iterator to the first value greater than the given one in a sorted range.
- `std::binary_search(first, last, value, [cmp])`: returns true if the given value is found in a sorted range.
- `std::count(first, last, value)`: count occurrences of the given value in the range.
- `std::count_if(first, last, predicate)`: count values for which the predicate returns true in the given range.

## STL Modifying Algorithms

- `std::iota(first, last, initial)`: fill a range with incrementing values.
- `std::fill(first, last, value)`: fill a range with the given value.
- `std::generate(first, last, generator)`: fill a range with calls to a given generator.
- `std::generate_n(first, count, generator)`: write a number of values via calls to a given generator.
- `std::sort(first, last, [cmp])`: sort a random-access collection, optionally with a comparator.
- `std::partial_sort(first, middle, last, [cmp])`: move the smallest elements in a random-access collection to the area pointed to by first and middle, optionally with a comparator.
- `std::partial_sort_copy(first, middle, last, dest_first, dest_last, [cmp])`: like `partial_sort`, but copy the elements to a target range.
- `std::nth_element(first, nth, last, [cmp])`: move the nth-smallest element to the location pointed to by `nth`.
- `std::stable_sort(first, last, [cmp])`: sort a random-access collection while preserving the order of equivalent elements, optionally with a comparator.
- `std::shuffle(first, last, rng)`: shuffle a random-access collection.
- `std::remove_if(first, last, predicate)`: remove elements that match the predicate.
- `std::remove(first, last, value)`: remove elements that equal the value.
- `std::partition(first, last, predicate)`: moves elements to the left or right of the container based on the predicate and returns the pivot.
- `std::stable_partition(first, last, predicate)`: like `partition`, but preserves the relative order of elements.

## Random

- `std::mt19937{seed}`: the Mersene Twister pseudorandom number generator suitable for insecure number generation.
- `std::uniform_real_distribution<T>{min, max}`: range of real numbers with equal probability.
- `std::uniform_int_distribution<T>{min, max}`: sequence of integers with equal probability.
- `std::normal_distribution{mean, stddev}`: a normal distribution.
- `std::sample(first, last, out, n, rng)`: samples N items without replacement and write them to the output.
- `std::generate_canonical(rng)`: generates a random value between 0 and 1.

## Variants and optional

- `std::holds_alternative<T>(variant)`: returns true if the variant holds a value of the given type.
- `std::get<T>(variant)`: return the variant value assuming it holds the given type.
- `std::get_if<T>(variant)`: returns a pointer to the variant value assuming it holds the given type, or `nullptr` otherwise.
- `std::visit(function, variant)`: call a function or other callable with the variant's value.
- `std::monostate`: type to use as the first type in a variant when the "real" first type is not default constructible.
- `optional.has_value()`: returns true if the optional is not `std::nullopt`.

## Iterators

- `std::distance(first, last)`: returns a difference value representing the distance between the iterators.
- `std::advance(iter, n)`: effectively increment an iterator N times.
- `std::next(iter, n)`: returns an iterator N steps ahead of the given one.
- `std::prev(iter, n)`: returns an iterator N steps behind the given one.
- `std::back_insert_iterator{container}` or `std::back_inserter(container)`: an output iterator that calls `push_back` on the container.
- `std::front_insert_iterator{container}` or `std::front_inserter(container)`: an output iterator that calls `push_front` on the container.
- `std::insert_iterator{container, iter}` or `std::inserter(container, iter)`: an output iterator that starts inserting at the given iterator.

### Iterator concept

Iterator types should have `difference_type`, `value_type`, `pointer` (void if not wanted), `reference`, and `iterator_category` defined.

The iterator category tags are:

- `std::input_iterator_tag`: Can be read and only moved forward.
- `std::output_iterator_tag`: Can be written to and only moved forward.
- `std::forward_iterator_tag`: Like an input iterator, but can also be copied and used to read the container multiple times.
- `std::bidirectional_iterator_tag`: Like a forward iterator, but can move in both directions.
- `std::random_access_iterator_tag`: Can be moved forward and back an arbitrary amount to reach any element in the container.

## Threading

- `std::this_thread::sleep_for(chrono_time)`: sleep for the given duration.