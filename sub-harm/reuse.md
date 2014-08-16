Reusable generic code
---------------------

*Faster development time through reuse of generic code*\

It is regarded as one of the holy grails of development to be able to
consistently reduce development overhead by reusing old code. In order
to stop wasting any of the investment in time and effort, it’s been
assumed that it will be possible to put together an application from
existing code and only have to write some minor new features. The
unfortunate truth is that any interesting new features you want to add
will probably be incompatible with your old code and old way of laying
out your data, and you will need to either rewrite the old code to allow
for the new feature, or rewrite the old code to allow for the new data
layout. If a software project can be built from existing solutions,
objects that were invented to provide features for an old project, then
it’s probably not very complex. Any project for significant complexity
includes hundreds if not thousands of special case objects that provide
all particular needs of that project. For example, the vast majority of
games will have a player class, but almost none share a common core set
of attributes. Is there a world position member in a game of poker? Is
there a hit point count member in the player of a racing game? Does the
player have a gamer tag in a purely offline game? Having a generic class
that can be reused doesn’t make the game easier to create, all it does
is move the specialisation into somewhere else. Some game toolkits do
this by allowing script to extend the basic classes. Some game engines
limit the gameplay to a certain genre and allow extension away from that
through data driven means. No-one has so far created a game API, because
to do so, it would have to be so generic that it wouldn’t provide
anything more than what we already have with our languages we use for
development.

Reuse, being hankered after by production, and thought of so highly by
anyone without much experience in making games, has become an end in
itself for many games developers. The pitfall of generics is a focus on
keeping a class generic enough to be reused or re-purposed without
thought as to why, or how. The first, the why, is a major stumbling
block and needs to be taught out of developers as quickly as possible.
Making something generic, for the sake of generality, is not a valid
goal. It adds time to development without adding value. Some developers
would cite this as short sighted, however, it is the how that deflates
this argument. How do you generalise a class if you only use it in one
place? The implementation of a class is testable only so far as it can
be tested, and if you only use a class in one place, you can only test
that it works in one situation. If you then generalise the class, yet
don’t have any other test cases than the first situation, then all you
can test is that you didn’t break the class when generalising it. So, if
you cannot guarantee that the class works for other types or situations,
all you have done by generalising the class is added more code for bugs
to hide in. The resultant bugs are now hidden in code that works,
possibly even tested, which means that any bugs introduced during this
generalising have been stamped and approved.

Test driven development implicitly denies generic coding until the point
where it is a good choice to do so. The only time when it is a good
choice to move code to a more generic state, is when it reduces
redundancy through reuse of common functionality.

Generic code has to fulfil more than just a basic set of features if it
is to be used in many situations. If you write a templated array
container, access to the array through the square bracket operators
would be considered a basic feature, but you will also want to write
iterators for it and possibly add an insert routine to take the headache
out of shuffling the array up in memory. Little bugs can creep in if you
rewrite these functions whenever you need them, and linked lists are
notorious for having bugs in quick and dirty implementations. To be fit
for use by all users, any generic container should provide a full set of
methods for manipulation, and the STL does that. There are hundreds of
different functions to understand before you can be considered an
STL-expert, and you have to be an STL-expert before you can be sure
you’re writing efficient code with the STL. There is a large amount of
documentation available for the various implementations of the STL. Most
of the implementations of the STL are very similar if not functionally
the same. Even so, it can take some time for a programmer to become a
valuable STL programmer due to this need to learn another langauge. The
programmer has to learn a new language, the language of the STL, with
its own nouns verbs and adjectives. To limit this, many games companies
have a much reduced feature set reinterpretation of the STL that
optionally provides better memory handling (because of the awkward
hardware), more choice for the containers (so that you may choose a
hash\_map or trie, rather than just a map), or explicit implementations
of simpler containers such as stack or singly linked lists and their
intrusive brethren. These libraries are normally smaller in scope and
are therefore easier to learn and hack than the STL variants, but they
still need to be learnt and that takes some time. In the past this was a
good compromise, but now the STL has extensive online documentation,
there is no excuse not to use the STL except where memory or compilation
time is concerned.

The takeaway from this however, is that generic code still needs to be
learnt in order for the coder to be efficient, or not cause accidental
performance bottlenecks. If you go with the STL, then at least you have
a lot of documentation on your side. If your game company implements an
amazingly complex template library, don’t expect any coders to use it
until they’ve had enough time to learn it, and that means that if you
write generic code, expect people to not use it unless they come across
it accidentally, or have been explicitly told to, as they won’t know
it’s there, or won’t trust it. In other words, starting out by writing
generic code is a good way to write a lot of code quickly without adding
any value to your development.
