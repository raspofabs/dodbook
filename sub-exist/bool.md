Don’t use booleans {#sec:exist-bool}
------------------

When you study compression technology, one of the most important aspects
you have to understand is the different between data and information.
There are many ways to store information in systems, from literal
strings that can be parsed to declare that something exists, right down
to something simple like a single bit flag to show that a thing might
have an attributes. Examples include the text that declares the
existence of a local variable in a scripting language, or the bit field
that contains all the different collision types a physics mesh will
respond to. Sometimes we can store even less information than a bit by
using advanced algorithms such as arithmetic encoding, or by utilising
domain knowledge. Domain knowledge normalisation applies in most games
development, but it is very infrequently applied. As information is
encoded in data, and the amount of information encoded can be amplified
by domain knowledge, it’s important that we begin to see the advice
offered by compression techniques is that: all we are really encoding is
probabilities.

If we take an example, a game where the entities have health, regenerate
after a while of not taking damage, can die, can shoot each other, then
lets see what domain knowledge can do to reduce processing.

We assume this domain knowledge: if you have full health, then you don’t
need to regenerate. Once you have been shot, it takes some time until
you begin regenerating. Once you are dead, you cannot regenerate. Once
you are dead you have zero health.

If we have a table for the entity thus:

~~~~ {caption="naive" entity="" table=""}
struct entity {
    // information about the entity position
    // ...
    // now health data in the middle of the entity
    float timeoflastdamage;
    float health;
    // ...
    // other entity information
};
list<entity> entities;
~~~~

Then we can run an update function over the table that might look like
this:

~~~~ {caption="every" entity="" health="" regen=""}
void updatehealth( entity *e ) {
    timetype timesincelastshot = e->timeoflastdamage - currenttime;
    bool ishurt = e->health < max_health && e->health > 0;
    bool regencanstart = timesincelastshot > time_before_regenerating;
    if( ishurt && regencanstart ) {
        e->health = min(max_health, e->health + ticktime * regenrate);
    }
}
~~~~

Which will run for every entity in the game, every update.

We can make this better by looking at the flow control statement. The
function only needs to run if the health is less than full health, and
more than zero. The regenerate function only needs to run if it has been
long enough since the last damage dealt.

Let’s change the structures:

~~~~ {caption="existence" based="" processing="" style="" health=""}
struct entity {
    // information about the entity position
    // ...
    // other entity information
};
struct entitydamage {
    float timeoflastdamage;
    float health;
}
list<entity> entities;
map<entityref,entitydamage> entitydamages;
~~~~

We can now run the update function over the health table rather than the
entities.

~~~~ {caption="every" entity="" health="" regen=""}
void updatehealth() {
    foreach( eh in entitydamages ) {
        entityref entity = eh->first;
        entitydamage &ed = eh->second;
        if( ed.health < 0 ) {
            deadentities.insert( entity );
            discard(eh);
        } else {
            timetype timesincelastshot = eh->timeoflastshot - currenttime;
            bool regencanstart = timesincelastshot > time_before_regenerating;
            if( regencanstart )
                eh->health =eh->health + ticktime * regenrate;
            if( eh->health > max_health )
                discard(eh);
        }
    }
}
~~~~

We only add a new entityhealth element when an entity takes damage. If
an entity takes damage when it already has an entityhealth element, then
it can update the health rather than create a new row, also updating the
time damage was last dealt. If you want to find out someone’s health,
then you only need to look and see if they have an entityhealth row, or
if they have a row in deadentities table. The reason this works is that
an entity has an implicit boolean hidden in the row existing in the
table. For the entityhealth table, that implicit boolean was ishurt from
the first function. For the deadentities table, the implicit boolean of
isdead, also implies a health value of 0, which can reduce processing
for many other systems. If you don’t have to load a float and check that
it is less than 0, then you’re saving a floating point comparison or
conversion to boolean.

Other similar cases include weapon reloading, oxygen levels when
swimming, anything that has a value that runs out, has a maximum, or has
a minimum. Even things like driving speeds of cars. If they are traffic,
then they will spend most of their time driving at <span>*traffic
speed*</span> not some speed that they need to calculate. If you have a
group of people all heading in the same direction, then someone joining
the group can be <span>*intercepting*</span> until they manage to, at
which point they can give up their self and become controlled by the
group.

As an aside, we use a map and a list here for simplicity of reading, and
though they are not the most optimal containers in that they are trees,
or pointers to elements, rather than a nice contiguous array of some
sort, they’re not going to adversely affect the profile as much as the
problem being overcome here, namely the mixing of hot[^1] data into the
middle of the entity class.

[^1]: hot data is the member or members of a class that are accessed
    with high frequency, and there can even be multiple per class.

Another example is with AI. If you have all your entities maintain a
team index, then you have to check each entity before reacting to them.
If you want to avoid all the entities from team x, and head towards the
closest member of team y, then if each team is in a different table you
can just operate on all the entities in those tables. If you want to
produce an avoidance vector from team x, you create a mapreduce function
that maps team x members to an avoidance vector, then reduce by summing.

~~~~ {caption="map" and="" reduce=""}
vector mapavoidance( entity *e ) {
    vector difference = e->pos - currentpos;
    float oneoversqr = 1.0f / difference.getsquaredlength();
    return difference * oneoversqr;
}
vector reduceavoidance( const vector l, const vector r ) {
    return l + r;
}
pair<float,entity*> mapnearest( entity *e ) {
    vector difference = e->pos - currentpos;
    float squaredistance = difference.getsquaredlength();
    return pair<float,entity*>( squaredistance, e );
}
pair<float,entity*> reducenearest( pair<float,entity*> l, pair<float,entity*> r ) {
    if( l.left < r.left ) return l; return r;
}
~~~~

The implicit boolean in these tables is that they are worth avoiding,
and that they are worth aiming towards. If nothing maps, then the
seeding value to the reduce is returned.

Another use is in state management. If an AI hears gunfire, then they
can add a row to a table for when they last heard gunfire, and that can
be used to determine whether they are in a heightened state of
awareness. If an AI has been involved in a transaction with the player,
it is important that they remember what has happened as long as the
player is likely to remember it. If the player has just sold an AI their
+5 longsword, it’s very important that the shopkeeper AI still have it
in stock if the player just pops out of the shop for a moment. Some
games don’t even keep inventory between transactions, and that can
become a sore point if they accidentally sell something they need and
then save their progress.

The general concept of tacking on data, or patching loaded data with
dynamic additional attributes, has been around for quite a while. Save
games often encode the state of a dynamic world as a delta from the base
state, and one of the first major uses was in fully dynamic
environments, where a world is loaded, but can be destroyed or altered
afterwards. Some world generators took a procedural landscape and
allowed their content creators to add patches of extra information,
villages, forts, outposts, or even break out landscaping tools to
drastically adjust the generated data. Taking that patching and applying
it to in-game runtime information adds a level of control not normally
available without using intrusive techniques.

