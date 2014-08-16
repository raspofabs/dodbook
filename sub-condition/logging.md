Logging decisions for debug: Making answers talk for themselves
---------------------------------------------------------------

With all this raw data moving around, some may think that it would be
harder to debug than a human friendly object-oriented code layout.
Indeed, some developers think that you need to understand the data in a
problem centric way in order to figure out what is causing a bug,
however, normally a bug is where the implementation did what was
written, not what was meant, and that can usually be found through
understanding what is going on inside the software, and not the problem
that was being solved by it. Most bug slaying involves understanding
what the computer was doing before it did the unexpected. It is hardly
ever about understanding the design, or the concepts represented by the
classes. It is very unlikely that your bug exists in something as high
level as the fact that a house is not a car.

For example, if you have a bug where a specific mesh is being culled,
you might think that you need to see the data about the entity that
renders that mesh all in one place. You may think that otherwise you
could spend a lot of time traversing data structures in a watch window
just to find out in what state an object was, that caused it to flip its
visible bit to false. This human view of the data may seem important to
many seasoned developers, but it’s false reasoning based on how
difficult it is to debug and reason about data structures inside an
object-oriented program. We’re used to thinking about our data as
objects, but our data is not objects, it’s data.

If your code is data-oriented, with checkpoints between each transform,
it becomes very easy to log any changes and their reason why. It even
becomes simpler to rerun transforms in order to find out what conditions
caused them to change. If you are using condition tables, you can run
the condition check multiple times to figure out what caused them to
emit or not emit output rows. If you keep the development
stream-oriented, that is, no mutable state or in-place modification,
then you can even allow for rolling back a lot of your program in order
to find the original cause of any bad state. We can roll back when we
don’t have global state mutation because any previous data implies a
state. As long as you don’t modify the stream, but instead generate a
new one as you make your way through your updates, you can always look
back and see what caused the change, or at least see where the data
didn’t match expectation.

If you think about things like meshes as being objects that have state,
then you are going to worry about how data got into a particular state.
Most object oriented developers fear that without the problem domain
borders, then states may get lost in one of the myriad anonymous
transforms that affect the data streaming through the system, however,
this is only because Object-oriented design allows or even enforces the
dangerous practice of hidden data and mutable state. As it is relatively
easy to hook an event handler to any table insert, adding logging for
bad state changes is very easy, and if you keep your transforms
deterministic, it becomes highly repeatable. In some languages there are
virtual machines that allow for complete rollback of the program. There
is a JVM that maintains historic state, and Microsoft’s CLR provides the
ability to go back in time for some of its languages. If you program
your game with condition tables, thorough logging, and a deterministic
set of transforms, you can have game state rollback in a high
performance language such as C++.

With this information at hand, it can be safe to assume that for the
normal practice of debugging, which is figuring out how an object got
into a particularly bad state, working within a well formed data
oriented code base would make debugging easier, not harder.

