Counting and Domain knowledge
=============================

Counting is something we take for granted. We count things and ignore
things based on probabilities instantly calculated from the numbers
obvious to us. Counting is a useful tool when it comes to processing
information, saving space while doing transformations, and for writing a
problem in a more mathematically correct manner, which usually leads to
a more efficient solution and one that can be more easily generalised or
reused. To some extent, we also count on things that can’t be counted.
We consider the chance of something happening, and when it’s going to
happen and take that into account. This is something that we have no way
of teaching compilers as it is different every time and is often part of
the design. We must assume they cannot be taught this until the
compilers become the programmers. This information is what we call
domain knowledge.

Some languages can be seen to count, functional languages to a certain
extent always count, but C++ does not. Most imperative languages don’t
count other than in the optimisation stage, the stage when loops are
unrolled, branches that are controlled by constants are reduced, and
constant expressions are brought to their minimal representation. All
this helps reduce the size of a program, and also helps increase its
speed, but the level of counting available to a compiler is quite simple
compared to what humans can accomplish given the full description of a
problem to solve. The problem that a piece of software is designed to
solve is not transparent to the compiler, the assembler, or the CPU that
runs the machine code. The computer, the language, nor programming
paradigm will solve the problem of transferring the entire design and
all the domain knowledge into the executable code, whether static, or
dynamic such as in the case of runtime compiling languages or
interpreters that can optimise the bytecode at runtime.

Counting is not simple. Counting is an area of Mathematics linked with
probability and very large numbers, and in such is the cornerstone of
most forms of cryptography. Handling very large numbers, but accurately,
is not something computers are very good at. Computers do well with very
large amounts of medium sized numbers. A computer is very happy working
on millions of different numbers ranging in the millions, and 64 bit
computers are happy all the way up to large quadrillions, but when the
size of numbers is measured in thousands of zeros, computers have to
give up and resort to just doing what they’re told.

The simple factorial is a function that usually gets out of hand for
values greater than 20 ($20! = 2432902008176640000$ is the largest
factorial less than $2^{64} = 18446744073709551616$) and when we’re
working with taking items from a list of possible items, the factorial
function becomes a common tool.

When we think about a problem, we often have an idea of how many things
we are working with. A compiler cannot guess at these things as it has
to work at runtime with only the information given at compile time.
Branch predictors help with some aspects of this lack of runtime
rebuilding, as they allow a program to respond to actual counts by
changing the default flow. We cannot hope that our statically compiled
programs can count like the runtime compiled languages or the bytecode
languages that have runtime optimisers.

And so we have now a vague idea of what counting means. We see how
humans are currently the only means by which a computer can count on any
large scale, as only humans can grasp the concept for which the programs
are designed. Counting means to understand the larger picture of what
kinds of numbers of events and the expected type and value of the
elements that are to be processed. This forward thinking can be
intuitive reasoning based on the design of the software (in a game, an
entity may only be able to die once) or may be garnered by
experimentation (conducting tests is a very good way to begin any
refactoring) or third part produced evidence (if an area of development
is new to you, you should see if someone else has publicly published any
papers or reports,) but will not likely ever be part of an optimising
compiler, so we must learn to count for our programs.

