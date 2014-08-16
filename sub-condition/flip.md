Flip it on its head
-------------------

The decision table approach is another form of taking what is normally a
singular entity approach and flipping it on its head. Now we are aware
of the idea of a structure of arrays, we can start to see other areas of
code that previously were being driven by a multiple individual entities
entering into update functions and calling things based on their own
data, and causing the processor to change direction and try to keep up
with the winding trail set by all the selfish entities. If every entity
needs to do an update, then effectively no individual entity needs to do
an update. Components need to update, and if instead of running an
update over each and every entity in your application, you run a
component update over every component manager, then you’re moving from a
data driven mess to a stream processing or flow based programming
paradigm. Each of these approaches has benefits, but the difficulty in
using them in the past has been how to begin to do it when starting with
an object oriented data layout. If your data is already organised as
structures of arrays (or indeed component managers of arrays of
transform related data), then the flow based techniques for transforming
data don’t need to be shoe-horned in.

Because we have moved the decisions out of the instances, we are in a
position to do more at the same time. A wary object-oriented programmer
might assume that each decision table applies to only one set of
entities, or one set of queries, but the truth is far more parallel.
Once you have moved away from entities being a type, and instead let
them be implicit on their components, you find that you can process a
very large number of apparently disparate entities at the same time. As
you build your application’s update function, you find that you need to
make decisions for components, update components based on those
decisions, and sometimes iterate over that sequence a few times. At no
point are you limited to one entity at a time, or even one component at
a time unless you build in dependencies into your transform chain.

Moving away from single entity processing is also good if you want to
offload your core application code onto a compute shader. As long as you
maintain your data in simple arrays inside the components, then there
will likely be very little currying of data into a shader ready format.
If you make sure your processing is stateless, as in it does not
accumulate or modify global state, or reference other elements in the
stream in a random access fashion, then it’s very likely you will be
able to convert your code to a compute kernel. At this point, you will
have left the general purpose CPU to scheduling the operations, and
joining tables. These are the only jobs still not easily handled by a
stateless streaming approach.

