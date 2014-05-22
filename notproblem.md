Data is not the problem domain
------------------------------

The first principle: Data is not the problem domain.

For some, it would seem that data-oriented design is the antithesis of
most other programming paradigms because data-oriented design is a
technique that does not readily allow the problem domain to enter into
the software so readily. It does not recognise the concept of an object
in any way, as data is consistently without meaning, whereas the
abstraction heavy paradigms try to pretend the computer and its data do
not exist at every turn, abstracting away the idea that there are bytes,
or CPU pipelines, or other hardware features.

The data-oriented design approach doesn’t build the real world problem
into the code. This could be seen as a failing of the data-oriented
approach by veteran object-oriented developers, as many examples of the
success of object-oriented design come from being able to bring the
human concepts to the machine, then in this middle ground, a solution
can be written in this language that is understandable by both human and
computer. The data-oriented approach gives up some of the human
readability by leaving the problem domain in the design document, but
stops the machine from having to handle human concepts at any level by
just that same action.

Let us consider first how the problem domain becomes part of the
software in programming paradigms that promote abstraction. In the case
of objects, we tie meanings to data by associating them with their
containing classes and their associated functions. In high level
abstraction, we separate actions and data by high level concepts, which
might not apply at the low level, thus reducing the likelihood that the
functions will be efficiently implemented.

When a class owns some data, it gives that data a context, and that
context can sometimes limit the ability to reuse the data. Adding
functions to a context can bring in further data, which quickly leads to
classes that contain many different pieces of data that are unrelated in
themselves, but need to be in the same class because an operation
required a context, but the operation also required additional data.
Normally this becomes hard to untangle as functions that operate over
the whole context drag in random pieces of data from all over the class
meaning that many data items cannot be removed as they would then be
inaccessible.

When we consider the data from the data-oriented design point of view,
data is mere facts that can be interpreted in whatever way necessary to
get the output data in the format it needs to be. We only care about
what transforms we do, and where the data ends up. In practice, when you
discard meanings from data, you also reduce the chance of tangling the
facts with their contexts, and thus you also reduce the likelihood of
mixing unrelated data just for the sake of an operation or two.

