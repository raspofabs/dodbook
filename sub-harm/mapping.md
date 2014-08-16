Mapping the problem
-------------------

*Objects provide a better mapping from the real world description of the
problem to the final code solution.*\

Object-oriented design when programming in games starts with thinking
about the game design in terms of entities. Each entity in the game
design is given a class, such as ship, player, bullet, or score. Each
object maintains its own state, communicates with other objects through
methods, and provides encapsulation so when the implementation of a
particular entity changes, the other objects that use it or provide it
with utility do not need to change. Games developers like abstraction as
historically, they have had to write games for not just one target
platform, but usually at least two. In the past it was between console
manufacturers, and now even games developers on the PC have to manage
both Windows(tm) and MacOS(tm) platforms. The abstractions in the past
were mostly hardware access abstractions, and naturally some gameplay
abstractions as well, but as the game development industry matured, we
found common forms of abstractions for areas such as physics, AI, and
even player control. Finding these common abstractions allowed for third
party libraries, and many of these use Object-oriented design as well.
It’s quite common for libraries to interact with the game through
agents. These agent objects contain their own state data, whether hidden
or publicly accessible, and provide functions by which they can be
manipulated inside the constraints of the system that provided them. The
game design inspired objects (such as ship, player, level) keep hold of
agents and use them to find out what’s going on in their world. A player
object might use their physics agent to find out where they are going to
be, and what is possible given where they are, and using their input
agent, find out the player’s intention, and in return providing some
feedback to their physics agent about the forces, and information to
their animation agent about what animations they need to play. A
non-player character could mediate between the world physics agent and
its AI agent. A car object could contain references to physics data for
keeping it on the road, and also runtime modifiable rendering
information can be chained to the collision system to show scratches and
worse.

The entities in Object-oriented design are containers for data and a
place to keep all the functions that manipulate that data. Don’t confuse
these entities with those of entity systems, as the entities in
Object-oriented design are immutable over their lifetime. An
Object-oriented entity does not change class during its lifetime in C++
because there is no process by which to reconstruct a class in place in
the language. As can be expected, if you don’t have the right tools for
the job, a good workman works around it. Games developers don’t change
the type of their objects at runtime, instead they create new and
destroy old in the case of a game entity that needs this functionality.

For example, in a first person shooter, an object will be declared to
represent the animating player mesh, but when the player dies, a clone
would be made to represent the dead body as a rag doll. The animating
player object is made invisible and moved to their next spawn point
while the dead body object with its different set of virtual functions,
and different data, remains where the player died so as to let the
player watch their dead body. To achieve this sleight of hand, where the
dead body object sits in as a replacement for the player once they are
dead, copy constructors need to be defined. When the player is spawned
back into the game, the player model will be made visible again, and if
they wish to, the player can go and visit their dead clone. This works
remarkably well, but it is a trick that would be unnecessary if the
player could become a dead rag doll rather than spawn a clone of a
different type. There is inherent danger in this too, that the cloning
could have bugs, and cause other issues, and also that if the player
dies but somehow is allowed to resurrect, then they have to find a way
to convert the rag doll back into the animating player, and that is no
simple feat.

Another example is in AI. The finite state machines that run most game
AI maintain all the data necessary for all their potential states. If an
AI has three states, { Idle, Making-a-stand, Fleeing-in-terror } then it
has the data for all three states. If the Making-a-stand has a
scared-points accumulator for accounting their fear, so that they can
fight, but only up until they are too scared to continue, and the
Fleeing-in-terror has a timer so that they will flee, but only for a
certain time, then Idle will have these two unnecessary attributes as
well. In this trivial example, the AI class has three data entries, {
state, how-scared, flee-time }, and only one of these data entries is
used by all three states. If the AI could change type when it
transitioned from state to state, then it wouldn’t even need the state
member, as that functionality would be covered by the virtual table
pointer. The AI would only allocate space for each of the state tracking
members when in the appropriate state. The best we can do in C++ is to
fake it by changing the virtual table pointer by hand, or setting up a
copy constructor for each possible transition.

This implementation detail does not cost much, can be worked around, but
when it does, it bends if not breaks the standard way of doing
Object-oriented development in C++.

