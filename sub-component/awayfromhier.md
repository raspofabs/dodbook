Away from the hierarchy
-----------------------

A recurring theme in articles and post-mortems from people moving from
Object-Oriented hierarchies of gameplay classes to a component based
approach is the transitional states of turning their classes into
containers of smaller objects, an approach often called composition.
This transitional form takes an existing class and finds the boundaries
between the concepts internal to the class and refactors them out into
new classes that can be pointed to by the original class.

First, we move the data out into separate structures so they can be more
easily combined into new classes.

    struct PlayerPhysical {
        Vec pos, up, forward, right;
        Vec velocity;
    };
    struct PlayerGameplay {
        float health;
        int xp;
        int usedPowerups;
        int SPEED, JUMP, STRENGTH, DODGE;
        bool cheating;
    };
    struct EntityAnim {
        AnimID currentAnimGoal;
        AnimID currentAnim;
        SoundHandle playingSoundHandle; // null most of the time
    };
    struct PlayerControl {
        int controller;
        bool controllable;
    };
    struct EntityRender {
        bool visible;
        AssetID playerModel;
    };
    struct EntityInWorld {
        LocomotionType currentLocomotiveModel;
    };
    struct Inventory {
        Array<ItemType> inventory;
        int bulletCount;
    };

    SparseArray<PlayerPhysical> phsyicalArray;
    SparseArray<PlayerGameplay> gameplayArray;
    SparseArray<EntityAnim> animArray;
    SparseArray<PlayerControl> controlArray;
    SparseArray<EntityRender> renderArray;
    SparseArray<EntityInWorld> inWorldArray;
    SparseArray<Inventory> inventoryArray;

    class Player {
    public:
        Player();
        ~Player();
        // ...
        // ... the member functions
        // ...
    private:
        int EntityID;
    };

When we do this, we see how a first pass of building a class out of
smaller classes can help organise the data into distinct purpose
oriented collections, but we can also see the reason why a class ends up
being a tangled mess. The rendering functions need access to the
player’s position as well as the model, and the gameplay functions such
as Shoot need access to the inventory as well as setting animations and
dealing damage. Take damage will need access to the animations, health.
Things are already seeming more difficult to handle than expected. But
what’s really happening here is that you can see that code needs to cut
across different pieces of data. With this first pass, we can start to
see that functionality and data don’t belong together.

We move away from the class being a container for the classes
immediately as we can quickly see the benefit of cache locality when
we’re iterating over multiple entities doing related tasks. If we were
iterating over the entities checking for whether they were out of
bullets, and if so setting their animation to reloading, we would only
need to check the EntityID to find the element for each involved entity.

Functionality of a class, or an object, comes from how facts are
manipulated. The relations between the facts are part of the problem
domain, but the facts are only raw data. This separation of fact from
meaning is not possible with an object oriented approach, which is why
every time a fact acquires a new meaning, the meaning has to be
implemented as part of the class containing the fact. Removing the facts
from the class and instead keeping them as separate components has given
us the chance to move away from classes that have meaning, but at the
expense of having to look up facts from different sources.
