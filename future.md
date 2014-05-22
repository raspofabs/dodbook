Future
======

The future of hardware is almost certainly increasingly parallel
processing with all the related problems that entails; from power
consumption, through deserialising our processing, to distribution of
jobs across more than just a few local cores.

Supercomputers have been vector machines for decades, and any advances
in graphics cards comes with an increase in the number of cores that run
transforms. Mobile phones have 4 cores and even some microcontrollers
have multi-core layouts[^1] Stream processing hardware is showing to be
more capable of increasing throughput per generation than the general
purpose computing architecture employed in the design of CPUs and
micro-controllers. It’s shaping up that the coming generations of
hardware are going to be a battles of the parallel processing
beasts[^2], larger core counts and more numerous pipes. Memory always
seems to be at a premium, so again, we’ll probably be trying to push
next gen games out without having enough space in which to work. One
area that has not been pushed around much has been offloading processing
outside the local machine. Even though there has been plenty of work
done with very high latency architectures such as Beowulf clusters or
grid computing, the idea that they could be useful for games is still in
its infancy due to the virtually real-time nature of processing for
games. It could be a while off, but we may see it come one day, and it’s
better not to let it sneak up on us. Once we need it, we will need a
language that handles offloading to external processing like any other
threaded task. Erlang is one such language. Erlang is functional (with a
tendency for immutable state which helps very much with concurrency) and
is highly process oriented with a very simple migration path from
single-machine multi-threaded to remote processing or grid compute style
distributed processing and a large number of options for fault
tolerance. Node-js offers some of the same parallelism and a much
shorter learning time as it is based on Javascript. Functional languages
would seem to dominate, but OpenCL isn’t purely functional, and C++AMP
only requires you consider how to amplify your code with parallelism,
which might not be enough for how many cores we really end up. Whatever
language we do end up using to leverage the power of parallel
processing, once it’s ubiquitous, we’d better be sure we’re not still
thinking serial.

But parallel processing isn’t the only thing on the horizon. Along with
many cores comes the beginnings of a new issue that we’re only starting
to see traces of outside supercomputing. The issue of power per watt. In
mobile gaming, though we’re striving to make a game that works, one
thing that developers aren’t regularly doing that will affect sales in
the years to come, is keeping the power consumption down on purpose. The
mobile device users will put up with us eking out the last of the
performance for only so long. There is a bigger thing at stake than
being the best graphical performance and fastest AI code, there is also
the need to have our applications be small enough to be kept on the
device, and also not eat up enough battery that the users drop the
application like a hot potato. Data-oriented design can address this
issue, but only if we add it to the list of considerations when
developing a game. As with parallelism, the language we use impacts the
possibilities. If we continue to move towards more high level languages
such as C\# and Java, then we will need smarter compilers to reduce the
overhead, but if we develop in a language made to support tasking, such
as the process kernels in OpenCL or the lightweight threads of Erlang,
then we may find new hardware changes to match the language much the
same way C++ and object-oriented design changed the way CPUs were
designed.

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

Distributed computing
---------------------

When you think of distributed computing, normally you think of farms of
computers spread over multiple locations, running long lifetime
processes on massive amounts of data. You think of on demand load
balancing systems providing more compute where necessary on the grid.
All this talk of large scale is just another step out from our CPU
cores. Another layer that we can move to when the possibility presents
itself. One day, maybe, we will have invisible grid computing for the
consumer. The idea of spreading the compute load out from the physical
device was first presented commercially with the CellBE, the idea that
adding more compute to an existing hardware instance could be done
without explicitly linking hardware through a proprietary interface.
There were articles talking of how your TV could increase the quality of
your gaming experience by allowing the console to offload some of the
processing onto the TVs processor. This has not come to pass, but the
common core, the idea of doing more work by adding more machines, that
has not gone away and is in common use in most development companies,
whether by use of the free to use build accelerators such as the one
included in the Sony developer tools, or proprietary software such as
Xoreax’s IncrediBuild. Adding more compute to processes that can safely
be very high latency is definitely one way of using grid engines, but
another alternative is to use grid engine’s to provide answers to
questions not yet asked. If you know that a type of question is common
during your processing, then offloading the question process so it
processes all known variants of the question means you can get back the
answer to all the possible questions before it’s even asked.

