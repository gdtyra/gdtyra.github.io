# C++ Templates and Metaprogramming

This is a collection of notes about C++ behavior that I found to useful, non-obvious, or hard to remember.


## Overload ambiguity

Overload ambiguities weren't really an issue until I started playing with templates heavily. Maybe because I don't have a very deep understanding of the C++ type system, I was surprised by what is and isn't considered ambiguous in the following examples:

```cpp

// Ambiguous between const-ref and value
void foo(int) { }
void foo(int const&) { }
foo(1);


// I thought maybe the above would not be ambiguous for a type that isn't copyable,
// but the ambiguity error remained. An error regarding the missing copy constructor surfaced
// only after removing the const reference option.
struct A {
    A(A const&) = delete;
    A& operator =(A const&) = delete;
};
void foo(A) { }
void foo(A const&) { }
A a{};
foo(a);

// NOT ambiguous; r-value reference and non-const reference take priority
void foo(int const&) { }
void foo(int&) { }
void foo(int&&) { }
int x = 1;
int const y = 2;
foo(x); // binds to int& if present, otherwise int const&
foo(y); // can only bind to int const&
foo(3); // binds to int&& if present, otherwise int const&
```


## Templates and overload resolution

This is largely intuitive, but there are many cases where I wasn't entirely sure what to expect without testing.

```cpp

struct A {};
struct B : A {};

template <class T>
void foo(T) { }

template <class T>
void foo(T*) { }

template <class T>
void foo(std::list<T>) { }

void foo(std::list<float>) { }

void foo(std::list<A>) { }

void foo(std::list<A*>) { }

template <class T>
void foo(std::list<std::enable_if_t<std::is_base_of_v<A, T>, T>>) { }


int x = 5;
foo(x); // calls foo(T)
foo(&x); // calls foo(T*)
foo<int*>(&x); // calls foo(T)
foo(std::list<int>{}); // calls foo(std::list<T>)
foo(std::list<float>{}); // calls foo(std::list<float>)
foo(std::list<A>{}); // calls foo(std::list<A>)
foo(std::list<B>{}); // calls foo(std::list<T>)
foo(std::list<B*>{}); // calls foo(std::list<T>)
foo<B>(std::list<B>{}); // calls foo(std::list<std::enable_if_t<std::is_base_of_v<A, T>, T>>)

```

What if I want an overload specifically for lists of objects derived from A? Using `enable_if_t` as above doesn't work with type deduction and needs `B` to be specified as the type parameter explicitly. The following possibilities don't work at all because they are considered ambiguous in combination with the general list overload:

```cpp

template <class T>
std::enable_if_t<std::is_base_of_v<A, T>, void> foo(std::list<T>) { }

template <class T, class = std::enable_if_t<std::is_base_of_v<A, T>, void>>
void foo(std::list<T>) { }

```

One option is to resolve the ambiguity by using SFINAE to enable different implementations in a mutually exclusive way:

```cpp

template <class T>
std::enable_if_t<!std::is_base_of_v<A, T>, void> foo(std::list<T>) { }

template <class T>
std::enable_if_t<std::is_base_of_v<A, T>, void> foo(std::list<T>) { }

```

Alternatively, tag dispatching can be used which seems easier to follow:

```cpp

template <class T>
void foo_impl(std::list<T>, std::true_type) { }


template <class T>
void foo_impl(std::list<T>, std::false_type) { }

template <class T>
void foo(std::list<T> lst) { 
    foo_impl(lst, std::is_base_of<A, T>{});
}

```

These options may be acceptable in many cases, but they require all implementations to be coupled together so that they mutually exclude each other. What I really want is a hierarchy of implementations where the more generic implementations are entirely unaware of any other more specific implementations that may exist.

According to my limited understanding and to ChatGPT (shout-out ChatGPT, love ya 😘), this can't be accomplished with only function templates. Instead, we have to make use of struct templates and partial specialization which is not available with function templates.

