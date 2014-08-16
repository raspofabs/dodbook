Domain Knowledge
----------------

Every time you find that you’re looking up the answer to a question and
find that though the calculation seems complex, the answer is highly
correlative to only a small subset of the inputs, there’s a chance that
you’re missing some domain knowledge. Sometimes you don’t even need the
answer to a question as the design prescribes an implicit value. These
implicit values, when figured into the code, can reduce a highly complex
function to one that is simple, or better, doesn’t need to run as often.

The full health bar that doesn’t need regenerating is a form of domain
knowledge that lead to existence based processing of the regeneration
code. Code that would otherwise have run without effect now only runs
when required.

Knowing that a compute kernel only affects elements that have differing
values, such as a Gaussian blur, can affect how much time it takes to
process the data. Marking regions of a data-store as potentially able to
be affected by the kernel in a pre-parse can make all the difference,
and can also help split a task across multiple workers.

Experimentation, documentation, and analysis, are the key ingredients to
any real understanding of data transforms. Without looking at the data
that an algorithm is using, and what comes out given that data, there
will never be any hope of insight or improvement.

In one analysis, an assumed to be completely smooth accelerometer
reading was proven to include the jerk vibrations from the force
propelling the sensor. This caused noisy data which increased the
difficulty to complete the intended analysis. Taking this base noise
into account allowed for a much simpler and higher accuracy algorithm.

When trying to find out what was causing a DVD read to run slow, an
analysis was required to find out where the head was while it was
reading. In the data, we found that the game was reading data from where
we expected, but also from a configuration file that was meant to be
read in debug builds. The file wasn’t really being read, but it’s
date-stamp was, which meant that the read head wasn’t where it was meant
to be while streaming, once a second. Without checking the data, there
wouldn’t have been a very good chance to find the bug.

Sometimes domain knowledge comes purely from the design of the game.
Knowing that you can eject the data for an area of the game as a section
is one way only can be a simple memory saver. Knowing that building
cannot return to their fixed state after being destroyed is important
too. For most older games that did allow destructible environments, the
knowledge that the environment didn’t need to be reversible was used to
reduce the memory footprint of the level data. Most games would require
reloading the level before being able to restart as once the structures
were destroyed, especially with procedural destruction, there was no
information on how the building started out. This lack of information
was a space saver, and could have been seen as a form of domain
knowledge.

Other key pieces of data can come from without. Analytics, both from
people playing the game and bots, can provide much needed data. Making a
bot for a single-player game can be very rewarding as it allows you to
run tests for things that would otherwise be too simple and thus too
boring for even the most dedicated testers. For example, running a
frame-rate analysis for a game can be highly tedious, but can provide a
massive amount of beneficial data to both the art team, and the engine
team, as they can look at specific hotspot areas in both the art assets,
and the engine technology. Knowledge of what really happens in the game
in this case leads to optimising only the parts of the game engine that
are really required to produce the game. Without a real analysis of the
performance of the game given the real data, the real game code and a
real run through, any optimisations have to be speculative at best. Even
if you can prove that an area of the engine code is running really
slowly, there’s no point in optimising it if it’s only used in sections
of the game where the engine has plenty of spare resources and doesn’t
need to run any faster. Another reason why running these tests via a bot
is important is that as with all optimisations and refactorings, it’s
important that once you have made your changes you must be able to see
the outcome of those changes, and must be able to prove that you haven’t
broken anything else while changing the code, and that you actually
improved things.

Sometimes it can be hard to run the same test multiple times. Sometimes
your test isn’t entirely deterministic. When that is the case you need
to gather your data more carefully and be aware of the statistical
significance of any data you have. Learn how to determine what
constitutes significant values and can be confirmed as improvement over
the noise inherent in the data you can collect.

