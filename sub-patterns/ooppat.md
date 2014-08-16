Existing design patterns
------------------------

Most of the Object-oriented design patterns aren’t necessary in
data-oriented development, but explaining why can be useful for
migrating from the object-oriented way of working. Even though design
patterns are founded in the world of object-oriented development, some
design patterns have mirrors in the data-oriented world. Sometimes this
is because the functionality is incredibly simple (such as with the
factory), or because the design pattern is emulated by basic
functionality of the data-oriented technique (such as flyweight).

### Abstract Factories

The requirement for abstract factories comes from needing to generate
new objects based on an overall scheme. This means creation can now be
dependent on two data values: the first is the scheme, the second is the
type requested for creation. This inherently object-oriented design
problem stems from the desire to reuse code to drive object creation,
but as C++ stops you from using objects by their features unless already
declared in some way, it is hard to retroactively apply old creation
techniques to new types. Normally we set up our classes by inheriting
from an abstract base class so we can later provide new classes under
new creation objects. The abstract factory is the eventual extension of
allowing the creation function to be chosen at runtime based on the type
of object required (which is statically checked) and the scheme or style
of the object (which is dynamically calculated by the abstract factory),
so choosing the right concrete factory object to create your new object.

When writing component entity systems, this is the equivalent of having
components being inserted into an entity based on two dimensional data.
The fact that a component of a certain type needs creating (the create
call) is emulated by the row in the component create table, and the
abstract factory calling into a concrete factory is emulated by the
value causing the create call to be dispatched to an appropriate final
factory table. Only once it has been dispatched to the right table does
it get inserted into the final concrete component table.

This pattern is useful for multi-platform object-oriented development
where you might have to otherwise refactor the internals of your object
creators, but with a component driven approach, you can switch your
output tables, transforms, or complete tree of transforms without losing
consistency where it is necessary.

### Builder

The builder pattern is all about wrapping up collections of reusable
low-level parts of a complex transform in order to provide a tool kit
for macro scale programming within a problem domain. The builder pattern
is used when you want to be able to switch which tool-kits are used,
thus providing a way of giving a high level program the ability to
direct the creation of objects through the interface of a collection of
tools.

This can be seen to parallel the tool-kit of transforms you tend to
build when developing with tables. With a data-oriented functional
programming approach, we don’t immediately call builders, but instead
generate the necessary build instructions that can then dispatched to
the correct parallel processes where possible before being reduced into
the final data. Usually the builders are stateless transforms that
convert the request to build into data outputs, or take a small amount
of input data and build it into larger or translated output.

Once you work out that the builder pattern is mostly a rewording of
procedural reuse with the addition of switching which procedures are
called based on a state in a larger scope, it is easy to see why the
pattern is applicable in all programming paradigms.

### Factory Method

The factory method allows for data controlled choice of what is created.
This is mirrored well in the component driven programming model, as all
components are created via predictably called functions, but whether
they are called is down to the data. Rather than a method, we use
creation tables. Instances of entities and components are created when
the system gets around to updating those tables. The creation request
table contains the same arguments as the factory method, so the type and
its arguments are used in that table update to cause an insert into the
component or entity table. There is never any in-place creation, as
there is never any need of it. Anything too complex to create as part of
the output from a single transform deserves the attention of an explicit
creation, and also will find it hard to mitigate the cost of creation
out of the order of normal object creation, so will be less tempted to
trash the instruction cache or derail the flow of the game for a special
case like we find frequently in object-oriented development.

### Prototype

The prototype pattern makes a lot of sense in an object-oriented code
base, as the ability to generate more class instances from another
class, only to modify it slightly before releasing it as finished almost
gives you the flexibility to generate new classes at run-time, but any
flexibility still has to be built into the classes before they can be
used as the classes can only inherit from types existing at compile
time. Some Object-oriented languages do let you generate new features at
run-time but C++ doesn’t allow for it without considerable coercion.

The existence-based-processing way of working stops you from creating a
prototype as its existence would imply that it is in the game. There is
no place to hide a prototype. But, there is also little call for it as
creating a prototype is about creating from a plan of sorts, and because
all the component creation can be controlled via read-only or
just-in-time mementos, its very easy to make new classes with their
components defined and specialised without resorting to hacks like
keeping in memory a runtime template for a class you might need later.
Unlike the object-oriented prototype, the component system memento does
not have all the feature of the final component set, it only has the
features of a creation data-type and thus fit’s its purpose more purely.
It cannot accidentally be used and damaged in the way prototypes can,
for example, prototypes can be damaged by global update functions that
accidentally modified the state. Because the only difference between a
prototype and the runtime instance is whether the program knows that
they are prototypes, it’s hard to secure them against unwanted messages.

