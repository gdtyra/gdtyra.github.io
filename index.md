# Intro
Hello! Thank you for taking the time to look beyond what's written in my resume. The following is a candid retrospective and self-reflection on my work experience. I don't necessarily expect anyone to read it, but its something I needed to do for myself in order to answer interview questions sufficiently and I figured I would make it available.

## Career Break
There isn't any one specific reason I decided to take a career break, but I probably wouldn't have made the decision without the alignment of 3 things in particular:

1. My team at the time had just gone through restructuring that left me on a new, small team that didn't yet own any systems and didn't have a clear vision of what we would own or build.
2. I assumed we would start working from the office again, but I had moved away from the office during the pandemic and had no plan to move back.
3. I had been feeling like I should explore opportunities at other companies for a number of years anyway simply to experience different environments and technology stacks

I didn't immediately look for a new role because there was no need and I wanted to get a better sense of whether remote work is here to stay or not. I prefer to live within walking distance of the office, so the difference between hybrid and fully remote work is very significant to me.

## What I'm Looking For
A role that involves at least one of these things:

- A product / service that feels interesting, relevant, important, or otherwise meaningful
- An opportunity to apply my experience and be of value
- An opportunity to learn a technology or stack that I'm less familiar with
- An opportunity to take on more leadership responsibilities

## Traits
These are the traits that I see as defining me and my behavior in relation to my work, the project, and the people around me. I see these traits as generally good, but they also imply certain roles, projects, and work environments that allow me to be most effective and biases I need to account for and be aware of.

- **Driven by technical curiosity**
    - &#x2714;: I'm in this field because I find computers and everything related to them to be very interesting. I'm driven by a curiosity in how things work and I have at least some familiarity and interest in everything from hardware to front-end UI. I'm more than happy to dive into unfamiliar territory and am able to learn quickly. I already have enough foundational knowledge in most areas to at least know where to begin when tackling an unfamiliar problem.
    - &#x26a0; I have broad knowledge, but am not specialized in any particular area. The product I'm working on or problem I'm solving is very much secondary in my mind. Unless the product is itself related to computers, software development, or an interesting technology, I probably don't care that much about it aside from my responsibility to deliver quality results to those who are depending on me. I expect someone else to be defining the high-level goals of what we are building, what the measurements of success will be and, unless the product is an API, what the user experience should look like.
- **Driven by perceived responsibility and desire to meet or exceed expectations**
    - &#x2714;: If I'm given a well-defined responsibility, I am highly motivated to handle that responsibility well. This might be delivering a feature by a target date, doing research to provide a planning estimate, or leading a particular weekly meeting.
    - &#x26a0; This breaks down if the expectations or constraints are unclear. Features usually have well-defined acceptance criteria and target dates, but lets say I'm tasked with researching and documenting different options for how to build something. I will likely have immediate ideas based on what I am already familiar with, but how much additional exploration and research should I do before calling it "done"? I do have my own sense of when I've done "enough", but if I'm given a predetermined time constraint then I will naturally make more effective use of the time.
- **Highly agreeable**
    - &#x2714;: I get along well with everyone. I'll offer my thoughts, but I'm happy to go along with team consensus or what leadership has decided on. If I really thought a huge misstep was being taken then I'm sure I would speak up, but I've never felt that way so far.
    - &#x26a0; I don't often have strong opinions. In code reviews, for example, I will most likely approve if it is functionally correct, has good tests, and there is nothing else objectively problematic about the change. I offer suggestions for anything else that I think could be done better, but leave it up to the implementer as I don't want to be the reason for holding up the change. If I do personally feel interested in improvements, I may do it myself later as part of other changes.
- **People pleaser**
    - &#x2714;: I want people to be happy with me. This is probably the force behind the desire to meet expectations as explained above, but I also enjoy helping people who are stuck on a problem or are having trouble understanding something.
    - &#x26a0; I am biased toward saying what people want to hear. For example, if I think someone will react badly to a longer project estimate, I may give a more optimistic estimate than I would otherwise.
