Locking out anti-patterns
-------------------------

In addition to the design patterns, the elements of reusable
object-oriented software, there are also the anti-patterns, the elements
of miserable software. Sometimes a particularly bad way of doing
something turns up way more often than it should, and when it does, it
begins to get a name for itself. data-oriented development helps reduce
these by both not being as complex to begin with because the problem
domain is not dragged into a new language of objects, nor does it have
objects themelves, which can cause multiple problems due to their
sometimes coarse and sometimes too fine nature.

### Abstraction Inversion

Abstraction inversion is when some internal functions of a class are
kept hidden, but they are useful, so an external developer has to
reinvent those internal functions as external functions by using only
the public interface, which itself will probably be using the internal
functions these new external functions are trying to replicate. Do this
enough times with even the simplest of classes and you can explode the
amount of work required to do a simple job.

As there is no inherent data or function hiding during data-oriented
development, there can be no barrier to using the functions or the
transforms that you want to use.

### Acme Pattern / God Class

One giant class that runs the show. One very large data clump that is
almost certainly a mess when it comes to organising the data by when it
is accessed. Because there are no objects and we normalise our data,
this anti-patterns becomes relatively difficult to experience. There is
still the chance that someone might try to implement a nosql version of
data-oriented development, but even if they do, most of the problems go
away under struct of arrays. When it comes to the problem of all the
methods in one class, then we know we’re fine as there are no such
boundaries.

### CObject / Cosmic Hierarchy

Almost the pure opposite of the God Class, the CObject does nothing, and
is inherited whether directly or indirectly by everything. Many game
engines have a concept of an entity or an object, but they generally
don’t keep it pure out of good practice. The threat of starting a cosmic
hierarchy has reduced the chance of people making another CObject. The
idea that everything comes from a base object class tends to encourage
hard to read code. Code that divines the type of object before use
suffers from overly long preamble in functions, and suffers from runtime
type checking overhead. It’s common knowledge that the preamble code -
such things as “if type == foo” or checks for NULL - or the runtime type
checking aren’t overly expensive. This common knowledge has long
outlived its lifespan though, and is provably a lie.

At the root of a lot of object-oriented entity systems lies a core class
to which everything can be cast. This usually leads to lots of
problematic code that costs cycles and can cause bugs by not correctly
identifying itself.

In data-oriented development there is no Cosmic base class, even
entities in an entity system only refer to entities. Each component will
have a manager, and the idea of any component sharing some common core
with another component goes so far away from the point of separating an
entity into components that you should be hard pressed to find something
that commits this anti-pattern.

### Hidden Requirements

Sometimes a basic design change is required by a long standing
requirement accidentally omitted from the original and all subsequent
design documents. In object-oriented development, making a refactor at a
late stage is very costly as object contracts can be hard to adjust
without causing a very large amount of related changes to all the code
that touches the changed class.

Luckily, in data-oriented development, changing everything does not get
much harder the longer the project continues because there are
documented tools and techniques for making large scale schema changes in
database technologies, and table based development can reap benefits
there by literally implementing the same migrational tool-chain that is
used in those circumstances.

### Stovepipe

The more that bugs are fixed and corner cases are added, the harder it
can be to refactor an existing Object-oriented codebase. This is not as
true in data-oriented as towards the end of a project the difficultly in
refactoring the design should be mitigated by the understanding and
transparency of the whole program.

