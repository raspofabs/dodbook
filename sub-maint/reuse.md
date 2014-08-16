Reusability
-----------

A feature commonly cited by the object-oriented developers that seems to
be missing from data-oriented development is reusability. The idea that
you won’t be able to take already written libraries of code and use them
again, or on multiple projects, because the design is partially within
the implementation. To be sure, once you start optimising your code to
the particular features of a software project, you do end up with
unreusable code. While developing data-oriented projects, the assumed
inability to reuse source code would be significant, but it is also
highly unlikely. The truth is found when considering the true meaning of
reusability.

Reusability is not fundamentally concerned in reusing source files or
libraries. Reusability is the ability to maintain an investment in
information. A wealth of knowledge for the entity that owns the
development IP.

Copyright law has made it hard to see what resources have value in
reuse, as it maintains the source as the object of it’s discussion
rather than the intellectual property represented by the source. The
reason for this is that ideas cannot be copyrighted, so by maintaining
this stance, the copyrighter keeps hold of this tenuous link to a right
to withhold information. Reusability comes from being aware of the
information contained within the medium it is stored. In our case, it is
normally stored as source code, but the information is not the source
code. With Object-Oriented development, the source can be adapted
(adapter pattern) to any project we wish to venture. However, the source
is not the information. The information is the order and existence of
tasks that can and will be performed on the data. Viewing the
information this way leads to an understanding that any reusability that
a programming technique can provide comes down to it’s mutability of
inputs and outputs. It’s willingness to adapt a set of temporally
coupled tasks into a new usage framework is how you can find out how
well it functions reusably.

In object-oriented development, you apply the information inherent in
the code by adapting a class that does the job, or wrapper it, or use an
agent. In data-oriented development, you copy the functions and schema
and transform into and out of the input and output data structures
around the time you apply the information contained in the data-oriented
transform.

Even though, at first sight, data-oriented code doesn’t appear as
resuable on the outside, the fact is that it maintains the same amount
of information in a simpler form, so it’s more reusable as it doesn’t
carry the baggage of related data or functions like object-oriented
programming, and doesn’t require complex transforms to generate the
input and extract from the output like procedural progamming tends to
generate due to the normalising.

Duck typing, not normally available in object-oriented programming due
to a stricter set of rules on how to interface between data, can be
implemented with templates to great effect, turning code that might not
be obviously reusable into a simple strategy, or a sequence of
transforms that can be applied to data or structures of any type, as
long as they maintain a naming convention.

The object-oriented C++ idea of reusability is a mixture of information
and architecture. Developing from a data-oriented transform centric
viewpoint, architecture just seems like a lot of fluff code. The only
good architecture that’s worth saving is the actualisation of data-flow
and transform. There are situations where an object-oriented module can
be used again, but they are few and far between because of the inherent
difficulty interfacing object-oriented projects with each other.

The most reusable object-oriented code appears as interfaces to agents
into a much more complex system. The best example of an object-oriented
approach that made everything easier to handle, was highly reusable, and
was fully encapsulated was the `FILE` type from `stdio.h` that is used
as an agent into whatever the platform and OS would need to open,
access, write, and read to and from a file on the system.

