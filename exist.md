Existence Based Processing
==========================

If you saw that there weren’t any apples in stock, would you still
haggle over their price?

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

Don’t use booleans {#sec:exist-bool}
------------------

When you study compression technology, one of the most important aspects
you have to understand is the different between data and information.
There are many ways to store information in systems, from literal
strings that can be parsed to declare that something exists, right down
to something simple like a single bit flag to show that a thing might
have an attributes. Examples include the text that declares the
existence of a local variable in a scripting language, or the bit field
that contains all the different collision types a physics mesh will
respond to. Sometimes we can store even less information than a bit by
using advanced algorithms such as arithmetic encoding, or by utilising
domain knowledge. Domain knowledge normalisation applies in most games
development, but it is very infrequently applied. As information is
encoded in data, and the amount of information encoded can be amplified
by domain knowledge, it’s important that we begin to see the advice
offered by compression techniques is that: all we are really encoding is
probabilities.

If we take an example, a game where the entities have health, regenerate
after a while of not taking damage, can die, can shoot each other, then
lets see what domain knowledge can do to reduce processing.

We assume this domain knowledge: if you have full health, then you don’t
need to regenerate. Once you have been shot, it takes some time until
you begin regenerating. Once you are dead, you cannot regenerate. Once
you are dead you have zero health.

If we have a table for the entity thus:

~~~~ {caption="naive" entity="" table=""}
struct entity {
    // information about the entity position
    // ...
    // now health data in the middle of the entity
    float timeoflastdamage;
    float health;
    // ...
    // other entity information
};
list<entity> entities;
~~~~

Then we can run an update function over the table that might look like
this:

~~~~ {caption="every" entity="" health="" regen=""}
void updatehealth( entity *e ) {
    timetype timesincelastshot = e->timeoflastdamage - currenttime;
    bool ishurt = e->health < max_health && e->health > 0;
    bool regencanstart = timesincelastshot > time_before_regenerating;
    if( ishurt && regencanstart ) {
        e->health = min(max_health, e->health + ticktime * regenrate);
    }
}
~~~~

Which will run for every entity in the game, every update.

We can make this better by looking at the flow control statement. The
function only needs to run if the health is less than full health, and
more than zero. The regenerate function only needs to run if it has been
long enough since the last damage dealt.

Let’s change the structures:

~~~~ {caption="existence" based="" processing="" style="" health=""}
struct entity {
    // information about the entity position
    // ...
    // other entity information
};
struct entitydamage {
    float timeoflastdamage;
    float health;
}
list<entity> entities;
map<entityref,entitydamage> entitydamages;
~~~~

We can now run the update function over the health table rather than the
entities.

~~~~ {caption="every" entity="" health="" regen=""}
void updatehealth() {
    foreach( eh in entitydamages ) {
        entityref entity = eh->first;
        entitydamage &ed = eh->second;
        if( ed.health < 0 ) {
            deadentities.insert( entity );
            discard(eh);
        } else {
            timetype timesincelastshot = eh->timeoflastshot - currenttime;
            bool regencanstart = timesincelastshot > time_before_regenerating;
            if( regencanstart )
                eh->health =eh->health + ticktime * regenrate;
            if( eh->health > max_health )
                discard(eh);
        }
    }
}
~~~~

We only add a new entityhealth element when an entity takes damage. If
an entity takes damage when it already has an entityhealth element, then
it can update the health rather than create a new row, also updating the
time damage was last dealt. If you want to find out someone’s health,
then you only need to look and see if they have an entityhealth row, or
if they have a row in deadentities table. The reason this works is that
an entity has an implicit boolean hidden in the row existing in the
table. For the entityhealth table, that implicit boolean was ishurt from
the first function. For the deadentities table, the implicit boolean of
isdead, also implies a health value of 0, which can reduce processing
for many other systems. If you don’t have to load a float and check that
it is less than 0, then you’re saving a floating point comparison or
conversion to boolean.

Other similar cases include weapon reloading, oxygen levels when
swimming, anything that has a value that runs out, has a maximum, or has
a minimum. Even things like driving speeds of cars. If they are traffic,
then they will spend most of their time driving at <span>*traffic
speed*</span> not some speed that they need to calculate. If you have a
group of people all heading in the same direction, then someone joining
the group can be <span>*intercepting*</span> until they manage to, at
which point they can give up their self and become controlled by the
group.

As an aside, we use a map and a list here for simplicity of reading, and
though they are not the most optimal containers in that they are trees,
or pointers to elements, rather than a nice contiguous array of some
sort, they’re not going to adversely affect the profile as much as the
problem being overcome here, namely the mixing of hot[^1] data into the
middle of the entity class.

Another example is with AI. If you have all your entities maintain a
team index, then you have to check each entity before reacting to them.
If you want to avoid all the entities from team x, and head towards the
closest member of team y, then if each team is in a different table you
can just operate on all the entities in those tables. If you want to
produce an avoidance vector from team x, you create a mapreduce function
that maps team x members to an avoidance vector, then reduce by summing.

~~~~ {caption="map" and="" reduce=""}
vector mapavoidance( entity *e ) {
    vector difference = e->pos - currentpos;
    float oneoversqr = 1.0f / difference.getsquaredlength();
    return difference * oneoversqr;
}
vector reduceavoidance( const vector l, const vector r ) {
    return l + r;
}
pair<float,entity*> mapnearest( entity *e ) {
    vector difference = e->pos - currentpos;
    float squaredistance = difference.getsquaredlength();
    return pair<float,entity*>( squaredistance, e );
}
pair<float,entity*> reducenearest( pair<float,entity*> l, pair<float,entity*> r ) {
    if( l.left < r.left ) return l; return r;
}
~~~~

The implicit boolean in these tables is that they are worth avoiding,
and that they are worth aiming towards. If nothing maps, then the
seeding value to the reduce is returned.

Another use is in state management. If an AI hears gunfire, then they
can add a row to a table for when they last heard gunfire, and that can
be used to determine whether they are in a heightened state of
awareness. If an AI has been involved in a transaction with the player,
it is important that they remember what has happened as long as the
player is likely to remember it. If the player has just sold an AI their
+5 longsword, it’s very important that the shopkeeper AI still have it
in stock if the player just pops out of the shop for a moment. Some
games don’t even keep inventory between transactions, and that can
become a sore point if they accidentally sell something they need and
then save their progress.

The general concept of tacking on data, or patching loaded data with
dynamic additional attributes, has been around for quite a while. Save
games often encode the state of a dynamic world as a delta from the base
state, and one of the first major uses was in fully dynamic
environments, where a world is loaded, but can be destroyed or altered
afterwards. Some world generators took a procedural landscape and
allowed their content creators to add patches of extra information,
villages, forts, outposts, or even break out landscaping tools to
drastically adjust the generated data. Taking that patching and applying
it to in-game runtime information adds a level of control not normally
available without using intrusive techniques.

Don’t use enums {#sec:exist-enum}
---------------

Enumerations are used to define sets of states. We could have had a
state variable for the regenerating entity, one that had infullhealth,
ishurt, isdead as its three states. We could have had a team index
variable for the avoidance entity enumerating all the available teams.
Instead we used tables to provide all the information we needed. Any
enum can be emulated with a variety of tables. All you need is one table
per enumerable value. Setting the enumeration is an insert into a table.

When using tables to replace enums, some things become more difficult:
finding out the value of an enum in an entity is difficult as it
requires checking all the tables that represent that state for the
entity. However, this is mostly disallowed and unnecessary, as the main
reason for getting the value is either to do an operation based on the
state, or to find out if an entity is in the right state to be
considered for an operation.

If the enum is a state or type enum previously handled by a switch or
virtual call, then we don’t need to look up the value, instead we change
the way we think about the problem. The solution is to run transforms
taking the content of each of the switch cases or virtual methods as the
operation to apply to the appropriate table, the table corresponding to
the original enumeration value.

If the enum is instead used to determine whether or not an entity can be
operated upon, then you can operate on all the entities in the
appropriate table. Transforming the whole table or the join of that
table with some other condition. If you’re thinking about the case where
you have an entity as the result of a query and need to know if it is in
a certain state before deciding commit some change, consider that the
table you need access to could have been one of the initial mappings,
meaning that no entity would be found that didn’t match the enum
replacing table in the way you needed it to.

Prelude to polymorphism {#sec:exist-prelpoly}
-----------------------

Let’s consider now how we implement polymorphism. We know we don’t have
to use a virtual table pointer; we could use an enum as a type variable.
That variable, the member of the structure that defines at runtime what
that structure should be capable of and how it is meant to react. That
variable could be used to direct the choice of functions called when
methods are called on the object.

When your type is defined by a member type variable, it’s usual to
implement virtual functions as switches based on that type, or as an
array of functions. If we want to allow for runtime loaded libraries,
then we would need a system to update which functions are called. The
humble switch is unable to accommodate this, but the array of functions
could be modified at runtime.

We have a solution, but it’s not elegant, or efficient. The data is
still in charge of the instructions, and we suffer the same instruction
cache hit whenever a virtual function is unexpected. However, when we
don’t really use enums, but instead tables that represent each possible
value of an enum, it is still possible to keep compatible with dynamic
library loading the same as with pointer based polymorphism, but we also
gain the efficiency of a data-flow processing approach to processing
heterogeneous types.

For each class, instead of a class declaration, we have a factory that
produces the correct selection of table insert calls. Instead of a
polymorphic method call, we utilise existence based processing. Our
elements in a tables allow the characteristics of the class to be
implicit. Creating your classes with factories can easily be extended by
runtime loaded libraries. Registering a new factory should be simple as
long as there is a data driven factory method. The processing tables and
their `update()` functions would also be added to the main loop.

Dynamic runtime polymorphism {#sec:exist-poly}
----------------------------

If you create your classes by composition, and you allow the state to
change by inserting and removing from tables, then you also allow
yourself access to dynamic runtime polymorphism.

Polymorphism is the ability for an instance in a program to react to a
common entry point in different ways due only to the nature of the
instance. In C++, compile time polymorphism can be implemented through
templates and overloading. Runtime polymorphism is the ability for a
class to provide a different implementation for a common base operation
with the class type unknown at compile time. C++ handles this through
virtual tables, calling the right function at runtime based on the type
hidden in the virtual table pointer at the start of the memory pointed
to by the this pointer. Dynamic runtime polymorphism is when a class can
react differently to a common call signature in different ways based on
both it’s type and any other internal state. C++ doesn’t implement this
explicitly, but if a class allows the use of an internal state variable
or variables, it can provide differing reactions based on that state as
well as the core language runtime virtual table lookup. Consider the
following code:

    class shape {
    public:
        shape() {}
        virtual ~shape() {}
        virtual float getarea() const = 0;
    };
    class circle : public shape {
    public:
        circle( float diameter ) : d(diameter ) {}
        ~circle() {}
        float getarea() const { return d*d*pi/4; }
        float d;
    };
    class square : public shape {
    public:
        square( float across ) : width( across ) {}
        ~square() {}
        float getarea() const { return width*width; }
        float width;
    };
    void test() {
        circle circle( 2.5f );
        square square( 5.0f );
        shape *shape1 = &circle, *shape2 = &square;
        printf( "areas are %f and %f\n", shape1->getarea(), shape2->getarea() );
    }

Allowing the objects to change shape during their lifetime requires some
compromise in C++ one way is to keep a type variable inside the class.

~~~~ {caption="ugly" internal="" type="" code=""}
enum shapetype { circletype, squaretype };
class mutableshape {
public:
    mutableshape( shapetype type, float argument )
        : m_type( type ), distanceacross( argument )
        {}
    ~mutableshape() {}
    float getarea() const {
        switch( m_type ) {
            case circletype: return distanceacross*distanceacross*pi/4;
            case squaretype: return distanceacross*distanceacross;
        }
    }
    void setnewtype( shapetype type ) {
        m_type = type;
    }
    shapetype m_type;
    float distanceacross;
};
void testinternaltype() {
    mutableshape shape1( circletype, 5.0f );
    mutableshape shape2( circletype, 5.0f );
    shape2.setnewtype( squaretype );
    printf( "areas are %f and %f\n", shape1.getarea(), shape2.getarea() );
}
~~~~

A better way is to have a conversion function to handle each case.

~~~~ {caption="convert" existing="" class="" to="" new="" class=""}
square squarethecircle( const circle &circle ) {
    return square( circle.d );
}
void testconvertintype() {
    circle circle( 5.0f );
    square square = squarethecircle( circle );
}
~~~~

Though this works, all the pointers to the old class are now invalid.
Using handles would mitigate these worries, but add another layer of
indirection in most cases, dragging down performance even more.

If you use existence-based-processing techniques, your classes defined
by the tables they belong to, then you can switch between tables at
runtime. This allows you to change behaviour without any tricks, without
any overhead of a union to carry all the differing data around for all
the states that you need. If you compose your class from different
attributes and abilities then need to change them post creation, you
can. Looking at it from a hardware point of view, in order to implement
this form of polymorphism you need a little extra space for the
reference to the entity in each of the class attributes or abilities,
but you don’t need a virtual table pointer to find which function to
call. You can run through all entities of the same type increasing cache
effectiveness, even though it provides a safe way to change type at
runtime.

As another potential benefit, the implicit nature of having classes
defined by the tables they belong to, there is an opportunity to
register a single entity with more than one table. This means that not
only can a class be dynamically runtime polymorphic, but it can also be
multimorphic in the sense that it can be more than one class at a time.
A single entity might react in two different ways to the same trigger
call because that might be appropriate for that current state for that
class. This kind of multidimensional classing doesn’t come up much in
gameplay code, but in rendering, there are usually a few different axes
of variation such as the material, what blend mode, what kind of
skinning or other vertex adjustments are going to take place on a given
instance. Maybe we don’t see this flexibility in gameplay code because
it’s not available through the natural tools of the language.

Event handling {#sec:exist-event}
--------------

When you wanted to listen for events in a system in the old days, you’d
attach yourself to an interrupt. Sometimes you might get to poke at code
that still does this, but it’s normally reserved for old or
microcontroller scale hardware. The idea was simple, the processor
wasn’t really fast enough to poll all the possible sources of
information and do something about the data, but it was fast enough to
be told about events and process the information as and when it arrived.
Event handling in games has often been like this, register yourself as
interested in an event, then get told about it when it happens. The
publish and subscribe model has been around for many years, but there’s
not been a standard interface built for it as it often requires from
problem domain knowledge to implement effectively. Some systems want to
be told about every event in the system and decide for themselves, such
as windows event handling. Some systems subscribe to very particular
events but want to react to them as soon as they happen, such as
handlers for the BIOS events like the keyboard interrupt.

Using your existence in a table as the registration technique makes this
simpler than before and lets you register and de-register with great
pace. You can register an entity as being interested in events, and
choose to fire off the transform immediately, or queue up new events
until the next loop round. As the model becomes simpler and more usable,
the opportunity for more common use leads us to new ways of implementing
code traditionally done via polling.

For example: unless the player character is within the distance to
activate a door, the event handler for the player’s action button wont
be attached to anything door related. When the character comes within
range, the character registers into the *has\_pressed\_action* event
table with the *open\_door\_(X)* event result. This reduces the amount
of time the CPU wastes figuring out what thing the player was trying to
activate, and also helps provide state information such as on-screen
displays saying that *pressing Green will Open the door*. It may even do
this by hooking into low level tables generated by default such as a
*character registers into the has\_pressed\_action event table* event.

This coding style is somewhat reminiscent of aspect oriented programming
where it is easy to allow for cross-cutting concerns in the code. In
aspect oriented programming, the core code for any activities is kept
clean, and any side effects or vetoes of actions are handled by other
concerns hooking into the activity from outside. This keeps the core
code clean at the expense of not knowing what is really going to be
called when you write a line of code. How using registration tables
differs is in where the reactions come from and how they are determined.
As we shall see in chapter [chap:condition], when you use conditions for
logical reactions, debugging can become significantly simpler as the
barriers between cause and effect normally implicit in aspect oriented
programming are significantly diminished or removed, and the hard to
adjust nature of object oriented decision making can be softened to
allow your code to become more dynamic without the normal associated
cost of data driven control flow.

[^1]: hot data is the member or members of a class that are accessed
    with high frequency, and there can even be multiple per class.
