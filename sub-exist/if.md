Why use an if
-------------

When studying software engineering you may find reference to cyclomatic
complexity or conditional complexity. This is a complexity metric
providing a numeric representation of the complexity of code, and is
used in analysing large scale software projects. Cyclomatic complexity
concerns itself only with flow control. The formula, summarised for our
purposes, is one (1) plus the number of conditionals present in the
system being analysed. That means for any system it starts at one, and
for each if, while, for, and do-while, we add one. We also add one per
path in a switch statement excluding the default case if present (this
is because whether or not the default case is included, it is part of
the possible routes through the code, so counts like the else case of an
if, as in, it isn’t counted, only the met conditions are counted.) under
the hood, if we consider how a virtual call works, that is, a lookup in
a function pointer table followed by a branch into the class member
function, we can see that a virtual call is effectively just as complex
as a switch statement. Counting the flow control statements is more
difficult in a virtual call because to know the complexity value, you
have to know the number of possible classes member functions that can
fulfil that request. In the case of a virtual call, you have to count
the number of overrides to a base virtual call. If the base is
pure-virtual, then you may subtract one from the complexity. However, if
you don’t have access to all the code that is running, which can be
possible in the case of dynamically loaded libraries, then the number of
different code paths that the process can take increases by an unknown
amount. This hidden or obscured complexity is necessary to allow third
party libraries to interface with the core process, but requires a level
of trust that implies that no single part of the process is ever going
to be thoroughly tested.

Analysing the complexity of a system helps us understand how difficult
it is to test, and in turn, how hard it is to debug. Sometimes, the
difficulty we have in debugging comes from not fully observing all the
flow control points, at which point the program will have entered into a
state we had not expected or prepared for. With virtual calls, the
likelihood of that happening can dramatically increase as we can not be
sure that we know all the different ways the code can branch until we
either litter the code with logging, or step through in a debugger to
see where it goes at run-time.

Returning to complexity in general, we must submit that we use flow
control to change what is executed in our programs. In most cases these
flow controls are put in for one of two reasons: design, and
implementation necessity. The first is when we need to implement the
design, a gameplay feature that has to only happen when some conditions
are met, such as jumping when the jump button is pressed, or autosaving
at a save checkpoint when the savedata is dirty. The second form of flow
control is structural, or defensive programming techniques where the
function operating on the data isn’t sure that the data exists, or is
making sure bounds are observed.

In real world cases, the most common use of an explicit flow control
statement is in defensive programming. Most of our flow control
statements are just to stop crashes, to check bounds, pointers being
null, or any other exceptional cases that would bring the program to a
halt. The second most common is loop control, though these are numerous,
most CPUs have hardware optimisations for these, and most compilers do a
very good job of removing condition checks that aren’t necessary. The
third most common flow control comes from polymorphic calls, which can
be helpful in implementing some of the gameplay logic, but mostly are
there to entertain the do-more-with-less-code development model
partially enforced in the object-oriented approach to writing games.
Actual visible game design originating flow control comes a distant
fourth place in these causes of branching, leading to an
under-appreciation of the effect each conditional has on the performance
of the software. That is, when the rest of your code-base is slow, it’s
hard to validate writing fast code for any one task.

If we try to keep our working set of data as a collections of arrays, we
can guarantee that all our data is not null. That one step alone will
eliminate most of our flow control statements. The third most common set
of flow control statements were the inherent flow control in a virtual
call, they are covered later in section [sec:exist-poly], but simply
put, if you don’t have an explicit type, you don’t need to switch on it,
so those flow control statements go away as well. Finally, we get to
gameplay logic, which there is no simple way to eradicate. We can get
most of the way there with condition tables which will be covered in
chapter [chap:condition], but for now we will assume they are allowed to
stay.

Reducing the amount of conditions, and thus reducing the cyclomatic
complexity on such a scale is an amazing benefit that cannot be
overlooked, but it is one that comes with a cost. The reason we are able
to get rid of the check for null is that we now have our data in a
format that doesn’t allow for null. This inflexibility will prove to be
a benefit, but it requires a new way of processing our entities. Where
we once had rooms, and we looked in the rooms to find out if there were
any doors on the walls we bumped into (in order to either pass through,
or instead do a collision response,) we now look in the table of doors
to see if there are any that match our roomid. This reversal of
ownership can be a massive benefit in debugging, but sometimes can
appear backwards when all you want to do is find out what doors you can
use to get out of a room.

If you’ve ever worked with shopping lists, or todo lists, you’ll know
how much more efficient you are when you have a definite list of things
to get or get done. It’s very easy to make a list, and easy to add to it
too. If you’re going shopping, it’s very hard to think what might be
missing from your house in order to get what you need. If you’re the
type that tries to plan meals, then a list is nigh on essential as you
figure out ingredients and then tally up the number of tins of tomatoes,
or how many different meats or vegetables you need to last through all
the meals you have planned. If you have a todo list and a calendar, you
know who is coming and what needs to be done to prepare for them, how
many extra mouths need feeding, how many extra bottles of beer to buy,
or how much washing you need to do to make enough beds for the visitors.
Todo lists are great because you can set an end goal and then add in sub
tasks that make a large and long distant goal seem more doable, and also
provide a little urgency that is usually missing when the deadline is so
far away.