### Singleton

There is no reason to think that a single instance of a piece of data
has any place in a data-oriented development. If the data is definitely
unique, then it deserves to be exposed as a system wide global. It is
only when globals are used for temporary store that they become
dangerous. Singletons are an inherently object-oriented solution to a
problem that only persists if you truly want to write platform ignorant
code. Initialising and deinitialising managers in specific order for
component managers, or for hardware or dependency sake can just as
easily be managed explicitly, and is less prone to surprising someone.
When you change the initialisation order accidentally by referencing a
singleton, that reference won’t be seen as changing the order of
initialisation and it has been seen to cause quite difficult to debug
when the effect of the change in order is subtle enough to not crash
immediately.

### Adapter

An adapter provides an API wrapper around an otherwise incompatible
class. Classes have their APIs locked down after they are created. If
two classes that need to work with each other come from third party
software libraries, the likelihood of them being naturally compatible is
low to non-existent. An adapter wraps the callee class in a caller
friendly API. The adapter turns the caller class friendly API calls into
callee class friendly API calls.

When writing programs data-oriented, most data is structs of arrays or
tables. In data-oriented development there is no reason for an adapter,
as in the first case, a transform can easily be made to take arguments
of the specific arrays used, and in the second case, the transform would
normally take two or more schema iterators that traversed the table
providing arguments to and capturing outputs from the transform. In a
sense, every table transform iterator is an adapter because it converts
the explicit form of the table into the explicit form accepted by the
transform.

Finally, data itself has no API, and thus the idea of an adapter is not
appropriate as there is nothing to adapt from, so this relegates the
idea to the concept of transforming the data so it can be provided to
third party libraries. Preparing data for external processes is part of
working with other code, and is one of the prices you pay for not having
full control of the source code. The adapter pattern doesn’t help this
in any way, only provides a way of describing the inevitable.

### Bridge

The bridge pattern is an object-oriented technique for providing
encapsulation from implementation when the class’s implementation is the
functionality that derived classes use to get by in their world. For
example, the platform specific code for an object can be privately owned
by the parent class, and the concrete class can derive from that class.
Then, it can use the implementation of it’s parent class, but the
implementation of the parent class member functions can be indirectly
implemented differently depending on the platform. This way, the child
class can call its parent’s functions to do what it needs to do, while
the parent class can call the implementation’s functions which can be
defined at runtime or compile time depending on what level of
polymorphism is required.

Because all platform specific functionality is defined inside transforms
and the way in which they are called, there is no reason to consider
this pattern for platform independent reasons. All that is needed to
benefit from the side effect of using this pattern is to recognise the
boundary between platform specific transforms and platform independent
transforms. For situations where the parent class implementation differs
from instance to instance, you only need to notice that components can
be different, yet still register with the same events. This means, any
differing implementations required can be added as additional components
which register into the same event tables as the existing components and
replace those on creation as part of the different creation sequence.

Also, transforms that take data and do with it something platform
specific would be written statically for each platform. This kind of
object-oriented approach to everything can be what gives object-oriented
development such a bad name when it comes to performance. There’s not
really any benefit to making your choice of implementation a runtime
polymorphic call when the call can only ever be to one concrete method
per platform as, at least in C++, there is not such thing as platform
independent builds. For C\#, it can be different, but the benefit of
doing it is just the same, you only benefit very slightly when it comes
to readability in the code, but you lose on every call at runtime.

### Composite

Unlike it’s programming namesake, the composite pattern is not about an
object being made out of multiple other classes by owning them in the
implementation. The composite pattern is the idea that an object that is
part of a system can be identified as a single object, or as a group of
objects. Usually, a game entity references one renderable unit with a
single AI instance, which is why this pattern can be useful. If an enemy
unit class can represent a single unit, or a squad of units, then it
becomes easier to manage commands in a real time strategy game, or
organise AI path finding.

When you don’t use objects, the level of detail of individual parts of
entities are not so hard tied to each other as the entities are not
objects. When you design your software around objects you get caught up
thinking about each object as being indivisible, and thus the composite
pattern lets you at least handle objects in groups. If you don’t limit
your data by tying it to objects, then the pattern is less useful as you
can already manipulate the data by group in any way you require.

### Decorator

The decorator acts much like adding more components to an entity. Their
effect comes online when their existence marks their necessity.
Decorators add features, which is exactly like the entity components
with their ability to add attributes and functionality to a referenced
entity.

### Façade

Even though there are no tangled messes of interacting objects in the
data-oriented approach, sometimes it might be better to channel data
through a simpler set of streams. This could be considered to offer the
same smaller surface area that the façade offers.

### Flyweight

