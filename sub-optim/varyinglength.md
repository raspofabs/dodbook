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

