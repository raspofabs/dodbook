It’s all about the data
-----------------------

Data is all we have. Data is what we need to transform in order to
create a user experience. Data is what we load when we open a document.
Data is the graphics on the screen and the pulses from the buttons on
your game pad and the cause of your speakers and headphones producing
waves in the air and the method by which you level up and how the bad
guy knew where you were to shoot at you and how long the dynamite took
to explode and how many rings you dropped when you fell on the spikes
and the current velocity of every particle in the beautiful scene that
ended the game, that was loaded off the disc and into your life. Any
application is nothing without its data. Photoshop without the images is
nothing. Word is nothing without the characters. Cubase is worthless
without the events. All the applications that have ever been written
have been written to output data based on some input data. The form of
that data can be extremely complex, or so simple it requires no
documentation at all, but all applications produce and need data.

Instructions are data too. Instructions take up memory, use up
bandwidth, and can be transformed, loaded, saved and constructed. It’s
natural for a developer to not think of instructions as being data (unless they are a lisp programmer),
but there is very little differentiating them on older, less protective
hardware. Even though memory set aside for executables is protected from
harm and modification on most contemporary hardware, this relatively new
invention is still merely an invention. Instructions are still data, and
once more, they are what we transform too. We take instructions and turn
them into actions. The number, size, and frequency of them is something
that matters and that we have control over.

This forms the basis of the argument for a data-oriented approach to
development, but leaves out one major element. All this data and the
transforming of data, from strings, to images, to instructions, they all
have to run on something. Sometimes that thing is quite abstract, such
as a virtual machine running on unknown hardware. Sometimes that thing
is concrete, such as knowing which specific CPU and what speed and
memory capacity and bandwidth you have available. But in all cases, the
data is not just data, but data that exists on some hardware somewhere,
and it has to be transformed by some hardware. In essence, data-oriented
design is the practice of designing software by developing transforms
for well formed data where well formed is guided by the target hardware
and the transforms that will operate on it. Sometimes the data isn’t
well defined, and sometimes the hardware is equally evasive, but in most
cases a good background of hardware appreciation can help out almost
every software project.

If the ultimate result of an application is data, and all input can be
represented by data, and it is recognised that all data transforms are
not performed in a vacuum, then a software development methodology can
be founded on these principles, the principles of understanding the
data, and how to transform it given some knowledge of how a machine will
do what it needs to do with data of this quantity, frequency, and it’s
statistical qualities. Given this basis, we can build up a set of
founding statements about what makes a methodology data-oriented.
