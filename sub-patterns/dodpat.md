Data-Oriented Design Patterns
-----------------------------

Even though the original design patterns were elements of reusable
Object-Oriented Design, there is scope for some pattern language for
development given the Data-Oriented approach. Many of the sections so
far have had an air of design pattern about them as they tend to solve
generic problems with one or more generic solutions. This is where we
gather and explain all the core patterns of development that are seen
when working with a data-oriented code base, but always remember, a
design pattern is a solution looking for a problem, and that alone is
enough reason to be wary. In data-oriented design, we prefer to use
design patterns as they were initially intended, as a way of
communicating between engineers without needing to describe all the
reasoning behind it. These architectural design patterns were a kind of
written down common sense, which means in some sense, the data-oriented
design patterns cannot be like these as common sense is often trumped by
profiling or invention. Regardless, the ability to speak a common tongue
is enough to merit trying to define some of the patterns present.

### A to B transform

A stateless function that takes elements from one container and produces
outputs into another container. All variables are constant over the
lifetime of the transform.

The normal way of working and the best way to guarantee that your output
and input tables don’t clash, is to create a new table and transform
into it. The A to B transform is also the basis of double buffered state
and provides a powerful mechanism for enabling concurrent processing as
you can ensure that A is read only, and B is write only for the whole
time slice. The A to B transform is the transform performed by shaders
and other compute kernels, and the same conditions apply: constants do
not change, local variables only, globals are considered to be
constants, data can be processed in any order and without any
communication to any other element in the transform.

A to B transforms aren’t expensive unless the row counts change, and
even then you can mitigate those more expensive transforms with
conc-trees and other in place transforms that reduce in the case of
filtering transforms. There are two things to consider when transforming
from one table to another:

Is this a transform to create new, or an updated state? Is this
transform going to significantly change the values before they hit the
output table?

The simplest transform is an update. This allows for concurrent state
updates across multiple associated systems without coupling. The
condition table transform is generally used to significantly change the
values, putting them into a new table with a different schema, ready for
decision transforms. Sometimes a transform will do more than one of
these, such as when an update also emits rows into an event table ready
for subscribing entities to react to a state change on the data.

An important requirement of the transform is that it is stateless.
Transforms operate on data, use constants to adjust how they transform
that data, and output in a standardised manner. Some amount of
restriction needs to be set up for the transforms to be worth doing,
however, and one of those restraints is that the transform must be
stateless. The data has state, but the transforms must not. If you look
at how the design pattern works for existing streaming transform engines
such as GPU shader models, you will see that the shader constants are
uniform across all the elements in one render call, this allows for easy
distribution of work across many different workers, even on different
machines. You can have local working variables, but you cannot store out
to some common location as that would introduce some coupling,
potentially making one part of a kernel serial in an otherwise
completely parallel process. Even accumulation over successive elements
would mean that the input to one element depended on the output of
another, which would immediately cause the whole process to become
serial in nature. If you do this, you are going to break the fundamental
parallelisable nature of the transform process, and with it, doom your
code to running only as fast as one of your workers can handle the data.

### In place transform

A stateless function that changes the data in a container based on
constants alone.

There are times when that’s not necessary to create a new table with a
transform. In update calls for many tables, the update can in place
modify rather than run as a double buffered state. The best way to in
place modify can change depending on the layout of the data and what
needs to be done with the data. Always consider how the data gets into
the transform, and how it gets out.

For inputs, make sure you find the optimal way to organise the
pre-fetching so that the transform is never starved of data, for
outputs, make sure that you write as much as you can in tightly packed
consecutive memory to offer opportunity for write combining. The
majority of cases have the same restrictions and benefits as A to B
transform.

If you are doing in place transforms, always remember to write back once
at most for each transform, otherwise aliasing rules can bite, for
example, writing to a local accumulator when the type of the accumulator
is the same as a type being read from, then aliasing may require your
accumulator to be re-read every time it is updated. One way around this
is to mark all your elements as restricted, thus ensuring that the
compiler will assume it’s safe to use the last value without reloading,
but this might be vendor specific so test by looking at the assembly
produced before declaring that the restrict will fix the problems
inherent in accumulators or other load-modify-store values that may be
used in in-place transforms.

