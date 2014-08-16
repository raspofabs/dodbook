Unit Testing
------------

Unit testing can be very helpful when developing games, but because of
the object-oriented paradigm making programmers think about code as
representations of objects, and not as data transforms, it’s hard to see
what can be tested. Linking together unrelated concepts into the same
object and requiring complex setup state before a test can be carried
out, has given unit testing a stunted start in games as object-oriented
programming caused simple tests to be hard to write. Making tests is
further complicated by the addition of the non-obvious nature of how
objects are transformed when they represent entities in a game world. It
can be very hard to write unit tests unless you’ve been working with
them for a while, and the main point of unit tests is that someone that
doesn’t fully grok the system can make changes without falling foul of
making things worse.

Unit testing is mostly useful during refactorings, taking a game or
engine from one code and data layout into another one, ready for future
changes. Usually this is done because the data is in the wrong shape,
which in itself is harder to do if you normalise your data as you’re
more likely to have left the data in an unconfigured form. There will
obviously be times when even normalised data is not sufficient, such as
when the design of the game changes sufficient to render the original
data-analysis incorrect, or at the very least, ineffective or
inefficient.

Unit testing is simple with data-oriented technique because you are
already concentrating on the transform. Generating tables of test data
would be part of your development, so leaving some in as unit tests
would be simple, if not part of the process of developing the game.
Using unit tests to help guide the code could be considered to be
partial following the test-driven development technique, a proven good
way to generate efficient and clear code.

Remember, when you’re doing data-oriented development your game is
entirely driven by stateful data and stateless transforms. It is very
simple to produce unit tests for your transforms. You don’t even need a
framework, just an input and output table and then a comparison function
to check that the transform produced the right data.

