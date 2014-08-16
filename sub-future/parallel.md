Parallel processing
-------------------

In short, parallel processing increases the number of things done at the
same time. Towards an infinite number of CPUs the amount of processing
available is infinite, but the amount of processing you can use is
limited by two factors.

The first limiting factor is the amount of work that needs to be done.
If you have a perfectly parallel algorithms, then you are limited by the
number of units of work you have to do.

For example, if a graphics card had an infinite number of cores (and
we’ll keep using infinite as it is the only good measure for future
values of N), then the maximum number of cores that it can use to render
a single polygon would be measured in how many tasks there are to do. If
the polygon was fully covering a standard 1080P HD screen with 1920 x
1080 pixels, then the highest feasible number of cores to throw at the
task of pixel shading the poly to the back buffer would be 2,073,600,
and thus the highest throughput you can possibly get from the machine
would rely on how fast one single core could transform the request to
render, into a final change of value at the pixel. This example is
slightly broken because the time taken to set up that many cores in a
normal rendering setup would probably cost more time than just splitting
the task into larger chunks, and if you use MSAA you can call on even
more cores, but eventually you’ll even run out of samples to do. The
point being, if there are not enough jobs, then the cores will be under
utilised.

A lack of jobs is hard to find in a graphics card, which is part of the
reason they have been growing in power so rapidly over the last few
years (2008-2013), and show no signs of significantly slowing down in
their GFLOPS growth. There are always more pixels to render, always more
vertices to transform, always more textures to lookup. The bottleneck in
a graphics card is still the number of cores, and that’s why it’s
relatively easy to increase the power of them compared to general
purpose chips like CPUs.

In addition to the amount of jobs the cores have to do, the relative
similarity of the jobs makes it easier to move towards a job-board style
approach to job dispatch. In every parallel architecture so far, the
instructions to run per compute core are decided specifically per core.
In the future, an implicit job system may make a difference by
instigating the concept of a public read-only job spec, and having set
up the compute cores to look out for jobs and apply their own variant
information on them. A good example might be that a graphics card may
set all the compute cores to run the same algorithm, but given some
constants about where they should get their data such as offsets into
the stream and different output rectangles of the display.

This second limiting factor is dependency. We touched on it with the
argument for pixel shaders, the set up time is a dependency. The number
of cores able to be utilised is serial up until the first step of set up
is finished, that is, the call to render primitive. Once the render call
is done, we can bifurcate our way to parallelism, but even then, we’re
wasting a lot of power because of dependence on previous steps. One way
to avoid this in hardware is have many cores wait for tasks to do by
assuming they will be in charge of some particular part of the
transform. We see it in SIMD processing where the CPU issues one
instruction to multiply a vector, and each sub core carries out its own
multiply, knowing that even though it was told that a multiply for the
whole vector was issued, it could be sure that it was the core involved
in multiplying element n of that vector. This is very useful and
possibly why future optimisations of hardware can work towards a runtime
configurable hardware layout that runs specified computations on demand,
but without explicit instruction. Instead, as soon as any data enters
into the transformation arena, it begins the configured task without
asking for, or needing information on how to interpret the data. This
type of stream processing may be best suited to runtime configurable
hardware.

Ahmdal’s Law is based on two constants, the time that a process must be
serial and the time that a process can be parallel. In the world of
infinite core computing we must continually strive for the lowest
possible serial latency in our development. That means we must find out
what is critical, what can be done without prior information, what can
be done in preparation, what can be not done until the very last moment.
All these elements of processing add up to a full product, and without
considering what the output data is and how we get there, we could
continually return to the state where we are optimising for code, and
not for what is of ultimate importance, the experience due to
realisation of output data in a timely fashion.

