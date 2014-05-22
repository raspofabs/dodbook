Optimisations and Implementations
=================================

When optimising software, you have to know what is causing the software
to run slower than you need it to run. We find in most cases, data
movement is what really costs us the most. In the GPU, we find it
labelled under fill rate, and when on CPU, we call it cache-misses. Data
movement is where most of the energy goes when processing data, not in
calculating solutions to functions, or from running an algorithm on the
data, but actually the fulfillment of the request for the data in the
first place. As this is most definitely true about our current
architectures, we find that implicit or calculable information is much
more useful than cached values or explicit state data.

If we start our game development by organising our data in normalised
tables, we have many opportunities for optimisation. Starting with such
a problem agnostic layout, we can pick and choose from tools we’ve
created for other tasks, at worst elevating the solution to a template
or a strategy, before applying it to both the old and new use cases.

Tables
------

To keep things simple, advice from multiple sources indicates that
keeping your data as vectors has a lot of positive benefits. There are
reasons to not use STL, including extended compile and link times, as
well as issues with memory allocations. Whether you use std::vector, or
roll your own dynamicly sized array, it is a good starting place for any
future optimisations. Most of the processing you will do will be
transforming one array into another, or modifying a table in place. In
both these cases, a simple array will suffice for most tasks.

For the benefit of your cache, structs of arrays can be more cache
friendly if the data is not related. It’s important to remember that
this is only true when the data is not meant to be accessed all at once,
as one advocate of the data-oriented design movement assumed that
structures of arrays were intrinsically cache friendly, then put the
x,y, and z coordinates in separate arrays of floats. The reason that
this is not cache friendly should be relatively easy to spot. If you
need to access the x,y, or z of an element in an array, then you more
than likely need to access the other two axes as well. This means that
for every element he would have been loading three cache-lines of float
data, not one. This is why it is important to think about where the data
is coming from, how it is related, and how it will be used.
Data-oriented design is not just a set of simple rules to convert from
one style to another.

If you use dynamic arrays, and you need to delete elements from them,
and these tables refer to each other through some IDs, then you may need
a way to splice the tables together in order to process them. If the
tables are sorted by the same value, then it can be written out as a
simple merge operation, such as in Listing [lst:joinmerge].

    Table<Type1> t1Table;
    Table<Type2> t2Table;
    Table<Type3> t3Table;

    ProcessJoin( Func functionToCall ) {
        TableIterator A = t1Table.begin();
        TableIterator B = t2Table.begin();
        TableIterator C = t3Table.begin();
        while( !A.finished && !B.finished && !C.finished ) {
            if( A == B && B == C ) {
                functionToCall( A, B, C );
                ++A; ++B; ++C;
            } else {
                if( A < B || A < C ) ++A;
                if( B < A || B < C ) ++B;
                if( C < A || C < B ) ++C;
            }
        }
    }

This works as long as the == operator knows about the table types and
can find the specific column to check against, and as long as the tables
are sorted based on this same column. But what about the case where the
tables are zipped together without being the sorted by the same columns?
For example, if you have a lot of entities that refer to a modelID, and
you have a lot of mesh-texture combinations that refer to the same
modelID, then you will likely need to zip together the matching rows for
the orientation of the entity, the modelID in the entity render data,
and the mesh and texture combinations in the models. The simplest way to
program a solution to this is to loop through each table in turn looking
for matches such as in Listing [lst:joinloop].

    Table<Orientation> oTable;
    Table<EntityRenderable> erTable;
    Table<MeshAndTexture> modelAssets;

    ProcessJoin( Func functionToCall ) {
        TableIterator A = oTable.begin();
        while( !A.finished() ) {
            TableIterator B = erTable.begin();
            while( !B.finished() ) {
                TableIterator C = modelAssets.begin();
                while( !C.finished() ) {
                    if( A == B && B == C ) {
                        functionToCall( A, B, C );
                    }
                 ++C;
                }
            ++B;
            }
        ++A;
        }
    }

Another thing you have to learn about when working with data that is
joined on different columns is the use of join strategies. In databases,
a join strategy is used to reduce the total number of operations when
querying across multiple tables. When joining tables on a column (or key
made up of multiple columns), you have a number of choices about how you
approach the problem. In our trivial coded attempt you can see we simply
iterate over the whole table for each table involved in the join, which
ends up being O($nmo$) or O($n^3$) for rougly same size tables. This is
no good for large tables, but for small ones it’s fine. You have to know
your data to decide whether your tables are big[^1] or not. If your
tables are too big to use such a trivial join, then you will need an
alternative strategy.