Another thing to mention is that for both the in-place transform and the
A to B transform, using a structure’s static member is just as invalid
as a global variable.

### Generative transform

A function that generates data into an output container based on an
algorithm rather than input data.

Sometimes all you need is some constants and only one small piece of
data to generate a whole new table. If you’ve got to build a world from
scratch, you can generate your map with procedural generators, but you
have to seed a procedural generator and the small inputs or constants.
These are what drives these types of transform. You don’t need a large
input set to drive a file loader, and that can be considered a
generative transform. If you put filenames into a *load-me-please*
table, and register a reaction transform into the *file-has-loaded*
event table, then you have a generative function as your streaming
engine. You can write your bootstrap as a generative transform that
introduces elements into multiple tables. If this transform is a script,
then you have the basis for a completely data-driven development. If
instead of a filename you provide a seed and expect to get back a chunk
of terrain, whether by pure procedural generation, or loading, or some
combination, then you have the basis for a distributed processing
landscape system. In the chapter on hierarchical level of detail, the
just-in-time memento that provides some style for a previously
non-existent entity can be considered a generative transform. Taking an
ID and generating a coherent collection of attributes that conforms to
other constraints that might be present such as district, time of day,
difficulty setting, or level of player.

### Sorted Table

A container that keeps itself sorted, tunable for different
circumstances including only sorting a small subset.

A table that is only ever read after sorting can attempt to keep track
of changes rather than sort before use. If the table needs to stay
sorted no matter what, it can generate indexes with which it reorders
the table on transform. There is hardly ever a good reason to explicitly
sort a table, and usually there are better ways to organise data than
sorted. Binary searches don’t work as well in practice as b-trees due to
the cache-friendly operations.

### Multi sorted table

A container that keeps multiple sorted representations of itself
available, tunable for circumstances including sorting different subsets
based on different criteria.

Much like the sorted table, but when a table has multiple queries all
requiring different sorting algorithms, then it’s better to give up and
only use indirection via indexes according to what order each query
requires. This is similar to how databases add indexes for each column
that requests it.

### Gatherer

A method by which large tasks can be split off into multiple parallel
tasks and can then be reduced back into one container for further
processing.

When you run concurrent processes, but you require the output to be
presented in one table, there is a final stage of any transform that
turns all the different outputs into one final output. You can reduce
the amount of work and memory taken up by using the concatenate function
and generate a table that is a conc-tree, or you can use a gather
transform. A gather transform has as many inputs as you have parallel
tasks leading into the final output table, and each input is a queue of
data waiting to enter the final transform. As long as the data is not
meant to be sorted, then the gatherer can run while the concurrent
transforms are running, peeling the transformed rows out of the
processes independent output queues, and dropping them into the final
output table. This allows for completely lockless parallelism of many
tasks that don’t require the data to be in any particular order at the
final stage.

If the gatherer is meant to produce the final table in the same order as
the input table then you will need to pre-parse the data or have the
gatherer use a more complex collating technique. When you pre-parse the
data you can produce a count that can be used to initialise the output
positions making the output table secure for the processing transforms
to write directly into it, but if there is no way to pre-parse the data,
then gatherer might need to co-operate with the task scheduler so that
the processes are biased to return ealier work faster, making final
collation a just in time process for the transfer to the next transform.

### Tasker

When a container is very large, break off pieces and run transforms as
concurrent tasks.

When you have a single large table, you can transform it with one
transform, or many. Using a tasker to fake multiple independent tables
allows for concurrent transforming as each transform can handle their
specific part of the input table without having to consider any of the
other parts in any way.

### Dispatcher

Rather than switch which instructions to run based on data in the
stream, prefer producing new tables that can each be transformed more
precisely.

When operating on data, sometimes the transform is dependent on the
data. Normally any enumerable types or booleans that imply a state that
can change what transform is meant to run are hidden behind existence
based processing tables, but sometimes it’s good to store the bool or
enum explicitly for size sake. When that is the case, it can be
beneficial to pre-process a table and generate a job table, a table with
a row for each transform that is meant to be run on the data.

A dispatcher takes on input table and emits into multiple tables based
on the data. This allows for rapid execution of the tasks without the
overhead of instruction cache misses due to changing what instructions
are going to be run based on the data as all the instructions are
collected into each of the job tables.
