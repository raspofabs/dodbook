Hierarchical design
-------------------

*Inheritance allows reuse of code by extension. Adding new features is
simple.*\

Inheritance was seen as a major reason to use classes in C++ by games
programmers. The obvious benefit was being able to inherit from multiple
interfaces to gain attributes or agency in system objects such as
physics, animation, and rendering. In the early days of C++ adoption,
the hierarchies were shallow, not usually going much more than three
layers deep, but later it became commonplace to find more than nine
levels of ancestors in central classes such as that of the player, their
vehicles, or the AI players. For example, in UnrealTournament, the
minigun ammo object had this:

Miniammo $\rightarrow$ TournamentAmmo $\rightarrow$ Ammo $\rightarrow$
Pickup $\rightarrow$ Inventory $\rightarrow$ Actor $\rightarrow$ Object

Games developers use inheritance to provide a robust way to implement
polymorphism in games, where many game entities can be updated,
rendered, or queried en-mass, without any hand coded checking of type.
They also appreciate the reduced copy pasting, because inheriting from a
class also adds functionality to a class. This early form of mix-ins was
seen to reduce errors in coding as there were often times where bugs
only existed because a programmer had fixed a bug in one place, but not
all of them. Gradually, multiple inheritance faded into interfaces only,
the practice of only inheriting from one real class, and any others had
to be pure virtual interface classes as per the Java definition.

Although it seems like inheriting from class to extend its functionality
is safe, there are many circumstances where classes don’t quite behave
as expected when methods are overridden. To extend a class, it is often
necessary to read the source, not just of the class you’re inheriting,
but also the classes it inherits too. If a base class creates a pure
virtual method, then it forces the child class to implement that method.
If this was for a good reason, then that should be enforced, but you
cannot enforce that every inheriting class implements this method, only
the first instantiable class inheriting it. This can lead to obscure
bugs where a new class sometimes acts or is treated like the class it is
inheriting from.

Another pitfall of inheritance in C++ comes in the form of runtime
versus compile time linking. A good example is default arguments on
method calls, and badly understood overriding rules. What would you
expect the output of the following program to be?

    class A {
        virtual void foo( int bar = 5 ) { cout << bar; }
    };
    class B : public A {
        void foo( int bar = 7 ) { cout << bar * 2; }
    };
    int main( int argc, char *argv[] ) {
        A *a = new B;
        a->foo();
        return 0;
    }

Would you be surprised to find out it reported a value of 10? Some code
relies on the compiled state, some on runtime. Adding new functionality
to a class by extending it can quickly become a dangerous game as
classes from two layers down can cause coupling side effects, throw
exceptions (or worse, not throw an exception and quietly fail,)
circumvent your changes, or possibly just make it impossible to
implement your feature as they might already be taking up the namespace
or have some other incompatibility with your plans, such as requiring a
certain alignment or need to be in a certain bank of ram.

Inheritance does provide a clean way of implementing runtime
polymorphism, but it’s not the only way as we saw earlier. Adding a new
feature by inheritance requires revisiting the base class, providing a
default implementation, or a pure virtual, then providing
implementations for all the classes that need to handle the new feature.
Obviously this has required access to the base class, and possible
touching of all child classes if the pure virtual route is taken, so
even though the compiler can help you find all the places where the code
needs to change, it has not made it significantly easier to change the
code.

Using a type member instead of a virtual table pointer can give you the
same runtime code linking, could be better for cache misses, and could
be easier to add new features and reason about because it has less
baggage when it comes to implementing those new features, provides a
very simple way to mix and match capabilities compared to inheritance,
and keeps the polymorphic code in one place. For example, in the fake
virtual function go-forward, the class Car will step on the gas. In the
class Person, it will set the direction vector. In the class UFO, it
will also just set the direction vector. This sounds like a job for a
switch statement fall through. In the fake virtual function re-fuel, the
class Car and UFO will start a re-fuel timer and remain stationary while
their fuelling up animatios play, whereas the Person class could just
reduce their stamina-potion count and be instantly refuelled. Again, a
switch statement with fall through provides all the runtime polymorphism
you need, but you don’t need to multiple inherit in order to provide
differing functionality on a per class per function level. Being able to
pick what each method does in a class is not something that inheritance
is good at, but it is something desirable, and non inheritance based
polymorphism does allow it.

The original reason for using inheritance was that you would not need to
revisit the base class, or change any of the existing code in order to
extend and add functionality to the codebase, however, it is highly
likely that you will at least need to view the base class
implementation, and with changing specifications in games, it’s also
quite common to need changes at the base class level. Inheritance also
inhibits certain types of analysis by locking people into thinking of
objects as having IS-A relationships with the other object types in the
game. A lot of flexibility is lost when a programmer is locked out of
conceptualising objects as being combinations of features. Reducing
multiple inheritance to interfaces, though helping to reduce the code
complexity, has drawn a veil over the one good way of building up
classes as compound objects. Although not a good solution in itself as
it still abuses the cache, a switch on type seems to offer similar
functionality to virtual tables without some of the associated baggage.
So why put things in classes?

