Internalised state
------------------

*Encapsulation makes code more reusable. It’s easier to modify the
implementation without affecting the usage. Maintenance and refactoring
become easy, quick, and safe.*\

The idea behind encapsulation is to provide a contract to the person
using the code rather than providing a raw implementation. In theory,
well written Object-oriented code that uses encapsulation is immune to
damage caused by changing how an object manipulates its data. If all the
code using the object complies with the contract and never directly uses
any of the data members without going through accessor functions, then
no matter what you change about how the class fulfils that contract,
there won’t be any new bugs introduced by change. In theory, the object
implementation can change in any way as long as the contract is not
modified, but only extended. This is the open closed principle. A class
should be open for extension, but closed for modification.

A contract is meant to provide some guarantees about how a complex
system works. In practice, only unit testing can provide these
guarantees.

Sometimes, programmers unwittingly rely on hidden features of objects’
implementations. Sometimes the object they rely on has a bug that just
so happens to fit their use case. If that bug is fixed, then the code
using the object no longer works as expected. The use of the contract,
though it was kept intact, has not helped the other piece of code to
maintain working status across revisions. Instead it provided false hope
that the returned values would not change. It doesn’t even have to be a
bug. Temporal couplings inside objects, or accidental or undocumented
features that goes away in later revisions can also damage the code
using the contract without breaking it.

One example would be the case where an object has a method that returns
a list. If the internal representation is such that it always maintains
a sorted list, and when the method is called it returns some subset of
that list, it would be natural to assume that in most implementations of
the method the subset would be sorted also. A concrete example could be
a pickup manager that kept a list of pickups sorted by name. If the
function returns all the pickup types that match a filter, then the
caller could iterate the returned list until it found the pickup it
wanted. To speed things up, it could early-out if it found a pickup with
a name later than the item it was looking for, or it could do a binary
search of the returned list. In both those cases, if the internal
representation changed to something that wasn’t ordered by name, then
the code would no longer work. If the internal representation was
changed so it was ordered by hash, then the early-out and binary search
would be completely broken.

Another example of the contract being too little information, in many
linked list implementations, there is a decision made about whether to
store the length of the list or not. The choice to store a count member
will make multi-threaded access slower, but the choice not to store it
will make finding the length of the list an O(n) operation. For
situations where you only want to find out whether the list if empty, if
the object contract only supplies a get\_count() function, you cannot
know for sure whether it would be cheaper to check if the count was
greater than zero, or check if the being() and end() are the same.

Encapsulation only provides a way to hide bugs and cause assumptions in
programmers. There is an old saying about assumptions, and encapsulation
doesn’t let you confirm or deny them unless you have access to the
source code. If you have, and you need to look at it to find out what
went wrong, then all that the encapsulation has done is add another
layer to work around rather than add any functionality of its own.