- **"Perfectionist", for lack of a better term**
    - &#x2714;: I aim to do things as well as possible while also feeling like there is always something to improve.
    - &#x26a0; I will work on details endlessly if there isn't some kind of externally imposed time constraints or completion criteria.
- **(Re)Inventor**
    - &#x2714;: I enjoy building things and am able to use my existing knowledge to start building solutions quickly.
    - &#x26a0; I have a bias toward building from lower-level tools I'm familiar with as opposed to finding and using appropriate pre-built solutions. This comes from an eagerness to start building over doing research, desire to avoid bloated dependencies, and a preference to learn tools and exercise skills that are more generalizable over learning tools and frameworks that have a specific use case.

# Projects
## Sustainability: Carbon Footprint (2020 - 2021)
### Product
This team was responsible for part of a larger system that calculates an estimate of the carbon footprint of Amazon's operations. Specifically, I was briefly part of a small team building the ingestion pipeline for energy usage data. This pipeline received documents from a handful of sources and formats, normalized and aggregated them by site and month, and filled in any missing data with estimates based on available data from other similar sites. The output consisted of parquet files delivered to S3 buckets owned by downstream parts of the system.

### Complexity
The work was technically pretty straightforward and the team was small with clearly defined responsibilities. I needed to become familiar with Scala and AWS CDK and had to deal with more complicated cross-account IAM relationships and roles, but overall it was a breath of fresh air with regard to how easily testable and decoupled the system was from any others and with how unidirectional the data flow was.

### Stack
The "pipeline" was essentially a series of AWS Lambda functions implemented in Scala which expected inputs in one S3 bucket and delivered transformed outputs to another. An AWS Step Function orchestrated the order of these transformations, running them in parallel when possible. Granular IAM roles were used throughout. CDK was used to define the infrastructure.

### Role
This was a temporary assignment with another team in the organization to help them stay on schedule.

I ramped up by writing standard security review documentation of the system, and then my main body of work was implementing the "proxy" calculation and lookup. The "proxy" lookup table was a hierarchical table keyed by site attributes like geographic location and type of site. It was populated with averages of real energy usage data we had and then used for estimates to fill in any gaps in the actual data prior to delivery to downstream systems.

### Team
This was a small team consisting of 3 engineers, an SDM, and a product manager. I was the 3rd engineer temporarily joining the team to help them stay on schedule.
 

## Sustainability: Packaging (2018 - 2020)
### Products
When I joined, this team owned a packaging certification system and website used by Amazon vendors to certify their products against packaging standards like "frustration-free" and "ships-in-own-container" (not over-boxed). They also owned an almost-launched service that determined whether given inventory was eligible for donation (e.g. not hazardous, not expired, not recalled, among others).

After I joined, much of the team's focus turned toward building a new system to begin replacing the existing packaging certification system which was not well understood, buggy, and brittle. This initiative was driven by a need to allow certifications and a more granular inventory level than the system currently supported.

I also built a service to aid in the creation of product labeling workloads for machine learning purposes while on this team. That is, the service would accept product identifiers and item attribute keys, collect the requested images and information from various sources, and create a labeling job in AWS SageMaker after which human workers could view the information and answer questions about the product that could be fed into a model as training data.

If you're wondering how these things are related, so am I.

### Complexity
The donation eligibility service was straightforward and not particularly interesting.

The existing package certification system was complex in the sense that nobody remaining on the team really understood what it was supposed to do. Even outside of the engineering team, there didn't seem to be a holistic understanding of what it was supposed to do, not supposed to do, what was deprecated or not, etc.

For the new systems we were building, there was complexity around the company's initiative to migrate systems onto public AWS offerings instead of the internal services and frameworks that had been used before. Other than the need to learn a new way of doing things, it added complexity in that dependencies we wanted to integrate with may be in differing stages of this migration and we needed to decide whether to wait for them to migrate or do a temporary integration with their legacy system.

