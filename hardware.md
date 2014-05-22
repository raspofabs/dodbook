Looking at hardware
===================

The first thing a good software engineer does when starting work on a
new platform is read the contents listings in all the hardware manuals.
The second thing is usually try to get hello world up and running. It’s
uncommon for a games development software engineer to decide it’s a good
idea to read all the documentation available. When they do, they will be
reading them literally, and still probably not getting all the necessary
information. When it comes to understanding hardware, there is the
theoretical restrictions implied by the comments and data sheets in the
manuals, but there is also the practical restrictions that can only be
found through working with the hardware at an intimate level.

As most of the contemporary hardware is now API driven, with hardware
manuals only being presented to the engineers responsible for graphics,
audio, and media subsystems, it’s tempting to start programming on a new
piece of hardware without thinking about the hardware at all. Most
programmers working on big games in big studios don’t really know what’s
going on at the lower levels of their game engines they’re working on,
and to some extent that’s probably good as it frees them up to write
more gameplay code, but there comes a point in every developer’s life
when they have to bite the bullet and find out why their code is slow.
Some day, you’re going to be five weeks from ship and need to claw back
five frames a second on one level of the game that has been optimised in
every other area other than yours. When that day comes, you’d better
know why your code is slow, and to do that, you have to know what the
hardware is doing when it’s executing your code.

Some of the issues surrounding code performance are relevant to all
hardware configurations. Some are only pertinent to configurations that
have caches, or do write combining, or have branch prediction, but some
hardware configurations have very special restrictions that can cause
odd, but simple to fix performance glitches caused by decisions made
during the chip’s design process. These glitches are the gotchas of the
hardware, and as such, need to be learnt in order to be avoided.

When it comes to the overall design of console CPUs, The XBox360 and PS3
are RISC based, low memory speed, multi-core machines, and these do have
a set of considerations that remain somewhat misunderstood by mainstream
game developers. Understanding how these machines differ from the
desktop x86 machines that most programmers start their development life
on, can be highly illuminating. The coming generation of consoles and
other devices will change the hardware considerations again, but
understanding that you do need to consider the hardware can sometimes
only be learned by looking at historic data.

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

Deep Pipes
----------

CPUs perform instructions in pipelines. This is true of all processors,
however, the number of stages differs wildly. For games developers, it’s
important to remember that it affects all the CPUs they work on, from
the current generation of consoles such as Sony’s PS3 and Microsoft’s
Xbox360, but also to hand helds such as the Nintendo DS, the iPhone, and
other devices.

Pipelines provide a way for CPUs to trade gains in speed for latency and
branch penalties. A non-pipelined CPU finishes every instruction before
it begins the next, however a pipelined CPU starts instructions and
doesn’t necessarily finish them until many cycles later. If you imagine
a CPU as a factory, the idea is the equivalent of the production line,
where each worker has one job, rather than each worker seeing and
working on a product from start to finish. A CPU is better able to
process more data faster this way because by increasing the latency, in
well thought out programs, you only add a few cycles to any processing
during prologue or epilogue. During the transform, latency can be
mitigated by doing more work on non-related data while waiting for any
dependencies. Because the CPUs have to do a lot less per cycle, the
cycles take less time, which is what allows CPUs to get faster. What’s
happening is that it still takes just as long for a CPU to do an
operation as it always has (give or take), but because the operation is
split up into a lot of smaller stages, it is possible to do a lot more
operations per second as all of the separate stages can operate in
parallel, and any efficient code concentrates on doing this after all
other optimisations have been made.

When pipelining, the CPU consists of a number of stages, firstly the
fetch and decode stages, which in some hardware are the same stage, then
an execute stage which does the actual calculation. This stage can take
multiple cycles, but as long as the CPU has all the cycles covered by
stages, it won’t affect throughput. The CPU then finally stores the
result in the last stage, dropping the value back into the output
register or memory location.

