# Distributed Systems
This is a collection of notes relating to distributed system design based on my experience and digesting things I've read.

## Concerns
Most OOP design principles also apply to distributed systems. Components of the system should have thoughtfully designed interfaces, decoupled components with limited responsibilities, and should tolerate change well. The difference is that distributed systems have additional concerns relating to security, availability, consistency, and many failure cases that are not practical concerns within a single application instance but become plausible and likely in a distributed system.

- Throughput: these systems often deal with large amounts of traffic and data which needs to be processed in a timely manner
- Latency: although related to throughput, its worth thinking about delay between input and end result as a separate concern
- Availability: components need to be ready to respond to incoming workloads
- Resilience: how does the system behave and recover when one or more components fail or become unavailable
- Synchronization: the system must gracefully deal with things happening out of order, at the same time, or after a delay
- Data integrity: data that is needed should never be lost due to a component failure or otherwise corrupted
- Security: access to data and operations must only be exposed to the intended audience
- Traffic patterns: the system may fluctuate from its baseline workload either predictably or unexpectedly
- Bad actors: especially if part of the system is exposed publicly, requests to the system from bad actors may disrupt the system for legitimate users
- Misbehaving clients: even if there is no malicious intent, clients may misbehave and generate invalid or excessive requests 

## Tools and Countermeasures
These are some options for dealing with the concerns above.

- Scaling (throughput): ideally horizontally as explained below, scaling is the primary way to increase throughput
- Decoupling (availability, resilience): in this context it largely refers to handling temporary unavailability of a component and is often accomplished with message queues or other buffers 
- Data redundancy (availability, resilience, throughput, data integrity): besides obviously protecting against data loss, having additional read-only data sources allows for scaling aspects of the system that only need read access to data and they can also be hot-swapped in as the target for write operations if the primary fails
- Rate limiting (availability, bad actors, misbehaving clients): rate limiting may be added at certain points in the system to prevent bad clients from impacting availability
- Authentication (security, bad actors, misbehaving clients): confidently identifying the source of requests is the first step in controlling access and makes it easier to effectively handle problematic clients
- Access control (security, bad actors, misbehaving clients): if clients are being confidently identified via an authentication mechanism, then access controls can be put in place to restrict how the system is used

There are also some practices that can work to our advantage:

- Avoid stateful components. Stateless components can be scaled on demand and can process pieces of work without concern for what happened before or after
- Offload read operations to secondary data sources. This results in data redundancy as mentioned above and ensures the primary data instance is able to make use of its throughput for the write operations which typically cannot scale as easily
- Reject bad inputs as early as possible. By dropping an input as soon as it can be determined that it is unauthorized or invalid, less of the system needs to spend resources processing it
- Break data and tasks into discrete chunks. In general, this aids in scaling and resilience by allowing more work to be done at once and allowing partially completed work to be picked up

## Vertical and Horizontal Scaling
Vertical scaling refers to simply adding more CPU, network, and memory resources to a fixed number of instances to increase throughput. It is simple and can be done without architectural changes, but there are limits to how far it can get you. Additionally, vertical scaling does not provide additional redundancy or resilience to the system. Therefore, it is best to design systems with horizontal scaling in mind.

Horizontal scaling refers to spreading workloads across an adjustable fleet of interchangeable instances. It requires more consideration for the problems inherent in distributed systems, but the benefit is a more scalable and resilient system.

It is easy enough to run logic on a scalable fleet of stateless servers that share a common data source, so the difficulty in horizontal scaling often comes down to where the shared data sources are and how they are accessed. If a fleet of stateless web servers read and write to a single shared database instance, then the system is not actually scalable.


## Other Thoughts
- There should always be a canonical data source for data which is copied around the system. It should never be ambiguous what the "correct" data is when there is a disagreement.
- If it is economically sane, keep copies of data around prior to each transformation or modification.
- Ensure that actions are transactional in the sense that state is never left in a plausibly correct but actually undesired state.
- Consider versioning and backward compatibility of interfaces from the start because it is hard to add later and cheap to add upfront.
- Try to keep operations idempotent