The flyweight pattern offers a way to use very fine grain elements in
the same way it uses larger constructs. In data-oriented development
there is no need to differentiate between the two, as there is no
inherent overhead in interfacing data in a data-oriented manner. The
reason for a flyweight is similar to the reason for the bridge pattern,
once you start thinking object-oriented and want to keep your whole
codebase working like that, you can end up painting yourself into a
corner about it and start adding objects to everything, even things that
are too small or fragile for such a heavy handed, human centric way of
seeing and manipulating the data.

### Proxy

In a sense, the proxy pattern is much like the level of detail system in
most games. You don’t load final assets until you are near enough to
need them. This topic was fully covered in chapter [chap:hier].

### Chain Of Responsibility

The only problem with the chain of responsibility is that in most
implementations it is inherently serial for all the possible recipients
interested in responding to it. If we remove the possibility of the
event being marked as handled, then the pattern is better handled
through existence based processing than through object-oriented design,
as existence-based-processing offers a way to subscribe at multiple
points in the same entity with different components wanting to respond
to different parts of a new event. If you want to enable such things as
marking as handled, then it might be better to have a responsibility
table for each message or event type with a dispatcher heading off the
message before it hits the general message queue.

### Command

This is realised fully when using tables to initiate your actions. All
actions have to exist as a row in a table at some point, usually as a
condition table row in the first place.

### Interpreter

This design pattern doesn’t seem very well suited to Object-oriented
programming at all, though it is rooted in data driven flow control. The
problem with the interpreter is it seems to be the design pattern for
parsers, but doesn’t add anything in itself.

### Iterator

Although the table iterators that convert table schema into transform
arguments are iterators, they don’t fit into the design pattern because
they are a concrete solution to iterating over tables. There is no scope
for using them for arguments to functions or using them to erase
elements and continue, they are stateful, but restricted to their one
job. However, because there are no containers in table oriented
solutions other than the tables, we can safely ignore true iterators as
a design. In a stream based development, iterators are so common and
pure, they don’t really exist in the design pattern sense.

### Mediator

The mediator can be thought of as a set up involving attaching event
transforms to table updates. When a table entry updates, the callback
can then inform the other related tables that they need to consider some
new information. However, this data hiding and decoupling is not as
necessary in data-oriented development as most solutions are considering
all the data and thus don’t need to be decoupled at this level.

### Memento

Stashing a compressed state in a table is very useful when changing
level of detail. Much was made of this in count lodding. Mementos also
provide a mechanism for undoing changes, which can be essential to low
memory usage network state prediction systems, so they can rollback
update, and fast forward to the new predicted state.

### Null Object

A null object is a pattern to stop unnecessary branching and checking
when a fetch operation returns a class instance. If the instance was
null, then returning the null object allows the calling code to continue
on as if it had received a valid object. This is unnecessary in table
driven processing scenarios as the transforms run over data. There is no
chance for a transform to run into a null pointer as pointers are banned
in general.

### Observer

The publish and subscribe model presented in the table based event
system is an observer pattern and should be used whenever data relies on
some other data. The observer patter is high latency, but provides for
callbacks, event handling, and job starting. In most games there will be
an observer registry for the frame sync, the physics tick, the AI tick
and for any IO completion. User defined callback tables will be
everywhere, including how many finite state machines are implemented.

### State

Data controlling the flow of the program is considered an anti-pattern
in data-oriented development, so this design pattern is to be
understood, and never used in the way it is presented. Instead, have
your state be implicitly defined by the table in which your entity
resides. Using table existince to drive the transform that is called is
the basis of finite state machine update, if not the alphabet response.

This design pattern is highly dangerous for any game that wants to run
at high speed with a high entity count.

### Strategy

### Template Method

The template method can still be used but overriding the calls by
removing the template callbacks and adding the specific new callbacks
would be how you organise the equivalent of overriding the virtual
calls.

### Visitor

The visitor pattern would be fine if it were not for the implicit
allowance for it to be stateful. If the visitor was not allowed to
accumulate during it’s structure traversal, then it would be an in-place
transform. By not defining it as a stateless entity, but a stateful
object that walks the container, it becomes an inherently serial, cache
unfriendly container analyser. This pattern in particular is quoted by
people who don’t understand the fundamental requirements of a transform
function. If you talk to an Object-Oriented programmer about taking a
list of data and doing a transform on it, they will tend to mention it
as the visitor patter because there is a tendency to fit solutions to
problems with design patterns. The best way to define a visitor pattern
is an object that changes state based on the incoming data. The final
state is dependent on the order in which the data is given to the
visitor, thus it is a serial operation. The best analogy to a transform
is not compatible with a visitor because a transform pattern denies the
possibility of accumulation.

