Looking at hardware
===================

The first thing a good software engineer does when starting work on a
new platform is read the contents listings in all the hardware manuals.
The second thing is usually try to get hello world up and running. It’s
uncommon for a games development software engineer to decide it’s a good
idea to read all the documentation available. When they do, they will be
reading them literally, and still probably not getting all the necessary
information. When it comes to understanding hardware, there is the
theoretical restrictions implied by the comments and data sheets in the
manuals, but there is also the practical restrictions that can only be
found through working with the hardware at an intimate level.

As most of the contemporary hardware is now API driven, with hardware
manuals only being presented to the engineers responsible for graphics,
audio, and media subsystems, it’s tempting to start programming on a new
piece of hardware without thinking about the hardware at all. Most
programmers working on big games in big studios don’t really know what’s
going on at the lower levels of their game engines they’re working on,
and to some extent that’s probably good as it frees them up to write
more gameplay code, but there comes a point in every developer’s life
when they have to bite the bullet and find out why their code is slow.
Some day, you’re going to be five weeks from ship and need to claw back
five frames a second on one level of the game that has been optimised in
every other area other than yours. When that day comes, you’d better
know why your code is slow, and to do that, you have to know what the
hardware is doing when it’s executing your code.

Some of the issues surrounding code performance are relevant to all
hardware configurations. Some are only pertinent to configurations that
have caches, or do write combining, or have branch prediction, but some
hardware configurations have very special restrictions that can cause
odd, but simple to fix performance glitches caused by decisions made
during the chip’s design process. These glitches are the gotchas of the
hardware, and as such, need to be learnt in order to be avoided.

When it comes to the overall design of console CPUs, The XBox360 and PS3
are RISC based, low memory speed, multi-core machines, and these do have
a set of considerations that remain somewhat misunderstood by mainstream
game developers. Understanding how these machines differ from the
desktop x86 machines that most programmers start their development life
on, can be highly illuminating. The coming generation of consoles and
other devices will change the hardware considerations again, but
understanding that you do need to consider the hardware can sometimes
only be learned by looking at historic data.

