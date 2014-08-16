What it means to be thread-safe
-------------------------------

Academics consistently focus on what is possible and correct, rather than what
is practical and usable, which is why we’ve been inundated with multi-threaded
techniques that work, but are complex, and cause a lot of unnecessary pain when
used in a high performance system such as a game. The idea that something is
thread-safe implies more than just that it is safe to use in a multi-threaded
environment. There are lots of thread safe functions that aren’t mentioned
becuase they seem trivial, but it’s a useful distinction to make when you are
tracking down what could be causing a strange thread issue. There are functions
without side-effects, such as the intrinsics for sin, sqrt, that return a value
given a value. There is no way they can cause any other code to change
behaviour, and no other code can change its behaviour either[^1]. In addition
to these very simple functions, there are the simple functions that change
things in an idempotent fashion, such as memset.

Thread safe implies that it doesn’t just access its own data, but
accesses some shared data without causing the system to enter into an
inconsistent state. Inconsistent state is a natural side effect of
multiple processes accessing and writing to shared memory. It is these
side effects that are the cause of many bugs in multi-threaded code,
which is why the develpers of the Erlang language chose to limit the
programmer to code that doesn’t have side-effects. Any code that relies
on reading from a shared memory before writing back an adjusted value
can cause inconsistent state as there is no way to guarantee that the
writing will take place before anyone else reads it before they modify
it.

    int shared = 0;
    void foo() {
        int a = shared;
        a += RunSomeCalculation();
        shared = a;
    }

Making this work in practice is hard and expensive. The standard
technique used to ensure the state is consistent is to make the value
update atomic. How this is achieved depends on the hardware and the
compiler. Most hardware has an atomic instruction that can be used to
create thread-safety through mutual exclusions. On most hardware the
atomic instruction is a compare and swap, or CAS. Building larger tools
for thread-safety from this has been the mainstay of multi-threaded
programmers and operating system developers for decades, but with the
advent of multi-core consoles, programmers not well versed in the
potential pitfalls of multi-threaded development are suffering because
of the learning cliff involved in making all their code work perfectly
over six or more hardware threads.

Using mutual exclusions, it’s possible to rewrite the previous example:

    int shared = 0;
    Mutex sharedMutex;
    void foo() {
        sharedMutex.acquire();
        int a = shared;
        a += RunSomeCalculation();
        shared = a;
        sharedMutex.release();
    }

And now it works. No matter what, this function will now always finish
its task without some other process damaging its data. Every time one of
the hardware threads encounters this code, it stops all processing until
the mutex is acquired. Once it’s acquired, no other hardware thread can
enter into these instructions until the current thread releases the
mutex at the far end.

Every time a thread-safe function uses a mutex section, the whole
machine stops to do just one thing. Every time you do stuff inside a
mutex, you make the code thread-safe by making it serial. Every time you
use a mutex, you make your code run bad on infinite core machines.

Thread-safe, therefore, is another way of saying: not concurrent, but
won’t break anything. Concurrency is when multiple threads are doing
their thing without any mutex calls, semaphores, or other form of
serialisation of task. Concurrent means at the same time. A lot of the
problems that are solved by academics using thread-safety to develop
their multi-threaded applications needn’t be mutex bound. There are many
ways to skin a cat, and many ways to avoid a mutex. Mutex are only
necessary when more than one thread shares write privileges on a piece
of memory. If you can redesign your algorithms so they only ever require
one thread to be given write privilege, then you can work towards a
fully concurrent system.

Ownership is key to developing most concurrent algorithms. Concurrency
only happens when the code cannot be in a bad state, not because it
checks before doing work, but because the design is such that no process
can interfere with another in any way.

[^1]: If you discount the possibility of other code changing the
    floating point operation mode

