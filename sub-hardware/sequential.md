Sequential data
---------------

When you process your data in a sequence, you have a much higher chance
of cache hit on reading in the data. Making all your calculations run
from sequential data not only helps hardware with caches for reading,
but also when using hardware that does write combining.

In theory, if you’re reading one byte at a time to do something, then
you can almost guarantee that the next byte will already be in memory
the next 127 times you look. For a list of floats, that works out as one
memory load for 32 values. If you have an animation that has less than
32 keys per bone, then you can guarantee that you will only need to load
as many cache-lines as you have bones in order to find all the key
indexes into your arrays of transforms.

In practice, you will find that this only applies if the process you run
doesn’t load in lots of other data to help process your stream. That’s
not to say that trying to organise your data sequentially isn’t
important, but that it’s just as important to ensure that the data being
accessed is being accessed in patterns that allow the processors to
leverage the benefits of that form. There is no point in making data
sequential if all you are going to do is use it so slowly that the cache
fills up between reads.

Sequential data is also easier to split among different processors as
there is little to no chance of cache sharing. When your data is stored
sequentially, rather than randomly, you know where in memory the data
is, and so you can dispatch tasks to work on guaranteed unshared
cache-lines. When multiple CPUs compete to write to a particular
cache-line, they have to storing and loading to keep things consistent.
If the data is randomly placed, such as when you allocate from a memory
pool, or directly from the heap, you cannot be sure what order the data
is in and can’t even guarantee that you’re not asking two different CPUs
to work on the same cache-line of data.

The data-oriented approach, even when you don’t use structs of arrays,
still maintains that sequential data is better than random allocations.
Not only is it good for the hardware, it’s good for simplicity of code
as it generally promotes transforms rather than object-oriented
messaging.

