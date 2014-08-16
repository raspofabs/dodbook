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

