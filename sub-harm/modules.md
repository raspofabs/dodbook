Divions of labour
-----------------

*Modular architecture for reduced coupling and better testing*\

The object-oriented paradigm is seen as another tool in the kit when it
comes to ensuring quality of code. Strictly adhering to the open closed
principle of always using accessors, methods, and inheritance to use or
extend objects, programmers write significantly more modular code than
they do if programming from a purely procedural perspective. This
modularity separates each object’s code into units. These units are
collections of all the data and methods that act upon the data. It has
been written about many times that testing objects is simpler because
each object can be tested in isolation.

However, Object-oriented design suffers from the problem of errors in
communication. Objects are not systems, and systems need to be tested,
and systems comprise of not only objects, but their inherent
communication. The communication of objects is difficult to test,
because in practice, it is hard to isolate the interactions between
classes. Object-oriented development leads to an Object-oriented view of
the system which makes it hard to isolate non-objects such as data
transforms, communication, and temporal coupling.

Modular architecture is good because it limits the potential damage
caused by changes, but just like encapsulation before, the contract to
any module has to be unambiguous so as to reduce the chance of external
reliance on unintended side effects of the implementation.

The reason Object-oriented modular approach doesn’t work as well, is
that the modules are defined by object boundary, not by a higher level
concept. Good examples of modularity include stdio’s FILE, the CRT’s
malloc/free, The NvTriStrip library’s GenerateStrips. Each of these
provide a solid, documented, narrow set of functions to access
functionality that could otherwise be overwhelming and difficult to
reason about.

Modularity in Object-oriented development can offer protection from
other programmers who don’t understand the code. An object’s methods are
often the instruction manual for an object in the eyes of a co-worker,
so writing all the important manipulation methods in one block can give
clues to anyone using the class. The modularity is important here
because game development objects are regularly large, offering a lot of
functionality spread across their many different aspects. Rather than
find a way to address cross cutting concerns, game objects tend to
fulfil all requirements rather than restrict themselves to their
original design. Because of this bloating, the modular approach, that
is, collecting methods by their concern in the source, can be beneficial
to programmers coming at the object fresh. The obvious way to fix this
would be to use a paradigm that supports cross cutting concerns at a
more fundamental level, but Object-oriented development is know to be
inefficient at representing this in code.

If Object-oriented development doesn’t increase modularity in such a way
as it provides better results than explicitly modularising code, then
what does it offer?

