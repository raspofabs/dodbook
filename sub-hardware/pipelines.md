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