```cpp

template <class T, class Enable = void>
struct foo_impl{
    static void apply(std::list<T>) { }
};

template <class T>
struct foo_impl<T, std::enable_if_t<std::is_base_of_v<A, T>>> {
    static void apply(std::list<T>) { }
};

template <class T>
int foo(std::list<T> lst) {
    return foo_impl<T>::apply(lst);
}

```

The primary template for `foo_impl` contains what would be the default implementation of the function. A dummy template parameter `Enable` is used as a sort of slot for doing SFINAE when specializing the template for types matching arbitrary criteria. It is given an arbitrary default type `void` so it doesn't get in the way. The type assigned to Enable is irrelevant; it just provides a place in the template to use `std::enable_if_t` when specializing. Through SFINAE, the use of `std::enable_if_t` in the specialization will cause C++ to ignore the specialization when the type given doesn't fulfill the criteria. In this example, the specialization requires `T` to be derived from `A`, otherwise the primary template will be used.

We are also able to hide all this behind a regular template function. If anyone wants to specialize behavior for a given type or types, they just need to define another specialization without modifying the default.

## Template functions are okay with returning void

I would have thought I needed to explicitly handle the situation where a template function makes use of another function that may or may not be `void` depending on the arguments, but this is handled automatically:

```cpp

void bar(int) {}
int bar(float) { return 0; }

template <class T>
auto foo(T x) {
    return bar(x);
}

// These both work
foo(1);
foo(1.0f);

```

## Placement of variadic template arguments

In the case of class templates, the compiler gives me a message specifically saying that variadic parameters must be the last template parameters.

```cpp

// Okay
template<class First, class... Remaining>
struct Bar {};

// Not okay
template<class... Remaining, class Last>
struct Bar {};

// Not okay
template<class First, class... Remaining, class Last>
struct Bar {};

```

Template functions don't give me an error explicitly telling me this, but rather fail in different ways depending on how I've ordered things and whether I've listed the template types or used deduction.

When relying on deduction the order of the template arguments themselves is not strict, but putting them anywhere but the end breaks your ability to provide all the type parameters explicitly because they are greedily assigned to the variadic arguments. It still "works" in that you can let deduction take care of the other types.

```cpp
template<class One, class... Remaining>
void foo(One&&, Remaining&&...) { }

foo(1, 2, 3, 4); // Okay
foo<int, int, int, int>(1, 2, 3, 4); // Okay

template<class... Remaining, class One>
void foo(One&&, Remaining&&...) { }

foo(1, 2, 3, 4); // Okay
foo<int, int, int>(1, 2, 3, 4); // Okay... One is deduced to be an int
foo<int, int, int, int>(1, 2, 3, 4); // Fails because compiler thinks 5 parameters are expected in total

```

Putting the function parameter pack itself anywhere but the end seems to completely break type parameter deduction, but the types can still be given explicitly.

```cpp

template<class One, class... Remaining>
void foo(Remaining&&..., One&&) { }
foo(1, 2, 3, 4); // Fails, apparently because deduction results in Remaining being empty
foo<int, int, int, int>(1, 2, 3, 4); // Okay

```

So, it seems that if you don't stick to putting variadics at the end, you sacrifice either deduction or the ability to specify all types explicitly.

At first I thought I was able to do something useful by reordering them. In this example, I'm able to recursively process the parameters in reverse order:

```cpp

template<class T>
void foo(T&& t) {
    std::cout << t << std::endl;
}
template<class Last, class... Remaining>
void foo(Remaining&&... remaining, Last&& last) {
    std::cout << last;
    foo<Remaining...>(std::forward<Remaining>(remaining)...);
}

foo<int, int, int, int>(1, 2, 3, 4); // output is 4321

```

However, using entirely unrelated types reveals a problem. I'm able to specify the type of 'Last' by hand on the top-level call, but for recursive calls 'Last' receives the wrong type.