Building the new packaging certification infrastructure involved the complexity of understanding what the current system was doing and verifying with appropriate stakeholders whether that was correct behavior or not.

The new system was also being designed with a scalable serverless architecture that allowed for a lot of parallelization in the workflow. However, we found that, while our system might be free to parallelize, we were being throttled by downstream dependencies and needed to rate limit ourselves to avoid having our requests rejected.

This additionally required work within the Amazon fulfillment center systems for receiving inventory. We needed to do this work ourselves in a foreign codebase which needed to be understood. It was also a very dangerous and mission-critical part of the code to make changes to, although we were able to do it in such a way that the worst possible impact would be extra boxes around items that didn't need them as opposed to halting the inventory receive process entirely.

### Stack
The existing certification system consisted of an RDS Aurora instance fronted by an HTTP REST service. A website built on a Java framework that I think was itself built on Spring MVC acted as the front-end to this service. The system used its relational database for, among other things, a queue of work to be done which everyone agreed was strange and problematic.

The new system, which had only so far been designed to replace a part of what the old system was responsible for, was built as Lambda functions behind API Gateway with S3 and DynamoDB for storage solutions. It used CloudFormation for infrastructure definition and Kinesis Firehose for streaming data to S3 and Redshift for reporting purposes. Despite being almost entirely public AWS offerings, it did use an established internal system for workflow orchestration that was responsible for calling into a REST service that performed the certification and decertification workflow logic.

Having just learned how to use Lambda and API Gateway, I similarly designed the new labeling job creation service as Lambda functions fronted by API Gateway. S3 was used for a few purposes and SQS was used as a batch processing queue. Because of complications related to the larger AWS migration, it did also need a proxy service running on EC2 in order to integrate with a dependency that had not yet migrated to AWS.

### Role
After joining the team, my initial responsibilities were to help finish the implementation of the donation eligibility service and get it launched and to do the security review for it. I was also tasked with helping a junior engineer write a formal report for an incident that had occurred prior to my joining and with doing promotion evaluation for a couple engineers in the organization.

With regard to the new certification system, I was responsible for the decertification workflow implementation and the work in the fulfillment center inventory receive codebase to support the new, more granularly scoped certifications.

I also did quite a bit of investigation and wrote proposals for how we might backfill the new certification data store with the existing certifications in the legacy system and how we might build a mechanism for auditing the state of the Amazon catalog data against our canonical certification data, but neither of these things were in scope to be implemented during my time on the team.

Although it was not particularly complex, I did design and implement the labeling job service entirely.

### Team
The team consisted of around 8 engineers. As mentioned above, the team was involved in a few different systems that don't seem particularly related and we were often focused on different things despite all sitting together.

In my experience on other teams, the engineering and product teams work closely. On this team, there was more of a line drawn where the product team was not sitting in on our planning meetings or stand-ups and I got the sense that the product team had other things going on unrelated to what we were actively working on. This was probably made worse by the fact that 2 or 3 of the engineers were senior engineers who would meet with stakeholders without the rest of the engineering team, so I always felt I was getting incomplete and second-hand information without the context I would expect.

Still, the team had solid code review, testing, an continuous deployment practices.


## Dash Wand (2014 - 2018)
### Product
The Dash Wand had 2 hardware models and, the way I look at it, 4 iterations on its functionality. The original idea was a sort of alternative to a written shopping list. Customers would keep it in their kitchen and either scan product barcodes when they ran out or speak the name of something they needed into the built-in microphone. It was originally just called the Amazon Dash, but the release of the Dash Button created confusion.

The first model and iteration allowed users to build a "Dash List" entirely distinct from their shopping cart on the AmazonFresh website. We leveraged the NLP services concurrently being built for the Echo device to do voice transcription and acquired a database of product UPC mappings to populate the Dash List with appropriate search terms. Customers could go to their Dash List page and select products to add to cart from in-line search results associated with each voice input or scan.