Apart from immutable type, Object-oriented development also has a
philosophical problem. Consider how humans perceive objects in real
life. There is always a context to every observation. The humble table,
when you look at it, you may see it to be a table with four legs, made
of wood and modestly polished. If so, you will see it as being a brown
colour, but you will also see the reflection of the light. You will see
the grain, but when you think about what colour it is, you will think of
it as being one colour. However, if you have the training of an artist,
you will know that what you see is not what is actually there. There is
no solid colour, and if you are looking at the table, you cannot see its
precise shape, but only infer it. If you are inferring that it is brown
by the average light colour entering your eye, then does it cease to be
brown if you turn off the light? What about if there is too much light
and all you can see is the reflection off the polished surface? If you
look at its rectangular form from one of the long sides, then you will
not see right angle corners, but instead a trapezium. We automatically
classify objects when we see them, apply our prejudices to them and lock
them down to make reasoning about them easier. This is why
Object-oriented development is so appealing to us. However, what we find
easy to consume as humans, is not optimal for a computer. When we think
about game entities being objects, we think about them as wholes. But a
computer has no concept of objects, and only sees objects as being badly
organised data and functions organised for maximal cache abuse.

If you take another example from the table, consider the table to have
legs about three feet long. That’s a standard table. If the legs are
only one foot long, it could be considered to be a coffee table. Short,
but still usable as a place to throw the magazines and leave your cups.
But when you get down to one inch long legs, it’s no longer a table, but
instead just a large piece of wood with some stubs stuck on it. We can
happily classify the same item but with different dimensions into three
distinct classes of object. Table, coffee table, lump of wood with some
little bits of wood on it. But, at what point does the lump of wood
become a coffee table? Is it somewhere between 4 and 8 inch long legs?
This is the same problem as presented about sand, when does it
transition from grains of sand, to a pile of sand? How many grains are a
pile, are a dune? The answer must be that there is no answer. The answer
is also helpful in understanding how a computer thinks. It doesn’t know
the specific difference between our human classifications because to a
certain degree even humans don’t.

In most games engines, the Object-oriented approach leads to a lot of
objects in very deep hierarchies. A common ancestor chain for an entity
might be: PlayerEntity $\rightarrow$ CharacterEntity $\rightarrow$
MovingEntity $\rightarrow$ PhysicalEntity $\rightarrow$ Entity
$\rightarrow$ Serialisable $\rightarrow$ ReferenceCounted $\rightarrow$
Base.

These deep hierarchies virtually guarantee you’ll never have a cache hit
when calling virtual methods, but they also cause a lot of pain when it
comes to cross-cutting code, that is code that affects or is affected by
concerns that are unrelated, or incongruous to the hierarchy. Consider a
normal game with characters moving around a scene. In the scene you will
have characters, the world, possibly some particle effects, lights, some
static and some dynamic. In this scene, all these things need to be
rendered, or used for rendering. The traditional approach is to use
multiple inheritance or to make sure that there is a Renderable base
class somewhere in every entity’s inheritance chain. But what about
entities that make noises? Do you add an audio emitter class as well?
What about entities that are serialised vs those that are explicitly
managed by the level? What about those that are so common that they need
a different memory manager (such as the particles), or those that only
optionally have to be rendered (like trash, flowers, or grass in the
distance). Traditionally this has been solved by putting all the most
common functionality into the core base class for everything in the
game, with special exceptions for special circumstances, such as when
the level is animated, when a player character is in an intro or death
screen, or is a boss character (who is special and deserves a little
more code). These hacks are only necessary if you don’t use multiple
inheritance, but when you use multiple inheritance you then start to
weave a web that could ultimately end up with virtual inheritance, and
that can cause some serious performance overhead as it has to figure out
a lot more than just where the virtual table is. The compromise almost
always turns out to be some form of cosmic base class anti-pattern.

Object-oriented development is good at providing a human oriented
representation of the problem in the source code, but bad at providing a
machine representation of the solution. It is bad at providing a
framework for creating an optimal solution, so the question remains: why
are games developers still using Object-oriented techniques to develop
games? It’s possible its not about better design, but instead about make
it easier to change the code. It’s common knowledge that games
developers are constantly changing code to match the natural evolution
of the design of the game, right up until launch. Does Object-oriented
development provide a good way of making maintenance and modification
simpler or safer?

