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

