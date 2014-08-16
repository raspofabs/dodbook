Beautiful Homogeneity
---------------------

Apart from all the speed increases and the simplicity of extension,
there is also an implicit tendency to turn out accidentally reusable
solutions to problems. This is caused by the data being formatted much
more rigidly, and therefore when it fits, can almost be seen as a type
of duck-typing. If the data can fit a transform, a transform can act on
it. Some would argue that just because the types match, doesn’t mean the
function will create the expected outcome, but this is simply avoidable
by not reusing code you don’t understand. Because the code becomes much
more penetrable, it takes less time to look at what a transform is doing
before committing to reusing it in your own code.

Another benefit that comes from the data being built in the same way
each time, handled with transforms and always being held in the same
types of container is that there is a very good chance that there are
multiple intention agnostic optimisations that can be applied to every
part of the code. General purpose sorting, counting, searches and
spatial awareness systems can be attached to new data without calling
for OOP adapters or implementing interfaces so that Strategies can run
over them.

A final reason to work with data in an immutable way comes in the form
of preparations for optimisation. C++, as a language, provides a lot of
ways for the programmer to shoot themselves in the foot, and one of the
best is that pointers to memory can cause unexpected side effects when
used without caution. Consider this piece of code:

~~~~ {caption="byte" copying=""}
char buffer[ 100 ];
buffer[0] = 'X';
memcpy( buffer+1, buffer, 98 );
buffer[ 99 ] = '\0';
~~~~

this is perfectly correct code if you just want to get a string with 99
’X’s in it. However, because this is possible, memcpy has to copy one
byte at a time. To speed up copying, you normally load in a lot of
memory locations at once, then save them out once they are all in the
cache. If your input data can be modified by your output buffer, then
you have to tread very carefully. Now consider this:

~~~~ {caption="trivially" parallelisable="" code=""}
int q=10;
int p[10];
for( int i = 0; i < q; ++i )
    p[i] = i;
~~~~

The compiler can figure out that q is unaffected, and can happily unroll
this loop or replace the check against q with a register value. However,
looking at this code instead:

~~~~ {caption="potentially" aliased="" int=""}
void foo( int* p, const int &q )
{
    for( int i = 0; i < q; ++i)
        p[i] = i;
}

int q=10;
int p[10];
foo( p, q );
~~~~

The compiler cannot tell that q is unaffected by operations on p, so it
has to store p and reload q every time it checks the end of the loop.
This is called aliasing, where the address of two variables that are in
use are not known to be different, so to ensure correctly functioning
code, the variables have to be handled as if they might be at the same
address.
