Data driven techniques
----------------------

Apart from finite state machines there are some other common forms of
data driven coding practices, some of which are not very obvious, such
as callbacks, and some of which are very much so, such as scripting. In
both these cases, data causing the flow of code to change will cause the
same kind of cache and pipe-line problems as seen in virtual calls and
finite state machines.

Callbacks can be made safer by using triggers from event subscription tables.
Rather than have a callback that fires off when a job is done, have an event
table for done jobs so that callbacks can be called once the whole run is
finished. This also means that the callback is running on the thread it was
intended to run, in case of expected locking considerations, meaning less
locking code in general.

For example, if a scoring system has a callback from “badGuyDies”, then in an
Object-oriented message watcher you would have the scorer increment its
internal score whenever it received the message that a badGuyDies. Instead run
each of the callbacks in the callback table once the whole set of badguys has
been checked for death. If you do that, and execute every time all the badGuys
have had their tick, then you can add points once for all badGuys killed. That
means one read for the internal state, and one write. Much better than multiple
reads and writes accumulating a final score.

For scripting, if you have scripts that run over multiple entities,
consider how the graphics kernels operate with branches, sometimes using
predication and doing both sides of a branch before selecting a
solution. This would allow you to reduce the number of branches caused
merely by interpreting the script on demand. If you go one step further
an actually build SIMD into the scripting core, then you might find that
you can run script for a very large number of entities compared to
traditional per entity serial scripting. If your SIMD operations operate
over the whole collection of entities, then you will pay almost no price
for script interpretation[^4].

[^4]: Take a look at the section headed *The Massively Vectorized
    Virtual Machine* on the bitsquid blog
    http://bitsquid.blogspot.co.uk/2012/10/a-data-oriented-data-driven-system-for.html