The 2nd iteration was the concept of "high confidence" inputs. If we were confident that an input was intended to represent a specific product, we would add that product directly to cart and skip the Dash List. However, we also provided an in-line UX for customers to switch the product from the AmazonFresh cart page. In practice, "high confidence" inputs were scans for which the Amazon catalog had a UPC mapping to an available product or voice inputs with search results containing an item previously purchased by the customer.

The 3rd iteration was the migration, along with AmazonFresh in general, to the primary Amazon.com retail website. There was no "Dash List" anymore, but rather the concept of "ambiguous items" co-mingled in the shopping cart view with regular cart items. Ambiguous items could be "disambiguated" by selecting from the in-line search results and disambiguated items could be swapped out with different search results using a similar UX.

At some point during the iterations above, a 2nd hardware model was also released. It was significantly smaller and had a proper speaker and more expressive LEDs.

The 4th and final iteration was the addition of Alexa integration. Instead of being a largely input-only device aside from confirmation beeps, customers could use it to talk to Alexa. It enabled most of the interactions that could be done with the Echo device except for things like music playback which would drain the battery. If the Alexa NLU systems matched an input to one of the Alexa intent handlers, the response would be streamed to the device. If not, the input would be treated as before and result in a cart item.

Device configuration was also a major component of the product from an engineering perspective. Customers would need to use a mobile app to configure the Dash Wand's Wi-Fi connection while also registering the device to their Amazon account. Originally, the only setup method was one in which the user's phone would connect to a temporary Wi-Fi network broadcast by the device after which the app could send the necessary configuration data to the device. This had the inherent issue of the mobile app losing Internet access while connected to the Dash, but even worse was the behavior of some Android phones to automatically disconnect from the Dash after detecting that there was no Internet access. The poor UX resulted in a second setup method using ultrasonic audio. The app would output the configuration data encoded as an ultrasonic audio signal and the Dash would listen for this. Sonic setup was the primary setup method and Wi-Fi setup remained as a fall-back in cases where Sonic setup failed for whatever reason.

### Complexity
Device registration was a major point of complexity and pain. This stemmed from the fact that it was a client-side activity which we didn't have as much insight into combined with the constantly changing world of smartphones at the time, especially on the Android side. We were able to test the full range of relevant iPhones OS versions, but for Android we just covered as much as we could using our current and previous personal phones. To help us in this aspect, I progressively added more detailed client-side logging to the apps and did what I could to ensure that the logs made their way to our server. The apps would send us logs if the user succeeded, failed, or abandoned setup, but would also proactively send us partial logs if the user switched away from the app since we couldn't be sure if they were coming back. If the app crashed, it would send any previously written logs on the next startup.

A major pain point on the development side was the fact that the Dash devices couldn't connect to the internal corporate network which prevented us from using them to test against our development environments. This wasn't the biggest problem early on because the device behavior was simple. We were able to write tests that covered API behavior and generally be confident it would work with the actual device. The problem was much more significant once we started working on Alexa integration because we would benefit much more from ad-hoc testing and experimentation with different Alexa interactions, especially as we were trying to understand how the Alexa systems worked and what kinds of responses we might get from it. We did eventually get one device that had special access to the corporate network, but it had to run modified firmware, was painful to update with new firmware, and the firmware was hard-coded to talk to a particular endpoint which all engineers had to share. It eventually became worthwhile to me to write a "virtual Dash" desktop app which enabled much easier development. We ran it on our laptops, which of course had access to the corporate network, and could use the laptop microphone to provide inputs. The app would play the audio response as well as print the HTTP headers and other useful debug information.

Migrating from AmazonFresh to Amazon.com was a major body of work involving swapping out dependencies, dealing with many new teams who didn't necessarily see it as a priority to support us. Instead of working within the stand-alone AmazonFresh website and mobile apps alongside people we had already worked with in the past, we were now trying to integrate with established Amazon systems that were surely dealing with many other things. While not an engineering complexity, there was definitely complexity involved in negotiating priorities with other teams and getting them aligned with our goals.