With instructions having many stages, it can take many cycles for them
to complete, but because only one part of the instruction is in use at
each stage, a new instruction can be loaded as soon as the first
instruction has got to the second stage. This pipe-lining allows us
issue many more instructions than we could otherwise, even though they
might have high latency in themselves, and saves on transistor count as
more transistors are being used at any one time. There is less waste. In
the beginning, the main reason for this was that the circuits would take
a certain amount of time to stabilise. Logic gates, in practice, don’t
immediately switch from one logic state to another. If you add in noise,
resonance, and manufacturing error, you can begin to see that CPUs would
have to wait quite a while between cycles, massively reducing the CPU
frequency. This is why FPGAs cannot easily run at GHz speeds, they are
arrays of flexible gate systems, which means that they suffer the most
from stability problems, but amplified by the gates being located a long
way from each other, in the sense that they are not right up next to
each other like logic circuits are inside an inflexible ASIC like a
production CPU.

Pipelines require that the instructions are ready. This can be
problematic if the data the instruction is waiting on is not ready, or
if the instruction is not loaded. If there is anything stopping the
instruction from being issued it can cause a stall, or in the case of
branching causing the instructions to be run, then trashed as the
pipe-line is flushed ready to begin processing the correct branch. If
the instruction pointer is determined by some data value, it can mean a
long wait while the next instruction is loaded from main memory. If the
next instruction is based on a conditional branch, then the branch has
to wait on the condition, thus causing a number of instructions to begin
processing when the branch could invalidate all the work done so far. As
well as instructions needing to be nearby, the registers must already be
populated, otherwise something will have to wait.

Microcode: virtually function calls.
------------------------------------

To get around the limitations implicit in trying to increase throughput,
some instructions on the RISC chips aren’t really there. Instead, these
virtual instructions are like function calls, calls to macros that run a
sequence of instructions. These instructions are said to be micro-coded,
and in order to run, they often need to commandeer the CPU for their
entire duration to maintain atomicity. Some functions are micro-coded
due to their infrequent use or relative cost to implement as an
intrinsic instruction, some because of the spec, and some because they
don’t fit well with the pipe-lined model of execution. In all of these
cases, a micro-coded instruction causes a gap, called a bubble, in the
pipeline, and that’s wasted execution time. In almost all cases, these
microcoded instructions can be avoided, sometimes by changing command
line parameters (ref Cell Performance), sometimes by adjusting how you
solve a problem (ref 1\<\<n hack), and sometimes by changing the problem
completely. (sqrt considered harmful)

Single Instruction Multiple Data
--------------------------------

There are no current generation consoles that don’t have SIMD of some
sort. All hardware now has some kind of vector unit, and to some extent,
as long as you work within your boundaries, even hardware that doesn’t
have SIMD instructions, such as embedded micro controllers, can operate
on multiple data. The idea behind SIMD is simple: issue one command, and
manipulate multiple pieces of data in the same way at the same time. The
most commonly referenced implementation of this is the vector units
inherent in all current generation hardware. The AlitVec instructions on
PPC and the SPU instruction set contain many instructions that operate
on multiple pieces of data at the same time, sometimes doing asymetric
operations such as rotating, splatting, or reconfiguring the vectors. On
older machines or simple machines, the explicit instructions may not
exist, but in the world of bitwise logic, we’ve always had some SIMD
instructions hanging around as all the bitwise ops run over multiple
elements in a bit field of whatever native word length. Consider some of
the winners of the quickest bit counting routines. My favourite is the
purely SIMD style bit counter given here:

    uint32_t CountBits( uint32_t in ) {
        v = v - ((v >> 1) & 0x55555555);                    // reuse input as temporary
        v = (v & 0x33333333) + ((v >> 2) & 0x33333333);     // temp
        c = ((v + (v >> 4) & 0xF0F0F0F) * 0x1010101) >> 24; // count
        return c;
    }

So, look to your types, and see if you can add a bit of SIMD to your
development without even breaking out the vector instrinsics.

Predictable instructions
------------------------

The biggest crime to commit in a deeply pipelined core is to tell it to
do loads of instructions, then once it’s almost done, change your mind
and start on something completely different. This heinous crime is all
too common, with control flow instructions doing just that when they’re
hard to predict, or impossible to predict in the case of entirely random
data, or where the data pattern is known, but the architecture doesn’t
support branch predictions.
