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

