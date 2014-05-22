Concurrency
===========

Any book on games development practices for contemporary and future
hardware must cover the issues of concurrency. There will come a time
when we have more cores in our computers than we have pixels on screen,
and when that happens, it would be best if we were already coding for
it, coding in a style that allows for maximal throughput with the
smallest latency. Thinking about how to solve problems for five, ten or
even one hundred cores isn’t going to keep you safe. You must think
about how your algorithms would work when you have an infinite number of
cores. Can you make your algorithms work for N cores?

Writing concurrent software has been seen as a hard task in the past
because most people think they understand threading and can’t get their
heads around all the different corner cases that are introduced when you
share the same memory as another thread. Fixing these with mutexs and
critical sections can become a minefield of badly written code that
works only 99% of the time. For any real concurrent development we have
to start thinking about our code transforming data. Every time you get a
deadlock or a race condition in threaded code, it’s because there’s some
ownership issue. If you code from a data transform point of view, then
there are some simple ground rules that provide very stable tools for
developing truly concurrent software.

What it means to be thread-safe
-------------------------------

Academics consistently focus on what is possible and correct, rather
than what is practical and usable, which is why we’ve been inundated
with multi-threaded techniques that work, but cause a lot of unnecessary
pain when used in a high performance system such as a game. The idea
that something is thread-safe implies more than just that it is safe to
use in a multi-threaded environment. There are lots of thread safe
functions that aren’t mentioned becuase they seem trivial, but it’s a
useful distinction to make when you are tracking down what could be
causing a strange thread issue. There are functions without
side-effects, such as the intrinsics for sin, sqrt, that return a value
given a value. There is no way they can cause any other code to change
behaviour, and no other code can change its behaviour either[^1]. In
addition to these very simple functions, there are the simple functions
that change things in an idempotent fashion, such as memset.

Thread safe implies that it doesn’t just access its own data, but
accesses some shared data without causing the system to enter into an
inconsistent state. Inconsistent state is a natural side effect of
multiple processes accessing and writing to shared memory. It is these
side effects that are the cause of many bugs in multi-threaded code,
which is why the develpers of the Erlang language chose to limit the
programmer to code that doesn’t have side-effects. Any code that relies
on reading from a shared memory before writing back an adjusted value
can cause inconsistent state as there is no way to guarantee that the
writing will take place before anyone else reads it before they modify
it.

    int shared = 0;
    void foo() {
        int a = shared;
        a += RunSomeCalculation();
        shared = a;
    }

Making this work in practice is hard and expensive. The standard
technique used to ensure the state is consistent is to make the value
update atomic. How this is achieved depends on the hardware and the
compiler. Most hardware has an atomic instruction that can be used to
create thread-safety through mutual exclusions. On most hardware the
atomic instruction is a compare and swap, or CAS. Building larger tools
for thread-safety from this has been the mainstay of multi-threaded
programmers and operating system developers for decades, but with the
advent of multi-core consoles, programmers not well versed in the
potential pitfalls of multi-threaded development are suffering because
of the learning cliff involved in making all their code work perfectly
over six or more hardware threads.

Using mutual exclusions, it’s possible to rewrite the previous example:

    int shared = 0;
    Mutex sharedMutex;
    void foo() {
        sharedMutex.acquire();
        int a = shared;
        a += RunSomeCalculation();
        shared = a;
        sharedMutex.release();
    }

And now it works. No matter what, this function will now always finish
its task without some other process damaging its data. Every time one of
the hardware threads encounters this code, it stops all processing until
the mutex is acquired. Once it’s acquired, no other hardware thread can
enter into these instructions until the current thread releases the
mutex at the far end.

Every time a thread-safe function uses a mutex section, the whole
machine stops to do just one thing. Every time you do stuff inside a
mutex, you make the code thread-safe by making it serial. Every time you
use a mutex, you make your code run bad on infinite core machines.

Thread-safe, therefore, is another way of saying: not concurrent, but
won’t break anything. Concurrency is when multiple threads are doing
their thing without any mutex calls, semaphores, or other form of
serialisation of task. Concurrent means at the same time. A lot of the
problems that are solved by academics using thread-safety to develop
their multi-threaded applications needn’t be mutex bound. There are many
ways to skin a cat, and many ways to avoid a mutex. Mutex are only
necessary when more than one thread shares write privileges on a piece
of memory. If you can redesign your algorithms so they only ever require
one thread to be given write privilege, then you can work towards a
fully concurrent system.

Ownership is key to developing most concurrent algorithms. Concurrency
only happens when the code cannot be in a bad state, not because it
checks before doing work, but because the design is such that no process
can interfere with another in any way.

Inherently concurrent operations
--------------------------------

When working with tables of data, many operations are inherently
concurrent. Simple transforms that take one table and generate the next
step, such as those of physics systems or AI state / finite state
machines, are inherently concurrent. You could provide a core per row /
element and there would be no issues at all. Setting up the local bone
transforms from a skeletal animation data stream, ticking timers,
producing condition values for later use in condition tables. All these
are completely concurrent tasks. Anything that could be implemented as a
pixel or vertex shader is inherently concurrent, which is why parallel
processing languages such as shader models, do not cheaply allow for
random write to memory, and don’t allow accumulators across elements.

Seeing that these operations are inherently concurrent, we can start to
see that it’s possible to restructure our game from an end result
perspective. We can use the idea of a structured query to help us find
our critical path back to the game state. Many table transforms can be
split up into much smaller pieces, possibly thinking along the lines of
map reduce, bringing some previously serial operations into the
concurrent solution set.

Any N to N transform is perfectly concurrent. Any N to \<=N is perfectly
concurrent, but depending on how you handle output NULLs, you could end
up wasting memory. A reduce stage is necessary, but that could be
managed by a gathering task after the main task has finished, or at
least, after the first results have started coming in.

Any uncoupled transforms can be run concurrently. Ticking all the finite
state machines can happen at the same time as updating the phsyics
model, can happen at the same time as the graphics culling system
building the next frame’s render list. As long as all your different
game state transforms are independent from each other’s current output,
they can be dependent on each other’s original state and still maintain
concurrency.

For example, the physics system can update while the renderer and the AI
rely on the positions and velocities of the current frame. The AI can
update while the animation system can rely on the previous set of
states.

Multi stage transforms, such as physics engine broadphase, detection,
reaction and resolution, will traditionally be run in series while the
transforms inside each stage run concurrently. Standard solutions to
these stages require that all data be finished processing from each
previous stage, but if you can find some splitting planes for the
elements during the first stage, you can then remove temporal cohesion
from the processing because you can know what is necessary for the next
step and hand out jobs from finished subsets of each stage’s results.

Concurrent operation assumes that each core operating on the data is
free to access that data without interfering, but there is a way that
seemingly unconnected processes can end up getting in each other’s way.
Most systems have multiple layers of cache, and this is where the
accident can happen. False sharing is when data, though actually
unrelated, is connected by the physical layout of the hardware. For
example, the cachelines of a CPU might be 16 to 128 bytes long. If two
different CPUs try to write to neighbouring bytes, or words, at best the
cores will lock up as the memory is shunted around trying to keep memory
consistent, but worse, could end up losing data if the cache is not
coherent[^2]. To reduce the chance of this happening, processing of
small element tables should consider this and split any cooperation into
cacheline size jobs.

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

[^1]: If you discount the possibility of other code changing the
    floating point operation mode

[^2]: cache coherency is the system by which changed data is propagated
    to other caches so that consistent state is achieved.