From an engineering perspective, the migration to Amazon.com was actually pretty smooth. The microservice architecture we had was a big reason for this. We were able to swap out or add dependencies as needed without more distant parts of the system needing to know about it. The difficulty was more about learning how the Amazon.com cart worked and how to make the necessary changes and integrate our "ambiguous items" with it.

### Stack
We owned a handful of microservices built on an Amazon internal HTTP REST framework. The Gateway service was the public Internet-facing service with the API that the Dash Wand devices talked to which handled authentication. Device registration, product search / high confidence matching, product offer resolution, ambiguous item list access, and voice input playback among other things were handled by distinct services. There was never anything overly complicated with regards to the logic in the services, but just a lot of integration points with other Amazon systems like the shopping cart, Alexa, device identity, customer identity, search, etc.

The microservice architecture was extremely helpful for the migration from AmazonFresh to Amazon.com, and for supporting some of the relationships that were later required but probably not foreseen. For example, ambiguous items eventually became something that might be created by voice shopping interactions with Alexa without involving a Dash device at all.

This project was done prior to Amazon's efforts to build everything directly on top of its own public AWS offerings, so much of the infrastructure was still using internal Amazon services. We used DynamoDB for ambiguous item storage and SQS/SNS for event driven parts of the system, but fleet management, load balancers, log archival, monitoring, reporting / data warehousing, and continuous integration pipelines were all very standardized internal offerings available to us.

### Role
I was recruited by the first engineer on the project, who had also worked with me on Fresh, at essentially the very beginning of the project. Shortly after, a 3rd engineer with more front-end experience joined and that was the original team for most of the pre-Amazon.com migration days.

I was involved in the architectural decisions from the beginning onward, but of course mostly deferred to the opinions of the two more senior engineers unless they specifically wanted a 3rd opinion. I implemented parts of all the services and the front-end web UIs, as did the other two. We just picked up tasks in priority order whenever we finished what we were working on.

On the other hand, given that I had mobile experience, I was really the only engineer of the original 3 working on the mobile app components: the device setup flow and mobile UIs for the Dash List. 

I was similarly siloed for a few months to help with part of the firmware implementation for the 2nd hardware model of the device. The original model had an off-the-shelf barcode module with built-in barcode decoding. The new model required us to implement that ourselves. The firmware team said they could not stay on schedule without more resources and I was the only engineer available with any kind of comfort working in C/C++. We identified a popular open-source C++ barcode library which I rewrote the relevant components from in C. It turned out that the noisy data provided by the simple light sensor on the device would not "just work" with the algorithm in the C++ code, so I had to work out a way to reliably filter out the noise and make sense of the image data. Since I was able to do the initial port to C very quickly, I had enough time to work through that in an experimental and iterative way and the project was able to move forward on schedule.

As the team grew from 3 to 12 engineers, I was able to mentor and guide the incoming engineers as I had complete knowledge of the current state of the project and its history. I was similarly able to help new SDMs get up to speed as we went through 3 of them over the course of the project.

Although our product manager had unusually strong SQL skills and handled much of the reporting, I also wrote SQL for reporting purposes on occasion.

For the migration to Amazon.com, I took the lead in learning how to develop for the Amazon.com retail website environment and digesting that for the rest of the growing team. It was built on a Perl framework that nobody had familiarity with.

There were often times where a puzzling issue or an issue outside the team's domain knowledge would come up and the task of solving it would fall to me with the expectation that I would have the best chance of figuring it out. One instance I remember (vaguely) is that the firmware team claimed that our Gateway endpoint was not behaving properly with regards to its response at the TCP level. As a team, we were really only aware of anything at the level of HTTP and even that was usually abstracted away from us. We weren't responsible for TCP-level behavior and were skeptical that the standard Amazon load balancer we used would behave incorrectly. Still, I was generally aware that I could use tools like tcpdump and Wireshark to inspect this kind of thing, so I worked with a firmware engineer to capture and identify the relevant TCP packets from our response as they appeared on our end. Unfortunately I don't remember the outcome other than we were ultimately able to figure out what was going on.