You can join by iteration, or you can join by lookup[^2], or you can
even join once and keep a join cache around.

The first thing could do is use the ability to have tables sorted in
multiple ways at the same time. Though this seems impossible, it’s
perfectly feasible to add auxilary data that will allow for traversal of
a table in a different order. We do this the same way databases allow
for any number of indexes into a table. Each index is created and kept
up to date as the table is modified. In our case, we implement each
index the way we need to. Maybe some tables are written to in bursts,
and an insertion sort would be slow, it might be better to sort on first
read. In other cases, the sorting might be better done on write, as the
writes are infrequent, or always interleaved with reads.

Concatenation trees provide a quick way to traverse a list. Conc-trees
usually are only minimally slower than a linear array due to the nature
of the structure. A conc-tree is a high level structure that points to a
low level structure, and many elements can pass through a process before
the next leaf needs to be loaded. The code for a conc-tree doesn’t
remain in memory all the time like other list handling code, as the list
offloads to an array iteration whenever it is able. This alone means
that sparse conc-trees end up spending little time in their own code,
and offer the benefit of not having to rebuild when an element goes
missing from the middle of the array.

In addition to using concatenation trees to provide a standard iterator
for a constantly modified data store, it can also be used as a way of
storing multiple views into data. For example, perhaps there is a set of
tables that are all the same data, and they all need to be processed,
but they are stored as different tables for some reason, such as what
team they are on. Using the same conc-tree code, they can be iterated as
a full collection with any code that accepts a conc-tree instead of an
array iterator.

Modifying a class can be difficult, especially at runtime when you can’t
affect the offsets in running code without at least stopping the process
and updating the executable. Adding new elements to a class can be very
useful, and in languages that allow it, such as Ruby and Python, and
even Javascript, it can be used as a substitute for virtual functions
and compositing. In other languages we can add new functions, new data,
and use them at runtime. In C++, we cannot change existing classes,
unless they are defined by some other mechanism than the compile time
structure syntax. We can add elements if we define a class by its
schema, a data driven representation of the elements in the class. The
benefit of this is that schema can include more, or less, than normal
given a new context. For example, in the case of some merging where the
merging happens on two different axes, there could be two different
schema representing the same class. The indexes would be different. One
schema could include both indexes, with which it would build up an
combination table that included the first two tables merged, by the
first index, but maintaining the same ordering so that when merging the
merged table with the third table to be merged, the second index can be
used to maintain efficient combination.

    A, B, C
    B has index(AB), and index(BC)
    merge A,B (by index(AB))
    AB, C
    merge AB, C (by index(BC))
    ABC

Transforms
----------

Taking the concept of schemas another step, a static schema definition
can allow for a different approach to iterators. Instead of iterating
over a container, giving access to an element, a schema iterator can
become an accessor for a set of tables, meaning the merging work can be
done during iteration, generating a context upon which the transform
operates. This would benefit large, complex merges that do little with
the data, as there would be less memory usage creating temporary tables.
It would not benefit complex transforms as it would reduce the
likelihood that the next set of data is in memory ready for the next
cycle.

For large jobs, a smarter iterator will help in task stealing, the
concept of taking work away from a process that is already running in
order to finish the job faster. A scheduler, or job management system,
built for such situations, would monitor how tasks were progressing and
split remaining work amongst any idle processors. Sometimes this will
happen because other processes took less time to finish than expected,
sometimes because a single task just takes longer than expected.
Whatever the reason, a transform based design makes task stealing much
simpler than the standard sequential model, and provides a mechanism by
which many tasks can be made significantly more parallel.

Another aspect of transforms is the separation of what from how, the
separation of the loading of data to transform from the code that
performs the operations on the data. In some languages, introducing map
and reduce is part of the basic syllabus, in c++, not so much. This is
probably because lists aren’t part of the base language, and without
that, it’s hard to introduce powerful tools that require an
understanding of them. These tools, map and reduce, can be the basis of
a purely transform and flow driven program. Turning a large set of data
into a single result sounds eminently serial, however, as long as one of
the steps, the reduce step, is either associative, or commutative, then
you can reduce in parallel for a significant portion of the reduction.

A simple reduce, one made to create a final total from a mapping that
produces values of zero or one for all matching elements, can be
processed as a less and less parallel tree of reductions. In the first
step, all reductions produce the total of all odd-even pairs of
elements, and produce a new list that goes through the same process.
This list reduction continues until there is only one item left
remaining. Of course this particular reduction is of very little use, as
each reduction is so trivial, you’d be better off assigning an Nth of
the workload to each of the N cores and doing one final summing. A more
complex, but equally useful reduction would be the concatenation of a
chain of matrices. Matrices are associative even if they are not
commutative, and as such, the chain can be reduced in parallel the same
way building the total worked. By maintaining the order during reduction
you can apply parallel processing to many things that would normally
seem serial as long as they are associative in the reduce step. Not only
matrix concatenation, but also products of floating point values such as
colour modulation by multiple causes such as light, diffuse, or gameplay
related tinting. Building text strings can be associative, as can be
building lists and of course conc-trees themselves.

