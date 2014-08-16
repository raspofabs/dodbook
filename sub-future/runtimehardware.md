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

