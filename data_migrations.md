# Data Migrations
Data migrations are straightforward if we accept that the system can remain unavailable indefinitely during the migration. It is also straightforward enough to provide read operations throughout a migration. The main complexity with migrations is how to perform them without disruption of write operations in the system.

When planning a migration, we have to consider some questions:

- How much data are we dealing with?
- Do we need to keep all the data?
- What components are depending on 
- Why are we migrating?
- Is this an opportunity to transform, sanitize, or filter the data in some way?
- What operations need to remain available to clients during the operation?
- Does the answer change depending on the expected duration of the migration? In other words, is a short outage okay but a longer outage not acceptable?

Ultimately, a successful migration must do these things:

- Ensure that the new datastore contains all desired data from the old datastore up to and including the moment that writes to the old datastore are stopped
- Ensure that the new datastore is able to successfully handle the traffic that the old datastore was receiving
- Gracefully handle a rollback scenario in case things go wrong

## Migrating via a secondary background process
One approach for migrating would be to leave the existing system as-is while bringing the new datastores up to speed before switching over. That could look something like this:

1. If there is more than one component directly reading or especially writing to the datastore, consider first standing up an API in front of the datastore and directing all operations through that
2. Implement write operations toward the new datastore and run them alongside writes to the old (failed writes to the new datastore should be monitored but not yet appear as a failure to the client)
3. After observing that writes to the new datastore are reliable, modify the implementation to require successful writes to both datastores. From this point on, incoming data should exist in both or none of the two datastores. On the other hand, effective latency and failure rate will be the worst of the two datastores. You may want a mechanism for quickly disabling this requirement if a problem does emerge
4. Perform backfill of historic data into the new datastore as an offline process
5. Perform any validation of the new datastore
6. Switch read operations over to the new datastore, perhaps gradually. Because writes to the old datastore are still ongoing, we can gracefully rollback to read from the old datastore at any point
7. After observing that the system is stable when reading from the new datastore for a sufficient amount of time, writes to the old datastore can be disabled. The amount of wait time is a tradeoff between storing twice as much incoming data and the impact on latency or failure rate that the old datastore may be having.

## Migrating as part of regular operations
Alternatively, data can be migrated if and when it is accessed. For example, if user accounts are being migrated or merged into a different system, users may be required to verify and update their information and credentials the next time they attempt to login. After some time, only the least regular users (or, more generally, least frequently accessed data) remains unmigrated and can be dealt with via a secondary process with a smaller scope that is less likely to impact the users or data that are most often needed.