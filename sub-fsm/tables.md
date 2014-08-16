Tables as States
----------------

If we wish to implement finite state machines without objects to contain
them, and without state variables to instruct their flow, we can call on
the runtime dynamic polymorphism inherent in the data oriented approach
to provide these characteristics based only on the existence of rows in
tables. We do not need an instruction cache trashing state variable that
would divert the flow according to internal state. We don’t need an
object to contain any state dependent data for analysis of the alphabet.

At the fundamental level, a finite state machine requires a reaction to
an alphabet. If we replace the alphabet handling code with condition
tables, then we can produce output tables of transitions to commit. If
each state is represented by a condition table, and any entity in that
state represented by a row in a state table, then we can run each state
in turn, collecting any transitions in buffers, then committing these
changes after everything has finished a single update step.

Finite state machines can be difficult to debug due to their data-driven
nature, so being able to move to a easier to debug framework should
reduce development time. In my experience, being able to log all the
transitions over time has reduced some AI problems down to merely
looking through some logs before fixing an errant condition based only
on an unexpected transion logged with its cause data.

Keeping the state as a table entry can also let the FSM do some more
advanced work, such as managing level of detail or culling. If your
renderables have a state of potentially visible, then you can run the
culling checks on just these entities rather than those not even up for
consideration this frame. Using count lodding with FSMs allows for game
flow logic as allowing the triggering of a game state change to emit the
state’s linked entities could provide a good point for debugging any
problems. Also, using condition tables makes it very easy to change the
reactions and add new alphabet without having to change a lot of code.

