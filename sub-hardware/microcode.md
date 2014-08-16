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

