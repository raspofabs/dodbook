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

[^1]: Parallax Propeller is a really interesting microcontroller that’s
    been out for some time, but provides a unique perspective on
    parallel computing

[^2]: Parallela was a successful 2012 Kickstarter campaign for Adapteva,
    in which their roadmap points to 1024 core boards being produced in
    2014

[^3]: One really good reason for an FPGA is to allow for future proofing
    of output connectivity. FPGAs can be used to test out new standards
    such as a new HDMI specification or a completely different encoding
