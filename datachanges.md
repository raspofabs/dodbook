Data changes
------------

Data-oriented design is current. Object-oriented design starts to show
its weaknesses when designs change. Object-oriented design suffers from
an inertia inherent in keeping the problem domain coupled with the
implementation. A data-oriented approach to design takes note of the
change in design by understanding the change in the data. The
data-oriented approach to design also allows for change to the code when
the source of data changes, unlike the encapsulated internal state
manipulations of the object-oriented approach. In general, data-oriented
design handles change better as pieces of data and transforms can be
more simply coupled and decoupled than objects can be mutated and
reused.

The reason this is so comes from the linking of intention and aspect
that comes with lumping data and functions in with concepts of objects
where the objects are the schema, the aspect, the use case, and the real
world or design counterpart to the code. If you link your data
manipulations to your data then you make it hard to unlink data related
by operation. If you link your operations by related data, then you make
it hard to unlink your operations when the data changes or splits. If
you keep your data in one place, write operations in another place, and
keep the aspects and roles of data intrinsic from how the operations and
transforms are applied to the data, then you will find that many
refactorings that would have been large and difficult in object oriented
code, become trivial. With this benefit comes a cost of keeping tabs on
what data is required for each operation, and the potential danger of
desynchronisation. This consideration can lead to keeping some cold code
in an object oriented style where objects are responsible for
maintaining internal consistency over efficiency and mutability.

A big misunderstanding for many new to the data-oriented design
paradigm, a concept brought over from abstraction based development, is
that we can design a static library or set of templates to provide
generic solutions to everything presented in this book as a
data-oriented solution. The awful truth is that data, though it can be
generic by type, is not generic in any real world sense. The values are
different, and often contain patterns that we can turn to our advantage.
How would it be possible to do compression if it were not for patterns?
Our runtime code can also benefit from this but it is overlooked as
being not object-oriented, or being too hard coded. It can be better to
hard code a transform than pretend it’s not hard coded by wrapping it in
a generic container and using the wrong algorithms on it. Using existing
templates like this provide a known benefit of a minor increase in
readability to those who already know of the library, and potentially
less bugs if the functionality was in some way generic. But, if the
functionality was not very well mapped to the existing generic solution,
writing it with a templated function and then extending would possibly
make the code harder to read by hiding the fact that the technique had
been changed subtly. Hard coding a new algorithm is frequently a better
choice as long as it has sufficient tests, and tests are easier to write
if you constrain yourself to the facts about the data, and only work
with simple data and not stateful objects.