```cpp

template<class T>
void foo(T&& t) {
    std::cout << t.getChar() << std::endl;
}
template<class Last, class... Remaining>
void foo(Remaining&&... remaining, Last&& last) {
    std::cout << last.getChar();
    foo<Remaining...>(std::forward<Remaining>(remaining)...);
}

struct A { char getChar() const { return 'A'; } };
struct B { char getChar() const { return 'B'; } };
struct C { char getChar() const { return 'C'; } };

foo<C, A, B>(A{}, B{}, C{}); // Fails because recursion attemps to call foo<A, B>(B&&, A&&) with arguments of type A&& and B&&

```

## What is the purpose of `std::forward`?

In trying to answer this question, I first found I need to understand what a forwarding reference is starting with the fact that the use of `&&` on parameters in a template is distinct from the use of `&&` outside of template code to accept an rvalue reference. I found by observing compiler error messages that what `&&` on parameters in a template actually does is change how the template parameters are deduced.

In the following example, the template parameters for `foo` were deduced to be `int&, const int&, int*, int, A&`:

```cpp

template <class... Ts>
void foo(Ts&&... args) { }

int x = 1;
int const y = 2;
A a{};
foo(x, y, &x, 5, a);

```

If I remove the `&&`, the deduced types change to `int, int, int*, int, A` which explains what `&&` was doing while also telling me the compiler distinguishes between pointers and non-pointers regardless of whether forwarding references are used.

Now that we understand that, lets expand on the example to see what `std::forward` does:

```cpp

void bar(int&) { std::cout << "ref" << '\n'; }
void bar(int&&) { std::cout << "rvalue ref" << '\n'; }
void bar(int const&) { std::cout << "const ref" << '\n';
void bar(int*) { std::cout << "pointer" << '\n'; }

template <class... Ts>
void foo(Ts&&... args) {
    (bar(std::forward<Ts>(args)), ...);
    std::cout << "---\n";
    (bar(args), ...);
}

int x = 1;
int const y = 2;
foo(x, y, &x, 5);

```

This examples passes forwarding references from a template function to a family of other functions using and then without using `std::forward`. The output of this tells me that the main purpose of `std::forward` is to ensure that rvalue references do not become regular references when passing them through a template function. For other parameter types, it does nothing.

```
ref
const ref
pointer
rvalue ref
---
ref
const ref
pointer
ref
```


## Template idioms

### Recursively processing variable template arguments

```cpp

void foo() {
    std::cout << std::endl;
}

template<class First, class... Remaining>
void foo(First&& first, Remaining&&... remaining) {
    std::cout << first;
    (foo(std::forward<Remaining>(remaining)), ...);
}

foo(1, 2, 3, 4)
// prints 1234

```

### Using specialization or deduction to unpack types

```cpp

template<class T>
struct Foo;

template<class... Ts>
struct Foo<std::tuple<Ts...>> {
    static constexpr std::size_t n = sizeof...(Ts);
};

template<class Tuple>
std::size_t bar(Tuple&&) {
    return Foo<Tuple>::n;
}

template<class... Ts>
std::size_t foo(Ts&&... ts) {
    return bar(std::tuple<Ts...>(std::forward<Ts>(ts)...));
}

foo(1, 2.0, '3'); // returns 3

```

### Tag dispatch

```cpp

template <class T>
int foo(T&&, std::true_type) {
    return 1;
}

template <class T>
int foo(T&&, std::false_type) {
    return 2;
}

template <class T>
int foo(T&& t) {
    return foo(std::forward<T>(t), std::is_integral<T>{});
}

foo(5); // returns 1
foo(5.0); // returns 2

```

### Type holder dispatch

```cpp

template <class T>
struct Holder {
    using type = T;
};

template <class T>
int foo(Holder<T>) {
    return 1;
}

template <class... Ts>
int foo(Holder<std::tuple<Ts...>>) {
    return 2;
}

foo(Holder<int>{}); // returns 1
foo(Holder<std::tuple<int, float>>{}); // returns 2

template <class T>
constexpr Holder<T> holder = Holder<T>{};

foo(holder<int>); // returns 1
foo(holder<std::tuple<int, float>>); // returns 2

```