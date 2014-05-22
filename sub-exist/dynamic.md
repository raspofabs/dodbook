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