### Team
As mentioned above, the team grew from 3 to 12 engineers. There were 1 or 2 product managers at a time, an SDM, and sometimes a UX designer.

The environment was energizing, had a well-defined product, clear milestones, and ambitious but achievable deadlines.

Even as the team grew, everyone did some work in all parts of the system with the exception of the mobile apps which remained my responsibility for the most part.

We adopted code review and test coverage requirements enforced as part of the deployment pipeline. The majority of our pipelines were reliably deploying continuously with the exception of the one for the retail Amazon.com website components. The UI tests relied on expected inventory and catalog states which would often change in ways we didn't have control over aside from finding a new alternative product to use for the test instead. We never found a good solution to this problem.


## AmazonFresh (2010 - 2014)
### Product
Fresh lives on within the larger Amazon website but, at this time, AmazonFresh was a standalone website with a largely independent warehouse management system serving only the Seattle, Los Angeles, and San Francisco areas.

### Team
The team was maybe 8-12 engineers with half primarily focused on either the customer-facing website and the others focused on the warehouse management system.

I only recognize this in retrospect, but there was a severe lack of testing and deployment procedures. Code reviews were not required, test coverage was inconsistent, and deployments happened whenever someone had a change they really wanted to get out. These things were starting to change as I transitioned away with the addition of a QA team and change management process for deployments.

### Role
Although my title was Support Engineer, there was little distinction between me and the rest of the software team. I was effectively just an engineer tasked with the things that others would prefer not to do or had a hard time getting prioritized. It was all new and exciting to me anyway.

I was initially focused on improving logging and alarms to make them more meaningful and actionable while also handling the majority of tickets and bug fixes that weren't obviously caused by another engineer's recent changes.

I implemented the first automated UI tests for the site after deciding between the competing options at the time of Selenium or WebDriver.

I did some front-end work for a website redesign.

I did a significant portion of the work to refactor product information retrieval out of the monolithic website code and into a service.

The AmazonFresh mobile apps were initially built by a contracted 3rd party and then largely neglected. Since I was acting as a sort of extra resource on the team, I was given any work related to the apps and therefore became the de facto owner of the mobile apps.

As with the automated UI tests for the website, I was responsible for figuring out how to set up automated testing for the mobile apps and for writing the initial tests.

Again, as the "extra" engineering resource, people on the business team would come to me for questions about the system or to request additions to the tools on the internal warehouse management and data warehouse websites.

Because I had been involved at least a little in all parts of the system, I sort of became the first responder for questions about how things worked.

### Complexity
Aside from everything simply being largely new to me, I remember the most complicated bugs involved delivery slots, inventory promises, order state transitions, order modification chains, and database deadlocks. The bugs often resulted from race conditions, especially after the Automatic Delivery feature was launched.

Automatic Delivery exacerbated existing race condition issues as it would automatically place orders on a customer's behalf, sometimes while the customer was also doing something else. I can't remember specifics, but in general there were many issues involving slots no longer being available unexpectedly, inventory being over-promised, order quantities being unexpectedly changed, and concurrent order modifications breaking the order modification chain (changes to a checked-out order were represented as a child order of the original).

A lot of my work involved collecting logs from different parts of the system relevant to a given incident and poking around in the database to try and put together a timeline of events. Sometimes I would need logs from months ago to figure out what state an order had previously been in prior to something breaking more recently. Over time, I had written tools for myself to make this process easier.

These issues were very systemic and hard to track down given that any part of the website or suite of scheduled tools were potentially writing to any table in the database.

### Stack
Everything centered around a MySQL database. The customer-facing website was built on Java and Apache Struts. It used Hibernate for database access and Solr for product search. The internal warehouse management and data warehouse websites were Ruby on Rails. The website and warehouse management system both had open access to the MySQL database. There were also scheduled jobs that shared a codebase with either the Java or Ruby websites.

Jenkins was used for continuous integration. Everything else worth mentioning was an established internal Amazon service: load balancers, fleet management, package management, deployment, log archival, and monitoring.
