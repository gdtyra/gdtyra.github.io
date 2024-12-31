# Distributed Systems
This is a collection of notes relating to distributed system design based on my experience and digesting things I've read.

## CAP Theorem
A distributed system can realistically only provide 2 out of 3 of the following at the same time:

- Consistency, meaning all clients at a given moment see the same / most up-to-date data
- Availability, meaning all clients are guaranteed to receive a valid response
- Partition tolerance, meaning the system can continue to operate despite a break in communication between nodes

Because network failure is unavoidable in practice distributed systems must be partition tolerant and make trade-offs between consistency and availability.

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

## Storage Options
- Local files: in some cases, it may be acceptable to store copies of data on a server's local file system. This may be the case for data that is some kind of configuration or pre-built read-only database and especially if it is acceptable for changes to the data to be performed as part of the regular application deployment process
- In-memory caches: caches such as Redis may be suitable for data that needs to be read frequently and which can be recomputed or retrieved in case the cache instance is reset
- Distributed file/object storage: storage services such as S3 may be suitable for records that don't need to be queried in real-time but are instead retrieved as-is on-demand or processed into some other form after being stored
- NoSQL databases are suitable for data that needs to be looked up by a particular key in applications that do not require or can otherwise work around the lack of strong consistency guarantees
- RDBMS instances should be considered when operations need to be strongly consistent and/or write operations need to be atomic. RDBMS instances can become a scaling bottleneck so they must be used thoughtfully (e.g. sharding and read-only replicas)


## Compute Options
- Serverless: serverless logic is suitable for any workloads that can tolerate a cold-start delay and do not have a need for the semi-persistent storage or more complicated setups that are possible on a dedicated server instance
- Dedicated server instances: traditional servers may be best when any cold-start delay is unacceptable, the workload would benefit from large amounts of memory, CPU, or temporary storage resources, when the component could benefit from semi-persistent storage on disk, or when there is a need for a more complicated setup with multiple processes cooperating on a single system. When made stateless and put behind a load balancer, they can scale horizontally but perhaps not as responsively

## Interface Options
- Synchronous API: most likely an HTTP/REST API, this is way a component is likely to interact with another when it needs some kind of response to a request, whether it be data or just a confirmation that the request was handled successfully
- Message queue: if an immediate response is not needed, using a message queue for input allows for decoupling of the components. The receiving component is free to process the workload at its own pace and can retry failed attempts as needed. Queue size is also a useful metric to track or use as an automatic scaling signal. Keep in mind that message queues typically deliver "at least once", not "only once". Some queues offer FIFO guarantees, otherwise messages may be received out of order.

## Caches and CDNs
Caches such as Redis or Memcache can be used to optimize and offload read operations for data that is read frequently

- Consider that, when a typical cache instance restarts, all cached data is suddenly lost. Although the cache is not a primary data store, the temporary or prolonged loss of a cache may severly impact the system
- In addition to an expiration policy based on time, caches must also have an eviction policy based on memory constraints. Most commonly this is LRU, but other options are LFU or FIFO

CDNs are essentially a form of cache that is placed closer to the clients rather than close to the other components of the application. They are also distinct in that they are directly accessed by the client as opposed to sitting behind the application's other interfaces

- CDNs, or other caches for that matter, may have invalidation APIs to bypass the automatic expiration policy. Alternatively, versioning can be used to ensure clients request the latest version of content
- Consider that, if the CDN does fail, you may want the client to be able to request resources from the origin as a fall-back


## Rate Limiting
Rate limiting is often a necessity even if you expect all your clients to behave reasonably. Without it, it is too easy for one client to accidentally or intentionally impact system performance.

Aside from determining how to identify or label traffic, the main decision is what the rate limiting policy/algorithm will be:

- Token bucket: clients are allotted tokens at a fixed rate up to a maximum. This allows for a degree of spiking traffic from clients
- Leaky bucket: this is effectively a queue with requests processed at a fixed rate regardless of spikes in traffic
- Fixed window counter: requests within a quantized time interval fall into the same bucket and are allowed as long as the bucket is not full. This can allow for more than expected traffic if a spike falls on the edge of a time window
- Sliding window log: fixes the edge-case with the fixed window counter but requires more memory. Request timestamps are kept in a cache. When a request arrives, timestamps of prior requests outside the current look-back window are dropped and the new timestamp is added. The request is allowed if the window is not full. Consider that even requests which are rejected must have their timestamp stored.
- Sliding window counter: similar to the fixed window counter but the counts in both the previous and current bucket are multiplied by how much of the "real" sliding look-back window overlaps them to get a more accurate running request rate

If we're dealing with an HTTP API, then HTTP 429 and associated response headers can be used to inform the client of when they may try again.


## Generating Unique IDs
The straightforward approach of generating incremental IDs is difficult in a distributed system, so alternatives are needed.

- Centralized "ticket generation servers" that each provide sequenced IDs
- UUIDs/GUIDs are a very simple and effective solution. However, they may not be suitable for situations that require smaller IDs or IDs that have a sequential relation to each other
- The "snowflake" method involves generating an ID made up of both sequential and unique source information such as timestamp, datacenter, machine ID, and machine-specific sequence number


## Client-Server Interaction
HTTP is client-initiated which works just fine for many situations, but situations where the client needs to receive events from a server are less straightforward.

- Polling: client repeatedly asks the server if there is anything it needs to know. This involves a tradeoff between delay upon receiving updates and overhead involved in opening and closing connections
- Long polling: client opens a connection with a relatively long timeout and closes the connection upon receiving a response or reaching the timeout before immediately connecting again. The benefits are that the client should receive updates as soon as they are available. The downsides are that it ties up server resources for connections that may not be very active
- WebSockets: a sort of "upgraded" HTTP connection, they allow for ongoing bidirectional communication. Downsides are that they require more complicated connection management on the server side. This sometimes involves a traditional "service discovery" API that provides the client with an optimal WebSocket server to connect to

## Other Thoughts
- Bloom filters can be used in situations to quickly determine that an item is definitely not in a set.
- Consider writing incoming data to a fast storage system and then responding to the client prior to committing the data to a more durable system.
- Offloading read operations to secondary sources can provide many benefits at once: data redundancy, lightening the workload on the primary read-write source, and improved latency in the case of CDNs or other geographically distributed caches.
- There should always be a canonical data source for data which is copied around the system. It should never be ambiguous what the "correct" data is when there is a disagreement.
- If it is economically sane, keep copies of data around prior to each transformation or modification.
- Ensure that actions are transactional in the sense that state is never left in a plausibly correct but actually undesired state.
- Consider versioning and backward compatibility of interfaces from the start because it is hard to add later and cheap to add upfront.
- Try to keep operations idempotent.
- The horizontal scaling difficulties associated with an RDBMS can be mitigated to some extent using application-level sharding with multiple writeable database instances and by queuing writes in message queues.
- Carefully consider the order in which things are done, e.g. transform then merge vs. merge then transform.