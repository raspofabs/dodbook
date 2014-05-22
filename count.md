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

Learning to count
-----------------

Sometimes we just want to save space, and to do that we need to
understand the data being compressed. The compiler cannot do it for us,
and we will always have a better idea of what the data is meant to be
like. The best example of the difference between trying to compress
anything and being able to specialise must be the special case lossy
compressors: JPEG, MPG, and the like. In these cases, and others where
the information is held inside the data, but not all the data is
required to rebuild the information, only an external agent that is
aware of what actually constitutes important data can provide the
information about what can be ignored. Lossy algorithms are based on
what can be expected (predictions which might require a transform into a
different way of viewing the data), and what is fundamental (some basic
structure that is known, but would not be picked up by a standard
compression technique). All lossy techniques rely on knowing the
difference between what is close enough and what is unacceptable
degradation. Lossy techniques rely on biological imperfections,
something which is still hard to build a general optimiser for.

Lossless compression relies on being able to count, and in one way, we
have invented counting algorithms in forms of Huffman or arithmetic
encoding. These algorithms count before they compress, to determine the
chance of any particular element being seen. Many lossless compressors
take an approach like this, or use history relative probability, such as
run-length-encoding where repeating a value is one of two high
probability choices available during encoding. Not being able to look at
the data beforehand and come up with a realistic, or even reasonable
estimate of probability of each possible encodable value will hamper any
form of compression that relies on probabilities.

Without understanding the cause of the data, these algorithmic
approaches can only go so far. If we know the reason why the data
exists, as in where it comes from or what it’s for, there are often
opportunities for even better compression. For example, compressing the
RGB in an image with alpha, knowing that the data is bitwise AND onto
destination data that has a known set of bits set, knowing the ranges of
many parts of a document and knowing biases for values given other
values in the same document.

Counting to find out facts
--------------------------

Counting isn’t just about compression, sometimes it’s about speed. Given
an algorithm, sometimes the best way to make it faster is to find out
what data it’s being given in the first place and find out if it comes
in regular patterns, or is large enough or small enough to change the
algorithm. In data-oriented design, it’s always pertinent to perform
some analysis of the real world performance of your code, and sometimes
what you count can be very important.

If a function being called by iterating over a large set of data and
being called on every element in the list, then the function can be
timed in various ways. You can time how long it takes to do the whole
set of updates, then divide by the number of updates, or you can try to
profile the function per call. You’re probably going to get reasonably
accurate timings either way, but what if the function was only going to
be called if some value in the element was set? What if the function is
normally fast but has spikes?

In the case of spikes, this is where per call timings are essential.
Counting the nanoseconds for operations (and storing the arguments going
into them) is a great way to do analysis of why your function has
unexpected performance.

In some cases, checking whether or not to do work just before doing it
can bring about significant performance issues. If the function to run
is not known at compile time, then there is a higher chance that this
pattern exhibits bad performance. Take the dirty flag as an example. If
an entity has a function that can be made dirty and only needs to be
updated when that flag is dirty, then it makes sense to check that flag
before committing to doing any work, but sometimes you can’t stop the
compiler from assuming the probability of that is high enough to begin
doing the work before you’re sure it’s necessary.

This code runs quickly and efficiently while the dirty flag is true, but
the moment the flag is false, depending on the target platform, this can
lead to the pipeline being flushed, and the cache being dirtied by code
that is ultimately not required to even be run.

This code, on most platforms, will run faster, even though it’s
apparently doing more work. The difference is that this code runs
through all the necessary elements only loading the data necessary to
perform the check to see if work is required to be done. Once the work
list is finished, then a definite call to do work can be made on each
item in the list. In the worst case, all the items in the container
require work, and the work list is full, and depending on your target,
this might be slower than the original iteration, but if there will be a
number of dirty items at which the two pass process is faster, and only
actually counting and profiling will find that value out. You cannot
rely on a compiler to reorganise your calls this way.

Some work has been done in virtual machines to do optimisations like
this, which leads to really good performance in spite of badly laid out
code, but the performance comes at a price, namely the fact that during
runtime, the virtual machine is having to look for optimisations to
make.