Spatial sets for collisions
---------------------------

In collision detection, there is often a broad-phase step which can
massively reduce the number of potential collisions we check against.
When ray casting, it’s often useful to find the potential intersection
via an octree, bsp, or other single query accelerator. When running path
finding, sometimes it’s useful to look up local nodes to help choose a
starting node for your journey.

All spatial data-stores accelerate queries by letting them do less. They
are based on some spatial criteria and return a reduced set that is
shorter and thus less expensive to transform into new data.

Existing libraries that support spatial partitioning have to try to work
with arbitrary structures, but because all our data is already organised
by table, writing adaptors for any possible table layout is simple.
Writing generic algorithms becomes very easy without any of the side
effects normally associated with writing code that is used in multiple
places. Using the table based approach, because of its intention
agnosticism (that is, the spatial system has no idea it’s being used on
data that doesn’t technically belong in space), we can use spatial
partitioning algorithms in unexpected places, such as assigning audio
channels by not only their distance from the listener, but also their
volume and importance. Making a 5 dimensional spatial partitioning
system, or an N dimensional one, would only have to be written once,
have unit tests written once, before it could be used and trusted to do
some very strange things. Spatially partitioning by the quest progress
for tasks to do seems a little overkill, but getting the set of all
nearby interesting entities by their location, threat, and reward, seems
like something an AI might consider useful.

Lazy Evaluation for the masses
------------------------------

When optimising Objectoriented code, it’s quite common to find local
caches of calculations done hidden in mutable member variables. One
trick found in most updating hierarchies is the dirty bit, the flag that
says whether the child or parent members of a tree imply that this
object needs updating. When traversing the hierarchy, this dirty bit
causes branching based on data that has only just loaded, usually
meaning there is no chance to guess the outcome and thus in most cases,
causes a pipeline flush and an instruction lookup.

If your calculation is expensive, then you might not want to go the
route that renderer engines now use. In render engines, it’s cheaper to
do every scene matrix concatenation every frame than it is only doing
the ones necessary and figuring out if they are.

For example, in the /emph<span>GCAP 2009 - Pitfalls of Object Oriented
Programming presentation by Tony Albrecht</span> in the early slides he
declares that checking a dirty flag is less useful than not checking it
as if it does fail (the case where the object is not dirty) the
calculation that would have taken 12 cycles is dwarfed by the cost of a
branch misprediction (23-24 cycles).

If your calculation is expensive, you don’t want to bog down the game
with a large number of checks to see if the value needs updating. This
is the point at which existence-based-processing comes into its own
again as existence the dirty table implies that it needs updating, and
as a dirty element is updated it can be pushing new dirty elements onto
the end of the table, even prefetching if it can improve bandwidth.

Not getting what you didn’t ask for
-----------------------------------

When you normalise your data you reduce the chance of another
multifaceted problem of object-oriented development. C++’s
implementation of objects forces unrelated data to share cache-lines.

Objects collect their data by the class, but many objects, by design,
contain more than one role’s worth of data. This is partially because
object-oriented development doesn’t naturally allow for objects to be
recomposed based on their role in a transaction, and partially because
C++ needed to provide a method by which you could have object-oriented
programming while keeping the system level memory allocations
overloadable in a simple way. Most classes contain more than just the
bare minimum, partially because of inheritance, and partially because of
the many contexts in which an object can play a part. Unless you have
very carefully laid out a class, many operations that require only a
small amount of information from the class, will load a lot of
unnecessary data into the cache in order to do so. Only using a very
small amount of the loaded data is one of the most common sins of the
object-oriented programmer.

Every virtual call loads in the cache-line that contains the
virtual-table pointer of the instance. If the function doesn’t use any
of the class’s early data, then that will be cacheline usage in the
region of only 4%. That’s a memory throughput waste, and cannot be
recovered without rethinking how you dispatch your functions. After the
function has loaded, the program has to load the data it wants to work
on, which can be scattered across the memory allocated for the class
too. Sometimes you might organise the data so that the function is
accessing contiguous blocks of useful information, but someone going in
and adding new data at the top of the class can shift all the data that
was previously on one cache-line, into a position where it is split over
two, or worse, make the whole class unaligned causing virtually random
timing properties on every call. This could be even worse if what they
have added is a precondition that loads data from an unrelated area of
memory, in which case it would require that the load finished before it
even got to the pipeline flush if it failed the branch into loading the
function body and the definitely necessary transformable data.