For example, If you know that your scene is going to animate, and you
want to do a ray cast from some entities to other entities, but don’t
know which, you can task the grid engine with advancing the animation
and doing all the ray casts. Then, once you are ready, read from the ray
casts that you decided that you did need after whatever calculations you
needed to do. That’s a lot of wasted processing power, but it reduces
latency. When you’re thinking about the future, it is only sensible to
think about latency as the future contains an infinite number of
processing cores.

Using this one example, you can ramp it back to current generation
hardware by offloading processes to begin large scale ray casting, and
during the main thread calculation stages, cull tasks from the thread
that is managing the ray casts. This means that you can get started on
tasks, but only waste cycles when you don’t know enough to not.

With very high speed network adapters, very high bandwidth network
connections to the internet, grid computing inside games might become
more commonplace than expected. What gameplay elements this amount of
processing power can open up is beyond our vision, but once it is here,
we can expect remote processing through something akin to stored
procedures to become a staple part of the game developer tool-kit.

Runtime hardware configuration
------------------------------

We cannot know what the future brings, and some assumptions we have
about CPUs might be broken. One such assumption might be that our
hardware is fixed in one form once it has been fabricated. Both field
programmable gate arrays and complex programmable logic arrays allow for
change during their lifetime, and some announcements have been made
about mainstream hardware adding FPGAs to their arsenal[^3] which may
open the door to FPGA add-on cards much the same way we saw the take-off
of graphics cards once they got a foot in the door.

FPGAs present a new and interesting problem to programmers, specifically
to the programmers that may be inventing new plans for others to
consume. One way this could pan out is by re-orienting the mindset of
the average programmer into that of a flow based or stream processing
developer. Being able to take game data and manipulate it with highly
efficient, and low latency modules dynamically loaded onto FPGAs could
be the final nail in the coffin for any language that links code with
data.

Approaches to development similar to that imposed on us by the shader
model and the process of getting data into the right layout for the
shaders might have been good training, readying us for the coming days
of compute power only really being available if we order it for later.
With dynamic partial reconfiguration, we would have the same benefits
seen in being able to switch shaders mid render. That is, the ability to
utilise an FPGA much smaller than would be necessary if we were to
attempt to cram all the potential processing modules onto it at once.
We’ve been here before. This extremely high latency before being able to
compute, followed by very fast processing once the computational
framework is ready, is very similar to programming with shaders, so much
so that we might not take that long bringing our existing engines up to
speed.

The CellBE was an attempt at this way of working, but was overlooked by
many as just a strange piece of hardware. The core, an underpowered CPU
that would look after feeding all the high power SPUs was assumed to be
a general purpose CPU. This was an unfortunate side effect of too many
years developing for out-of-order CPUs, and a deep investment in random
memory access programming methods such as object-oriented design and
interpreted languages. We don’t know what other CPUs may come along in
the future, but we can attempt to use a data-oriented approach and not
try to make a CPU work the way we want to work, but work with it to make
the best out of what we have.

Data centric development in hardware design
-------------------------------------------

Once software solutions concentrate on transforming data, what changes
can we expect from hardware vendors? Is that a silly question? Would a
change of programming paradigm really affect the people who create
hardware?

What should we promote and demote in order to get the most from our
transistors?

move away from serial thinking more functional programming, where there
are no side-effects, leads to solutions for infinite numbers of cores

Whatever the future brings with respect to hardware and processing
configurations, there are certain assumptions we can make.

[^1]: Parallax Propeller is a really interesting microcontroller that’s
    been out for some time, but provides a unique perspective on
    parallel computing

[^2]: Parallela was a successful 2012 Kickstarter campaign for Adapteva,
    in which their roadmap points to 1024 core boards being produced in
    2014

[^3]: One really good reason for an FPGA is to allow for future proofing
    of output connectivity. FPGAs can be used to test out new standards
    such as a new HDMI specification or a completely different encoding
