# Software Design
The following is a collection of guidelines for class and general software component design based on things I've read and / or found to be helpful in my experience.

## High-level considerations
- Design systems in such a way that engineers can make changes to one aspect of the system without modifying or needing to understand other parts of the system.
- Good systems can tolerate change well without rippling effects

# Use of OOP and class design
## SOLID
- Single Responsibility: a class should do the smallest possible useful thing
- Open-Closed: objects should be open to extension and closed for modification; i.e. they should be extensible without modifying the existing code
- Liskov-Substitution: objects should be replaceable by subtypes without altering correctness
- Interface Segregation: many client-specific interfaces are better than one general-purpose interface
- Dependency Inversion: this seems to boil down to "depend on abstractions"

## Constructors and dependency injection
- Constructors should be simple and serve only to fully validate and initialize an object
    - DO assign values and collaborator objects that are received by the constructor to instance fields
    - DO feel free to create simple value / plain-old-data objects as long as they are state-focused and have minimal behavior
    - DO perform validation or simple normalization of input data
    - DO NOT create complex objects that have substantial behavior of their own. These collaborator objects should be received instead
    - DO NOT call out to static methods or free functions unless they are doing simple validation or normalization
- Creation of object graphs should be the responsibility of a dedicated dependency injection framework or dedicated factory / builder classes that do nothing but create objects

## Interfaces and object relationships
- Good design results in objects that can tolerate change easily
    - Try to depend on behavior, not data; hide fields and data structures, even within a class
    - Clients of an object should "ask" for what they want rather than "tell" the object what to do. This kind of interaction allows more flexibility for "how" the result is accomplished
    - Prefer to depend on things that change less often. Pay attention to the direction of dependencies to ensure that is the case
- Good design naturally progresses toward small independent objects that rely on abstractions
    - Warnings that a class is doing too much include...
        - It is hard to name
        - It has fields that are only used in some methods, or has static methods that only operate on parameters
        - It works with simple collaborators that don't have their own behavior (perhaps behavior should be moved into those classes)
    - Watch out for "hidden" interactions between the main responsibilities of a class
    - Try asking "{class}, what is your {attribute}?" or "{class}, can you {method}?" and see if it makes sense
    - An object may have a single responsibility but require more "context" than it needs to do it
- Objects should interact only with immediate collaborators (Law of Demeter)
    - Violations of this guideline suggest an object's interface might be lacking
    - "Fluent" interfaces are an exception, as are chaining methods that return the same interface
    - Delegation superficially appears to fix violations and may in fact be an improvement, but delegation itself can also just hide the problem
    - There may be exceptions to apparent violations; it's really about whether the code is "reaching" through the object graph in ways that are fragile. Code should not invoke behavior just because it happens to "know" a long path to get to that behavior. You have to ask whether it "should" know that path or not.
    - Objects passed into a method should be used for something other than reaching in to retrieve another object deeper in the object graph
- While inheritance is a good fit in some cases, it has drawbacks and may be used inappropriately
    - Inheritance gives "free" delegation at the cost of a prescribed hierarchy
    - Only use inheritance when it truly provides benefits that justify it. It is often less flexible and less reusable than composition
    - Don't prematurely create class hierarchies with only one implementation
    - If a problem really calls for an inheritance structure, consider "hook" methods to avoid calls to super (template method pattern)
- Composition is often a more flexible and less brittle solution to OOP problems. It promotes many small objects with clear responsibilities and interfaces
    - Composition allows for a more flexible and reusable structure than inheritance but requires the object to have explicit knowledge about delegation
    - Standard compositional mechanisms for altering class behavior: decorator and strategy patterns

## Subtle dependencies
- Even method names, expected arguments, and argument order represent dependencies
    - Remove argument-order dependencies (named keywords in Python and ruby, or a dedicated "Params" object in Java or similar languages)
    - Context objects sound like a good way to minimize changes in method signatures, but they obfuscate the actual dependencies of a class or method when they are not specific to a particular method or group of methods
- Global state is generally not okay except when it is immutable or when the information only flows one way, as with a Logger interface

## Tips for refactoring a large class
- Extract extra responsibilities from methods to reveal reusable pieces
- Isolate to an inner class if you don't want to move it out to a new class yet
- If it is too much effort to properly fix object relationships, you can at least easily isolate the bad relationship