A general approach with the table formatted data is to preparse the
table to produce a job list. There would be one job list per transform
type identified by the data if it was to emulate a virtual call. Then,
once built, transform using these new job tables to drive the process.
For each transform type , run the transform over all the jobs in the job
queue built for this transform. This is much faster as the function used
to transform the data is no longer coming from a virtual lookup, but
instead is implied by which table is being processed, meaning no
instruction cache misses after the first call to the transform function,
and not loading the transform if there are zero entries.

Another benefit is that the required data can be reorganised now that
it’s obvious what data is necessary. This leads to simple to optimise
data structures compared to an opaque class that to some extent,
pretends that the underlying memory configuration is unimportant and
encapsulated. This can help with pre-fetching and write combining to
give near optimal performance without any low level coding.

Varying Length Sets
-------------------

Throughout the techniques so far, there’s been an implied table
structure to the data. Each row being a struct, or each table being a
row of columns of data, depending on the need of the transforms. When we
normally do stream processing, for example, with shaders, we normally
use fixed size buffers. Most work done with stream processing has this
same limitation, we tend to have a fixed number of elements for both
sides. However, we saw that conc-trees solve the problem of mapping from
one size input to another size output, and that it works by
concatenating the output data into a cache-oblivious structure. This
structure is very general purpose and could be a basis for preliminary
work with map-reduce programming for your game, but there are cases
where much better structures exist.

For filtering, that is where the input is known to be superset of the
output, then there can be a strong case for an annealing structure. Like
the conc-trees, each transform thread has its own output, but instead of
concatenating, the reduce step would first generate a total and a start
position for each reduce entry and then process the list of reduces onto
the final contiguous memory.

If the filtering was a stage in a radix sort or something that uses a
similar histogram for generating offsets, then a parallel prefix sum
would reduce the time to generate the offsets. A prefix sum is the
running total of a list of values. The radix sort output histogram is a
great example because the bucket counts indicate the starting points
through the sum of all histogram buckets that come prior.
$o_n = \sum_{i=0}^{n-1} b_i$. This is easy to generate in serial form,
but in parallel we have to consider the minimum required operations to
produce the final result. In this case we can remember that the longest
chain will be the value of the last offset, which is a sum of all the
elements. This is normally optimised by summing in a binary tree
fashion. Dividing and conquering: first summing all odd numbered slots
with all even numbered slots, then doing the same, but for only the
outputs of the previous stage.

$$\xymatrix{
    A \ar[d] \ar[dr] & B \ar[d] & C \ar[d] \ar[dr] & D \ar[d] \\
    a \ar[d] & ab \ar[d] \ar[drr] & c \ar[d] & cd \ar[d] \\
    a & ab & abc & abcd }$$

Then once you have the last element, backfill all the other elements you
didn’t finish on your way to making the last element. When you come to
write this in code, you will find that these back filled values can be
done in parallel while making the longest chain. They have no dependency
on the final value so can be given over to another process, or managed
by some clever use of SIMD.

$$\xymatrix{
    a \ar[d] & ab \ar[d] \ar[dr] & c \ar[d] & abcd \ar[d] \\
    a & ab & abc & abcd }$$

Also, for cases where the entity count can rise and fall, you need a way
of adding and deleting without causing any hiccups. For this, if you
intend to transform your data in place, you need to handle the case
where one thread can be reading and using the data that you’re deleting.
To do this in a system where objects’ existence was based on their
memory being allocated, it would be very hard to delete objects that
were being referenced by other transforms. You could use smart pointers,
but in a multi-threaded environment, smart pointers cost a mutex to be
thread safe for every reference and dereference. This is a high cost to
pay, so how do we avoid it?

Don’t ever delete.

Deletion is for wimps. If you are deleting in a system that is
constantly changing, then you would normally use pools anyway. By
explicitly not deleting, but doing something else instead, you change
the way all code accesses data. You change what the data represents. If
you need an entity to exist, such as a CarDriverAI, then it can stack up
on your table of CarDriverAIs while it’s in use, but the moment it’s not
in use, it won’t get deleted, but instead marked as not used. This is
not the same as deleting, because you’re saying that the entity is still
valid, won’t crash your transform, but can be skipped as if it were not
there until you get around to overwriting it with the latest request for
a CarDriverAI. Keeping dead entities around is as cheap as keeping pools
for your components.

