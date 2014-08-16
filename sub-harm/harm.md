The Harm
--------

*Virtuals don’t cost much, but if you call them a lot it can add up.\
aka - death by a thousand papercuts*

The overhead of a virtual call is negligible under simple inspection.
Compared to what you do inside a virtual call, the extra dereference
required seems petty and very likely not to have any noticeable side
effects other than dereference and the extra space taken up by the
virtual table pointer. The extra dereference before getting the pointer
to the function we want to call on this particular instance seems to be
a trivial addition, but lets have a closer look at what is going on.

Firstly, we have a pointer to a class that has derived from a base class
with virtual methods. This instantly adds the virtual table pointer as
the implicit first data member of the class. Obviously, there is no way
around this, it’s in the language specification that the data layout be
partially up to the compiler so it can implement such things as virtual
methods by adding hidden members and generating new arrays of function
pointers behind the scenes. If we try to call a virtual method on the
class we have to read the first data member in order to access the right
virtual table for calling. This requires loading from the address of the
class into a register and adding an offset to the loaded value. Every
virtual method call is a lookup into a table, so in the compiled code,
all virtual calls are really function pointer array dereferences, which
is where the offset comes in. It’s the offset into the array of function
pointers. Once the address of the real function pointer is generated, it
is loaded into a register, then used to chance the program counter, via
a branch instruction.

For multiple inheritance it is slightly more convoluted.

So let’s count up the actual operations involved in this method call:
first we have a load, then an add, then another load, then a branch. To
almost all programmers this doesn’t seem like a heavy cost to pay for
runtime polymorphism. Four operations per call so that you can throw all
your game entities into one array and loop through them updating,
rendering, gathering collision state, spawning off sound effects. This
seems to be a good trade off, but it was only a good trade off when
these particular instructions were cheap.

Two out of the four instructions are loads, which don’t seem like they
should cost much, but in actual fact, unless you hit the cache, a load
takes around 600 cycles on modern consoles. The add is cheap, to modify
the register value to address the correct function pointer, but the
branch is not always cheap as it doesn’t know where it’s going until the
second load completes. This could cause cache miss in the instructions.
All in all, it’s common to see around 1800 cycles wasted due to a single
virtual call in any significantly large scale game. In 1800 cycles, the
floating point unit alone could have finished naively calculating over
fifty dot products, or up to 27 square roots. In the best case, the
virtual table pointer will already be in memory, the object type the
same as last time, so the function pointer address will be the same, and
therefore the function pointer will be in cache too, and in that
circumstance it’s likely that the unconditional branch won’t stall as
the instructions are probably still in the cache too. But this best case
is fairly uncommon.

The implementation of C++ doesn’t like how we iterate over objects. The
standard way of iterating over a set of heterogeneous objects is to
literally do that, grab an iterator and call the virtual function on
each object in turn. In normal game code, this will involve loading the
virtual table pointer for each and every object. This causes a wait
while loading the cache line, and cannot easily be avoided. Once the
virtual table pointer is loaded, it can be used, with the constant
offset (the index of the virtual method), to find the function pointer
to call, however due to the size of virtual functions commonly found in
games development, the table won’t be in the cache. Naturally, this will
cause another wait for load, and once this load has finished, we can
only hope that the object is actually the same type as the previous
element, otherwise we will have to wait some more for the instructions
to load.

The reason virtual functions in games are large is that games developers
have had it drilled into them that virtual functions are okay, as long
as you don’t use them in tight loops, which invariably leads to them
being used for more architectural considerations such as hierarchies of
object types, or classes of solution helpers in tree like problem
solving systems (such as path finding, or behaviour trees).

In C++, classes’ virtual tables store function pointers by their class.
The alternative is to have a virtual table for each function and switch
function pointer on the type of the calling class. This works fine in
practice and does save some of the overhead as the virtual table would
be the same for all the calls in a single iteration of a group of
objects. However, C++ was designed to allow for runtime linking to other
libraries, libraries with new classes that may inherit from the existing
codebase, and due to this, there had to be a way to allow a runtime
linked class to add new virtual methods, and have them able to be called
from the original running code. If C++ had gone with function oriented
virtual tables, the language would have had to runtime patch the virtual
tables whenever a new library was linked whether at link time for
statically compiled additions, or at runtime for dynamically linked
libraries. As it is, using a virtual table per class offers the same
functionality but doesn’t require any link time or runtime modification
to the virtual tables as the tables are oriented by the classes, which
by the language design are immutable during link time.

Combining the organisation of virtual tables and the order in which
games tend to call methods, even when running through lists in a highly
predictable manner, cache misses are commonplace. It’s not just the
implementation of classes that causes these cache misses, it’s any time
the instructions to run are controlled by data loaded. Games commonly
implement scripting languages, and these languages are often interpreted
and run on a virtual machine. However the virtual machine or JIT
compiler is implemented, there is always an aspect of data controlling
which instructions will be called next, and this causes branch
misprediction. This is why, in general, interpreted languages are
slower, they either run code based on loaded data in the case of
bytecode interpreters, or they compile code just in time, which though
it creates faster code, causes cache misses and thrashing of its own.

When a developers implements and Object-oriented framework without using
the built-in virtual functions, virtual tables and this pointers present
in the C++ langauge, it doesn’t reduce the chance of cache miss unless
they use virtual tables by function rather than by class. But even when
the developer has been especially careful, the very fact that they are
doing Object-oriented programming with games developer access patterns,
that of calling single functions on arrays of heterogeneous objects,
they are still going to have the same cache misses as found when the
virtual table has survived the call into the object. That is, the best
they can hope for is one less cache miss per virtual call. That still
leaves the opportunity for two cache misses, and an unconditional
branch.

So, with all this apparent inefficiency, what makes games developers
stick with Object-oriented coding practices? As games developers are
frequently cited as a source of how the bleeding edge of computer
software development is progressing, why have they not moved away
wholesale from the problem and stopped using Object-oriented development
practices all together?

