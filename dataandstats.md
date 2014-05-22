Data and Statistics
-------------------

The second principle: Data is type, frequency, quantity, shape and
probability.

The second statement is that data is not just the structure. A common
misconception about data-oriented design is that it’s all about cache
misses. Even if it was all about making sure you never missed the cache,
and it was all about structuring your classes so the hot and cold data
was split apart, it would be a generally useful addition to your toolkit
of thought, but data-oriented design is about all aspects of the data.
To write a book on how to avoid cache misses, you need more than just
some tips on how to organise your structures, you need a grounding in
what is really happening inside your computer when it is running your
program. Teaching that in a book is also impossible as it would only
apply to one generation of hardware, and one generation of programming
languages, however data oriented design is not rooted in one language
and one set of hardware. The schema of the data is still important, but
the actual values are as important, if not more so. It is not enough to
have some photographs of a cheetah to determine how fast it can run. You
need to see it in the wild.

The data-oriented design model is centred around data, live data, real
data, information data. Object-oriented design is centred around the
problem and its solution. Objects, not real things, but abstract
representations of things that make up the design of the solution to the
problem presented in the application design document. The objects only
manipulate the data needed to represent them without any consideration
for the hardware or the real world data patterns or quantities. This is
why object-oriented design allows you to quickly build up first versions
of applications, allowing you to put the first version of the design
document or problem definition directly into the code.

Data-oriented design takes a different approach to the problem, instead
of assuming that we know nothing about the hardware, it assumes we know
nothing about the problem. Anyone who has written a sizable piece of
software should recognise that the technical design for any project can
change so much that there is hardly anything recognisable from the first
draft in the final implementation. Data-oriented design avoids this
waste of resources by never assuming that the design needs to exist
anywhere other than in a document while it proceeds to provide a
solution to the current problem.

Data-Oriented Design takes it’s cues from the data that is seen or
expected. Instead of planning for all eventualities, or planning to make
things adaptable, it uses the most probable input to direct the choice
of algorithm. Instead of planning to be extendible, it plans to be
simple, and get the job done. Extendible can be added later, with the
safety net of unit tests to ensure that it remains working as it did
while it was simple.

