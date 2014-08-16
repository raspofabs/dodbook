Refactoring
-----------

During refactoring, it’s always important to know that you’ve not broken
anything by changing the code. Allowing for such simple unit testing
gets you halfway there. Another advantage of data-orieted development is
that, at every turn, it peels away the unnecessary elements, so you
might find that refactoring is more a case of switching out the order of
transforms more than changing how things are represented. Refactoring
normally involves some new data representation, but as long as you
normalise your data, there’s going to be little need of that. When it is
needed, tools for converting from one schema to another can be written
once and used many times.
