Implicit Entities
-----------------

Getting your data out of a database and into your objects can appear
quite daunting, but a database approach to data storage does provide a
way to allow old executables to run off new data, it also allows new
executables to run off old data, which is can be vital when working with
other people who might need to run an earlier or later version. We saw
that sometimes adding new features required nothing more than adding a
new table. That’s a non-intrusive modification if you are using a
database, but a significant change if you’re adding a new member to a
class. If you’re trying to keep your internal code object-oriented, then
loading up tables to generate your objects isn’t as easy as having your
instances generated from script calls, or loading them in a binary file
and doing some pointer fixup. Saving can be even more of a nightmare as
when going from objects back to rows, it’s hard to tell if the database
needs rows added, deleted, or just modified. This is the same set of
issues we normally come across when using source control. The problem
with figuring out what was moved, deleted, or added when doing a three
way merge.

But again, this is only true if you convert your database formatted
files into explicit objects. These denormalised objects are troublesome
because they are in some sense, self aware. They are aware of what their
type is, and what to a large degree, what their type could be. A problem
seen many times in development is where a base type needs to change
because a new requirement does not fit with the original vision.
Explicit objects act like the original tables before normalisation: they
have a lot of nulls when features are not used. If you have a reasonable
amount of object instances, this wasted space can cause problems.

You can see how an originally small object can grow to a
disproportionate size, how a Car class can gain 8 wheel pointers in case
it is a truck, how it can gain up to 15 passengers, optionally having
lights, doors, sunroof, collision mesh, different engine, a driver base
class pointer, 2 trailers, and maybe a physics model base class pointer
so you can switch to different physics models when level collision is or
isn’t present. All these are small additions, not considered bad in
themselves, but every time you check a pointer for null it can turn out
either way. If you guess wrong, or the branch predictor guesses wrong,
the best you can hope for is an instruction cache miss or pipeline flush
before doing an action. Pipeline flushes may not be very expensive on
out-of-order CPUs, but the PS3 and Xbox360 have in-order CPUs and suffer
a stall when this happens.

It is generally assumed that if you bind your type into an explicit
object, you also allow for runtime polymorphism. This is seen as a good
thing, in that you can keep the over arching game code smaller and
easier to understand. You can have a main loop that runs over all of
your objects, calling: “Think”, “Update”, “Render”, and then you loop
forever. But runtime polymorphism is not only made possible by using
explicit types in an Object-oriented system. In the set of tables we
just normalised, the Pickups were optionally coloured. In traditional
Object-oriented C++ games development we generally define the Pickups,
and then either have an optional component for tinting or derive from
the Pickup type and add more information to the GetColour member
function. In either case it can be necessary to override the base class
in some fashion. You can either add the optional tint explicitly or make
a new class and change the Pickup factory to accept that some Pickups
can have colour tinting. In our database normalisation, adding tinting
required only adding a new table and populating it with only the Pickups
that were tinted.

The more commonly seen as a bad approach (littering with pointers to
optional things) is problematic in that it leads to a lot of cases where
you cannot quickly find out whether an object needs special care unless
you check this extended type info. For example, when rendering the
Pickups, for each one in every frame, we might need to find out whether
to render it in the alpha blend pass or in the solid pass. This can be
an important question, and because it is asked every frame in most
cases, it can add some dark matter to our profile, some cold code
ineffciency.

The more commonly seen as correct approach (that is create a new type
and adjust the factory), has a limitation that you cannot change a
Pickup from non-tinted to tinted at runtime without some major changes
to how you use Pickups in the code. This means that if an object is
tinted, it remains tinted unless you have the ability to clone and swap
in the new object. This seems quite strict in comparison to the pointer
littering technique. You may find that you end up making all pickups
tinted in the end, just because they might be tinted at some time in the
future. This would mean that you would have the old code for handling
the untinted pickup rotting while you assume it still works. This has
been the kind of code that causes one in a thousand errors that are very
hard to debug unless you get lucky.

The database approach maintains the runtime dynamicity of the pointer
littering approach by allowing for the creation of tint rows at runtime
post creation. It also maintains the non-littering aspect of the derived
type approach because we didn’t add anything to any base type to add new
functionality. It’s quicker than both for iterating, which in our
example was binning into alpha blend render pass and solid render pass.
By only iterating over the table of tints picking out which have alpha
values that cause it to be binned in alpha blended, we save memory
accesses as we’re only traversing the list of potentially alpha blended
rather than running over all the objects. All objects not in the
TintedPickup set but in the Pickup set can be assumed to be solid
rendered, no checking of anything required. We have one more benefit
with the separation of data in that it is easier to prefetch rows for
analysis when they are much simpler in layout, and we could likely have
more rows in the cache at once than in either of the other methods.

The fundamental difference between the database style approach and the
object-oriented approach is how the type of a Pickup is defined.
Traditionally, we derive new explicit types to allow new functionality
or behaviours. With databases, we add new tables and into them insert
rows referencing existing entities to show new information about old
information. We imply new functionality while not explicitly adding
anything to the original form.

In an explicit entity system, the noun is central, the entity has to be
extended with data and functions. In an implicit entity system, the
adjectives are central, they refer to an entity, implying its existence
by recognising it as being their operand. The entity only exists when
there is something to say about it. By contrast, in an explicit entity
system, you can only say something about an entity that already exists
and caters for that describability.

