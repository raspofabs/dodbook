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

