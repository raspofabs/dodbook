Counting to find out facts
--------------------------

Counting isn’t just about compression, sometimes it’s about speed. Given
an algorithm, sometimes the best way to make it faster is to find out
what data it’s being given in the first place and find out if it comes
in regular patterns, or is large enough or small enough to change the
algorithm. In data-oriented design, it’s always pertinent to perform
some analysis of the real world performance of your code, and sometimes
what you count can be very important.

If a function being called by iterating over a large set of data and
being called on every element in the list, then the function can be
timed in various ways. You can time how long it takes to do the whole
set of updates, then divide by the number of updates, or you can try to
profile the function per call. You’re probably going to get reasonably
accurate timings either way, but what if the function was only going to
be called if some value in the element was set? What if the function is
normally fast but has spikes?

In the case of spikes, this is where per call timings are essential.
Counting the nanoseconds for operations (and storing the arguments going
into them) is a great way to do analysis of why your function has
unexpected performance.

In some cases, checking whether or not to do work just before doing it
can bring about significant performance issues. If the function to run
is not known at compile time, then there is a higher chance that this
pattern exhibits bad performance. Take the dirty flag as an example. If
an entity has a function that can be made dirty and only needs to be
updated when that flag is dirty, then it makes sense to check that flag
before committing to doing any work, but sometimes you can’t stop the
compiler from assuming the probability of that is high enough to begin
doing the work before you’re sure it’s necessary.

This code runs quickly and efficiently while the dirty flag is true, but
the moment the flag is false, depending on the target platform, this can
lead to the pipeline being flushed, and the cache being dirtied by code
that is ultimately not required to even be run.

This code, on most platforms, will run faster, even though it’s
apparently doing more work. The difference is that this code runs
through all the necessary elements only loading the data necessary to
perform the check to see if work is required to be done. Once the work
list is finished, then a definite call to do work can be made on each
item in the list. In the worst case, all the items in the container
require work, and the work list is full, and depending on your target,
this might be slower than the original iteration, but if there will be a
number of dirty items at which the two pass process is faster, and only
actually counting and profiling will find that value out. You cannot
rely on a compiler to reorganise your calls this way.

Some work has been done in virtual machines to do optimisations like
this, which leads to really good performance in spite of badly laid out
code, but the performance comes at a price, namely the fact that during
runtime, the virtual machine is having to look for optimisations to
make.

