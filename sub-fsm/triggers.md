Condition tables as Triggers
----------------------------

Sometimes a finite state machine transition has side effects. Some
finite state machines allow you to add callbacks on transitions, so you
can attach onEnter, onExit, and onTransition effects. Because the
transform oriented approach has a natural rhythm of state transforms to
transition request transforms to new state, it’s simple to hook into any
state transition request table and add a little processing before the
state table row modifications are committed.

You can use hooks for logging, telemetry, or game logic that is watching
certain states. If you have a finite state machine for mapping input to
player movement, it’s important to have it react to a player state that
adjusts the control method. For example, if the player has different
controls when under water, the onEnter of the inWater state table could
change the player input mapping to allow for floating up or sinking
down. It would also be a good idea to attach any oxygen-level gauge
hooks here to. If there is meant to be a renderable for the
oxygen-level, it should be created by the player entering the inWater
state. It should also be hooked into the inWater onExit transition
table, as it will probably want to reset or begin regenerating at that
point.

One of the greatest benefits of being able to hook into transitions, is
being able to keep track of changes in game state for syncing. If you
are trying to keep a network game sycnronised, knowing exactly what
happened and why can be the difference between a 5 minute and 5 day
debugging session.