Domain Knowledge
----------------

Every time you find that you’re looking up the answer to a question and
find that though the calculation seems complex, the answer is highly
correlative to only a small subset of the inputs, there’s a chance that
you’re missing some domain knowledge. Sometimes you don’t even need the
answer to a question as the design prescribes an implicit value. These
implicit values, when figured into the code, can reduce a highly complex
function to one that is simple, or better, doesn’t need to run as often.

The full health bar that doesn’t need regenerating is a form of domain
knowledge that lead to existence based processing of the regeneration
code. Code that would otherwise have run without effect now only runs
when required.

Knowing that a compute kernel only affects elements that have differing
values, such as a Gaussian blur, can affect how much time it takes to
process the data. Marking regions of a data-store as potentially able to
be affected by the kernel in a pre-parse can make all the difference,
and can also help split a task across multiple workers.

Experimentation, documentation, and analysis, are the key ingredients to
any real understanding of data transforms. Without looking at the data
that an algorithm is using, and what comes out given that data, there
will never be any hope of insight or improvement.

In one analysis, an assumed to be completely smooth accelerometer
reading was proven to include the jerk vibrations from the force
propelling the sensor. This caused noisy data which increased the
difficulty to complete the intended analysis. Taking this base noise
into account allowed for a much simpler and higher accuracy algorithm.

When trying to find out what was causing a DVD read to run slow, an
analysis was required to find out where the head was while it was
reading. In the data, we found that the game was reading data from where
we expected, but also from a configuration file that was meant to be
read in debug builds. The file wasn’t really being read, but it’s
date-stamp was, which meant that the read head wasn’t where it was meant
to be while streaming, once a second. Without checking the data, there
wouldn’t have been a very good chance to find the bug.

Sometimes domain knowledge comes purely from the design of the game.
Knowing that you can eject the data for an area of the game as a section
is one way only can be a simple memory saver. Knowing that building
cannot return to their fixed state after being destroyed is important
too. For most older games that did allow destructible environments, the
knowledge that the environment didn’t need to be reversible was used to
reduce the memory footprint of the level data. Most games would require
reloading the level before being able to restart as once the structures
were destroyed, especially with procedural destruction, there was no
information on how the building started out. This lack of information
was a space saver, and could have been seen as a form of domain
knowledge.

Other key pieces of data can come from without. Analytics, both from
people playing the game and bots, can provide much needed data. Making a
bot for a single-player game can be very rewarding as it allows you to
run tests for things that would otherwise be too simple and thus too
boring for even the most dedicated testers. For example, running a
frame-rate analysis for a game can be highly tedious, but can provide a
massive amount of beneficial data to both the art team, and the engine
team, as they can look at specific hotspot areas in both the art assets,
and the engine technology. Knowledge of what really happens in the game
in this case leads to optimising only the parts of the game engine that
are really required to produce the game. Without a real analysis of the
performance of the game given the real data, the real game code and a
real run through, any optimisations have to be speculative at best. Even
if you can prove that an area of the engine code is running really
slowly, there’s no point in optimising it if it’s only used in sections
of the game where the engine has plenty of spare resources and doesn’t
need to run any faster. Another reason why running these tests via a bot
is important is that as with all optimisations and refactorings, it’s
important that once you have made your changes you must be able to see
the outcome of those changes, and must be able to prove that you haven’t
broken anything else while changing the code, and that you actually
improved things.

Sometimes it can be hard to run the same test multiple times. Sometimes
your test isn’t entirely deterministic. When that is the case you need
to gather your data more carefully and be aware of the statistical
significance of any data you have. Learn how to determine what
constitutes significant values and can be confirmed as improvement over
the noise inherent in the data you can collect.

Facts from counting
-------------------

Proofs sometimes come from trying to find out the patterns behind data.
Find a pattern in your results from a function and you might find a much
simpler way to calculate your values.

ryg

simple9, run length encoding, dictionary

array or map, or spatial partitioning?
