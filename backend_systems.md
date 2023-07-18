# Backend Systems

This page will become a collection of tips and guidelines for backend system design, but at the moment is just a few thoughts I had recently.

- Many OOP design principles apply to distributed systems. These systems should have well designed interfaces, limited responsibilities, and tolerate change well. The difference is that distributed systems have additional concerns relating to security, availability, consistency, and many failure cases that are not practical concerns within a single application instance but become plausible and likely in a distributed system. They also have parts that may need to change while other parts are still active without interrupting the entire system.
- System should have a well defined canonical data source for everything. It should never be ambiguous what the "correct" data is when there is a disagreement.
- Look out for opportunities for cheap breadcrumbs, i.e. have a canonical data store but also action logs that could be used to reconstruct the correct state of something if the canonical data store is broken. If it is economically sane, keep copies of data around prior to each transformation or modification.
- Ensure that actions are transactional in the sense that state is never left in a plausibly correct but actually undesired state.
- Consider versioning and backward compatibility of interfaces from the start because it is hard to add later and cheap to add upfront.