When your program is running, if you don’t give it lists to work with,
and instead let it do whatever comes up next, it will be inefficient,
slow, and probably have irregular frame timings. Inefficiency comes from
not knowing what kind of processing is coming up next. In the case of
large arrays of pointers to heterogeneous classes all being called with
an `update()` function, you can get very high counts of cache misses
both in data and instruction cache. If the code tries to do a lot with
this pointer, which it usually does because one of the major beliefs of
object-oriented programmers is that virtual calls are only for higher
level operations, not small, low level ones, then you can virtually
guarantee that not only will the instruction and data cache be thrashed
by each call, but most branch predictor slots could be too dirty to
offer any benefit when the next `update()` runs. Assuming that virtual
calls don’t add up because they are called on high level code is fine
until they become the go to programming style and you stop thinking
about how they affect your application when there are millions of
virtual calls per second. All those inefficient calls are going to add
up somewhere, but luckily for the object oriented zealot, they never
appear on any profiles. They always appear somewhere in the code that is
being called. Slowness also comes from not being able to see how much
work needs to be done, and therefore not being able to scale the work to
fit what is possible in the time-frame given. Without a todo list, and
an ability to estimate the amount of time that each task will take, it
is impossible to decide the best course of action to take in order to
reduce overhead while maintaining feedback to the user. Irregular frame
timings also can be blamed on not being able to act on distant goals
ahead of time. If you know you have to load an area because a player has
ventured into a position where it is possible they will soon be entering
an unloaded area, the streaming system can be told to drag in any data
necessary. In most games this happens with explicit triggers, but there
is no such system for many other game elements. It’s unheard of for an
AI to pathfind to some goal because there might soon be a need to head
that way. It’s not commonplace to find a physics system doing look ahead
to see if a collision has happened in the future in order to start doing
a more complex breakup simulation. But, if you let your game generate
todo lists, shopping lists, distant goals, and allow for preventative
measures by forward thinking, then you can simplify your task as a coder
into prioritising goals and effects, or writing code that generates
priorities at runtime.

In addition to the obvious lists, metrics on your game are highly
important. If you find that you’ve been optimising your game for a silky
smooth frame rate and you think you have a really steady 30fps or 60fps,
and yet your customers and testers keep coming back with comments about
nasty frame spikes and dropout, then you’re not profiling the right
thing. Sometimes you have to profile a game while it is being played.
Get yourself a profiler that runs all the time, and can report the state
of the game when the frame time goes over budget. Sometimes you need the
data from a number of frames around when it happened to really figure
out what is going on, but in all cases, unless you’re letting real
testers run your profiler, you’re never going to get real world
profiling data.

Existence-based-processing is when you process every element in a
homogeneous set of data. You run the same instructions for every element
in that set. There is no definite requirement for the output in this
specification, however, usually it is one of three types of operation:
filter, mutation, or emission. A mutation is a one to one manipulation
of the data, it takes incoming data and some constants that are setup
before the transform, and produces one element for each input element. A
filter takes incoming data, again with some constants set up before the
transform, and produces one element or zero elements for each input
element. An emission is a manipulation on the incoming data that can
produce multiple output elements. Just like the other two transforms, an
emission can use constants, but there is no guaranteed size of the
output table; it can produce anywhere between zero and infinity
elements.

Every CPU can efficiently handle running processing kernels over
homogeneous sets of data, that is, doing the same operation over and
over again over contiguous data. When there is no global state, no
accumulator, it is proven to be parallelisable. Examples can be given
from existing technologies such as mapreduce and opencl as to how to go
about building real work applications within these restrictions.
Stateless transforms also commit no crimes that prevent them from being
used within distributed processing technologies. Erlang relies on these
as language features to enable not just thread safe processing, not just
inter process safe processing, but distributed computing safe
processing. Stateless transforms of stateful data is highly robust, and
deeply parallelisable.

Within the processing of each element, that is for each datum operated
on by the transform kernel, it is fair to use control flow. Almost all
compilers should be able to reduce simple local value branch
instructions into a platform’s preferred branchless representation. When
considering branches inside transforms, it’s best to compare to existing
implementations of stream processing such as graphics card shaders or
OpenCL kernels.

In predication, flow control statements are not nearly ignored, they are
used instead as an indicator of how to merge two results. When the flow
control is not based on a constant, a predicated if will generate code
that will run both sides of the branch at the same time and discard one
result based on the value of the condition. It manages this by selecting
one result based on the condition, in some CPUs there is an fsel
intrinsic, other CPUs may have a cmov instruction, but all CPUs can use
masking to effect this trick.

There are other solutions in the form of SIMD and MIMD. SIMD or
single-instruction-multiple-data allows the parallel processing of data
when the instructions are the same. If there are any conditionals, then
as long as the result of the condition is the same across the data, the
function returns quickly. If the condition result is different across
the different data, the function stalls for one branch remembering which
of the data had chosen which path, completes for one side, then goes
back and continues for the other side. This costs time, but is not as
expensive as predication as it does not always run both branches. In
other systems, the condition can lead to new micro jobs handed off to
different cores, converging back to the main thread only once all
branches have completed.

In MIMD, that is multiple instruction, multiple data, every piece of
data can be operated on by a different set of instructions. Each piece
of data can take a different path. This is the simplest to code for
because it’s how most parallel programming is currently done. We add a
thread and process some more data with a separate thread of execution.
MIMD includes multi-core general purpose CPUs. MIMD often allows shared
memory access and all the synchronisation issues that come with it. MIMD
is by far the easiest to get up and running, but it is also the most
prone to the kind of rare fatal error that costs a lot of time to debug.
