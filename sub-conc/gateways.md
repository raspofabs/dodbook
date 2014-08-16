Queues as gateways, and “Now”
-----------------------------

When you don’t know how many items you are going to get out of a
transform, such as when you filter a table to find only the X that are
Y, you need run a reduce on the output to make the table non-sparse.
Doing this can be log(N) latent, that is pairing up rows takes serial
time based on log(N). But, if you are generating more data than your
input data, then you need to handle it very differently. Mapping a table
out onto a larger set can be managed by generating into gateways, which
once the whole map operation is over, can provide input to the reduce
stage. The gateways are queues that are only ever written to by the
Mapping functions, and only ever read by the gathering tasks such as
Reduce. there is always one gateway per Map runtime. That way, there can
be no sharing across threads. A Map can write that it has put up more
data, and can set the content of that data, but it cannot delete it or
mark any written data as having been read. The gateway manages a read
head, that can be compared with the write head to find out if there is
any waiting elements. Given this, a gathering gateway or reduce gateway
can be made by cycling through all known gateways and popping any data
from the gateway read heads. This is a fully concurrent technique and
would be just as at home in variable CPU timing solutions as it is in
standard programming practices as it implies a consistent state through
ownership of their respective parts. A write will stall until the read
has allowed space in the queue. A read will either return “no data” or
stall until the write head shows that there is something more to read.

When it comes to combining all the data into a final output, sometimes
it’s not worth recombining it into a different shape, in which case we
can use conc-trees, a technique that allows for concurrency and
cache-friendly transforming while maintaining most of the efficiency of
contiguous arrays. Conc-trees are a tree representation of data that
almost singlehandedly allows for cache oblivious efficient storage of
arbitrary lists of data. Cache oblivious algorithms don’t need to know
the size of the cache in order to fully utilise them and normally
consist of some kind of divide and conquer core algorithm, and
conc-trees do this by either representing the null set, a concatenation,
or some data. If we use conc trees with output from transforms, we can
optimise the data that is being concatenated so it fits well in cache
lines, and we can also do the same with conc tree concatenate nodes,
making them concatenate more than just two nodes, thus saving space and
memory access. We can tune these structures per platform or by data
type.

Concurrency is acheived between writer and readers by preparing a new
tree from the remnants of the old tree before pushing the root node
back. Normally, operations involve adding or subtracting elements from a
list: simply recreating the small array that contains the change, then
recreating all the nodes all the way back to the root. This allows for a
new tree to exist alongside the old tree. Maintaining reference counts
for reading will allow for perfect timed destruction of the old nodes,
but you may find there will be a time when you know there won’t be any
remaining readers, leading to a simpler garbage collection. Multiple
writers will still block, but readers can operate off old data while a
writer is recreating.

Given that we have a friendly structure for storing data, and that these
can be built as concatenations rather than some data soup, we have basis
for a nicely concurrent yet associative transform system. If we don’t
need to keep the associative nature of the transform, then we can
optimise further, but as it comes at little to no cost, and most reduce
operations rely on associativity, then it’s good that we have that
option.

Moving away from transforms, there is the issue of *now* that crops up
whenever we talk about concurrent hardware. Sometimes, when you are
continually updating data in real time, not per frame, but actual real
time, there is no safe time to get the data, or process it. Truly
concurrent data analysis has to handle reading data that has literally
only just arrived, or is in the process of being retired. data-oriented
development helps us find a solution to this by not having a concept of
now but a concept only of the data. If you are writing a network game,
and you have a lot of messages coming in about a player, and their
killers and victims, then to get accurate information about their state,
you have to wait until they are already dead. With a data-oriented
approach, you only try to generate the information that is needed, when
it’s needed. This saves trying to analyse packets to build some
predicted state when the player is definitely not interesting, and gives
more up to date information as it doesn’t have to wait until the object
representing the data has been updated before any of the most recent
data can be seen or acted on.

The idea of now is present only in systems that are serial. There are
multiple program counters when you have multiple cores, and when you
have thousands of cores, there are thousands of different nows. Humans
think of things happening at a certain time, but sometimes you can take
so long doing something that more data has arrived by the time you’re
finished that you should probably go back and try again.

Take for example the idea of a game that tries to get the lowest
possible latency between player control pad and avatar reaction. In a
lot of games, you have to put up with the code reading the pad state,
the pad state being used to adjust animations, the animations adjusting
the renderables, the rendering system rastering and the raster system
swapping buffers. In most games it takes at least three frames

> <span>**read**</span> the player pad. in logic to new pad state. the
> character. the new bone positions. happens, moves the render requests
> into the procesing list while calling: on the old lists. happens again
> which starts to render our reaction to the pad state. then shows our
> change as

and many games have triple buffering and animation systems that don’t
update instantly.

In this case, the player could potentially be left until the last minute
before checking pad status, and apply an emergency patchup to the in
flight renderQueue. If you allowed a pad read to adjust the animation
system’s history rather than it’s current state, you could request that
it update it’s historical commits to the render system, and potentially
affect the next frame rather than the frame three buffer swaps from now.
Alternatively, have some of the game run all potential player initiated
events in parallel, then choose from the outcomes based on what really
happened, then you can have the same response time but with less
patching of data.