Bit twiddling decision tables
-----------------------------

Condition tables normally operate as arrays of condition flag bit
fields. The flags are the collected results of conditions on the data.
But, if the bit fields are organised by decision rather than by row,
then you can call in only the necessary conditions into different
decision transforms.

If the bits are organised by condition, then you can run a short
transform on the whole collection of condition bits to create a new,
simpler list of whether or nots. For example, you may have conditions
for decisions that you can map to an alphabet of a-m, but only need some
for making a decision. Imagine you need to be sure that a,d,f,g are all
false, but e,j,k need to all be true. Given this logic, you can build a
new condition, let’s say q, that equals $( a \wedge
d \wedge f \wedge g ) \wedge \neg( e \vee j \vee k )$ which can then be
used immediately as a job list.

Organising the bits this way could be easier to parallelize as a
transform that produces a condition stream would be in contention with
other processes if they shared memory[^3]. The benefit to row based
conditions comes when the conditions change infrequently, and the number
of things looking at the conditions to make decisions is small enough
that they all fit in a single platform specific type, such as a 32bit or
64bit unsigned int. In that case, there would be no benefit in reducing
the original contention when generating the condition bits, and because
the number of views, or contexts about the conditions is low, then there
is little to no benefit from splitting the processing so much.

If you have an entity that needs to reload when their ammo drops to
zero, and they need to consider reloading their weapon if there is a
lull in the action, then, even though both those conditions are based on
ammo, the decision transforms are not based on the same condition. If
the condition table has been generated as arrays of condition bitfields
with each bit representing one row’s state with respect to that
condition, then you can halve the bandwidth to the check for
definite-reload transform, and halve the bandwidth for the
reload-consideration check. There will be one stream of bits for the
condition of ammo equal to zero, and another stream for ammo less than
max. There’s no reason to read both, so we don’t.

What we have here is another case of deciding whether to go with
structures of arrays, or sticking with an array of structures. If we
access the data from a few different contexts, then a structure of
arrays trumps it. If we only have one context for using the conditions,
then the array of structures, or in this case, array of masks, wins out.
But remember to profile as any advice is only advice and only measuring
can really provide proof, or evidence that assumptions are wrong.

Joins as intersections
----------------------

Sometimes, normalisation can mean you need to join tables together to
create the right situation for a query. Unlike RDBMS queries, we can
organise our queries much more carefully and use the algorithm from
merge sort to help us zip together two tables. As an alternative, we
don’t have to output to a table, it could be a pass through transform
that takes more than one table and generates a new stream into another
transform. For example, per entityRenderable, join with entityPosition
by entityID, to transform with AddRenderCall( Renderable, Position )

Data driven techniques
----------------------

Apart from finite state machines there are some other common forms of
data driven coding practices, some of which are not very obvious, such
as callbacks, and some of which are very much so, such as scripting. In
both these cases, data causing the flow of code to change will cause the
same kind of cache and pipe-line problems as seen in virtual calls and
finite state machines.

Callbacks can be made safer by using triggers from event subscription
tables. Rather than have a callback that fires off when a job is done,
have an event table for done jobs so that callbacks can be called once
the whole run is finished. For example, if a scoring system has a
callback from “badGuyDies”, then in an Object-oriented message watcher
you would have the scorer increment its internal score whenever it
received the message that a badGuyDies. Instead run each of the
callbacks in the callback table once the whole set of badguys has been
checked for death. If you do that, and execute every time all the
badGuys have had their tick, then you can add points once for all
badGuys killed. That means one read for the internal state, and one
write. Much better than multiple reads and writes accumulating a final
score.

For scripting, if you have scripts that run over multiple entities,
consider how the graphics kernels operate with branches, sometimes using
predication and doing both sides of a branch before selecting a
solution. This would allow you to reduce the number of branches caused
merely by interpreting the script on demand. If you go one step further
an actually build SIMD into the scripting core, then you might find that
you can run script for a very large number of entities compared to
traditional per entity serial scripting. If your SIMD operations operate
over the whole collection of entities, then you will pay almost no price
for script interpretation[^4].

[^1]: dependent on the target hardware, how many rows and columns, and
    whether you want the process to run without trashing too much cache

[^2]: often a lookup join is called a join by hash, but as we know our
    data, we can use better row search algorithms than a hash when they
    are available

[^3]: This would be from false sharing, or even real sharing in the case
    of different bits in the same byte

[^4]: Take a look at the section headed *The Massively Vectorized
    Virtual Machine* on the bitsquid blog
    http://bitsquid.blogspot.co.uk/2012/10/a-data-oriented-data-driven-system-for.html
