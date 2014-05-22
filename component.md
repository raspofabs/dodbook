Component Based Objects
=======================

Component oriented design is a good head start for high level
data-oriented design. Components put your mind in the right frame for
not linking together concepts when they don’t need to be, and component
based objects can easily be processed by type, not by instance, which
leads to a smoother processing profile. Component based entity systems
are found in games development as a way to provide a data-driven
functionality system for entities, which can allow for designer control
over what would normally be the realm of a programmer. Not only are
component based entities better for rapid design changes, but they also
stymie the chances of the components getting bogged down into monolithic
objects as most game designers would demand more components with new
features over extending the scope of existing components. Most new
designs need iterating, and extending an existing component by code
doesn’t allow design to change back and forth, trying different things.

When people talk about how to create compound objects, sometimes they
talk about using components to make up an object. Though this is better
than a monolithic class, it is not component based approach, it merely
uses components to make the object more readable, and potentially more
reusable. Component based turns the idea of how you define an object on
its head. The normal approach to defining an object in object oriented
design is to name it, then fill out the details as and when they become
necessary. For example, your car object is defined as a Car, if not
extending Vehicle, then at least including some data about what physics
and meshes are needed, with construction arguments for wheels and body
shell model assets etc, possibly changing class dependent on whether
it’s an AI or player car. In component oriented design, component based
objects aren’t so rigidly defined, and don’t so much become defined
after they are named, as much as a definition is selected or compiled,
and then tagged with a name if necessary. For example, instancing a
physics component with four wheel physics, instancing a renderable for
each part (wheels, shell, suspension) adding an AI or player component
to control the inputs for the physics component, all adds up to
something which we can tag as a Car, or leave as is and it becomes
something implicit rather than explicit and immutable.

A component based object is nothing more than the sum of its parts. This
means that the definition of a component based object is also nothing
more than an inventory with some construction arguments. This object or
definition agnostic approach makes refactoring and redesigning a
completely trivial exercise.

Components in the wild
----------------------

Component based approaches to development have been tried and tested.
Many high profile studios have used component driven entity systems to
great success[^1], and this was in part due to their developer’s
unspoken understanding that objects aren’t a good place to store all
your data and traits. Gas Powered Games’ Dungeon Siege Architecture is
probably the earliest published document about a game company using a
component based approach. If you get a chance, you should read the
article[^2]. In the article it explains that using components means that
the entity type[^3] doesn’t need to have the ability to do anything.
Instead, all the attributes and functionality come from the components
of which the entity is made.

In this section we’ll show how we can take an existing class and rewrite
it in a component based fashion. We’re going to tackle a fairly typical
complex object, the player class. Normally these classes get messy and
out of hand quite quickly, and we’re going to assume it’s a player class
designed for a generic 3rd person action game, and take a typically
messy class as our starting point.

~~~~ {caption="Player" class=""}
class Player {
public:
    Player();
    ~Player();
    Vec GetPos(); // the root node position
    void SetPos( Vec ); // for spawning
    Vec GetSpeed(); // current velocity
    float GetHealth();
    bool IsDead();
    int GetPadIndex(); // the player pad controlling me
    float GetAngle(); // the direction the player is pointing 
    void SetAnimGoal( ... ); // push state to anim-tree
    void Shoot( Vec target ); // fire the player's weapon
    void TakeDamage( ... ); // take some health off, maybe animate for the damage reaction
    void Speak( ... ); // cause the player to start audio/anim
    void SetControllable( bool ); // no control in cut-scene
    void SetVisible( bool ); // hide when loading / streaming
    void SetModel( ... ); // init streaming the meshes etc
    bool IsReadyForRender();
    void Render(); // put this in the render queue
    bool IsControllable(); // player can move about?
    bool IsAiming(); // in normal move-mode, or aim-mode
    bool IsClimbing();
    bool InWater(); // if the root bone is underwater
    bool IsFalling();
    void SetBulletCount( int ); // reload is -1
    void AddItem( ... ); // inventory items
    void UseItem( ... );
    bool HaveItem( ... );
    void AddXP( int ); // not really XP, but used to indicate when we let the player power-up
    int GetLevel(); // not really level, power-up count
    int GetNumPowerups(); // how many we've used
    float GetPlayerSpeed(); // how fast the player can go
    float GetJumpHeight();
    float GetStrength(); // for melee attacks and climb speed
    float GetDodge(); // avoiding bullets
    bool IsInBounds( Bound ); // in trigger zone?
    void SetGodMode( bool ); // cheater
private:
    Vec pos, up, forward, right;
    Vec velocity;
    Array<ItemType> inventory;
    float health;
    int controller;
    AnimID currentAnimGoal;
    AnimID currentAnim;
    int bulletCount;
    SoundHandle playingSoundHandle; // null most of the time
    bool controllable;
    bool visible;
    AssetID playerModel;
    LocomotionType currentLocomotiveModel;
    int xp;
    int usedPowerups;
    int SPEED, JUMP, STRENGTH, DODGE;
    bool cheating;
};
~~~~

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

Towards Managers
----------------

After splitting your classes up into components, you might find that
your classes look more awkward now they are accessing variables hidden
away in new structures. But it’s not your classes that should be looking
up variables, but instead transforms on the classes. A common operation
such as rendering requires the position and the model information, but
it also requires access to the renderer. Such global access is seen as a
common compromise during most game development, but here it can be seen
as the method by which we move away from a class centric approach to
transforming our data into render requests that affect the graphics
pipeline without referring to data unimportant to the renderer, and how
we don’t need a controller to fire a shot.

    class RenderManager {
        void Update() {
            foreach( {index,pos} in positionArray ) {
                if( index in renderArray ) {
                    ModelID mid = renderArray[ index ].playerModel;
                    gRenderer.AddModel( mid, pos );
                }
            }
        }
    }
    class PhysicsManager {
        void Update() {
            foreach( {index,pos} in positionArray ) {
                if( index in renderArray ) {
                    ModelID mid = renderArray[ index ].playerModel;
                    ApplyCollisionAndResponse( pos.position, pos.velocity
                }
            }
        }
    }
    class PlayerControl {
        void Update() {
            foreach( {index,control} in controlArray ) {
                if( control.controllable ) {
                    Pad pad = GetPad( control.controller );
                    if( pad.IsPressed( SHOOT ) ) {
                        if( index in inventoryArray ) {
                            if( inventoryArray[ index ].bulletCount > 0 ) {
                                if( index in animArray ) {
                                    animArray[ index ].currentAnimGoal = SHOOT_ONCE;
                                }
                            }
                        }
                    }
                }
            }
            foreach( {index,inv} in inventoryArray )  {
                if( inv.bulletCount > 0 ) {
                    if( index in animArray ) {
                        anim = animArray[ index ];
                        if( anim.currentAnim == SHOOT_ONCE ) {
                            anim.currentAnim = SHOT;
                            inventoryArray[index].bulletCount -= 1;
                            anim.playingSoundHandle = PlaySound( GUNFIRE );
                        }
                    }
                }
            }
        }
    }

What happens when we let more than just the player use these arrays?
Normally we’d have some separate logic for handling player fire until we
refactored the weapons to be generic weapons with NPCs using the same
code for weapons proably by having a new weapon class that can be
pointed to by the player or an NPC, but instead what we have here is a
way to split off the weapon firing code in such a way as to allow the
player and the NPC to share firing code without inventing a new class to
hold the firing. In fact, what we’ve done is split the firing up into
the different tasks that it really contains.

Tasks are good for parallel processing, and with component based objects
we open up the opportunity to make most of our previously class oriented
processes into more generic tasks that can be dished out to whatever CPU
or co-processor can handle them.

There is no Entity
------------------

What happens when we completely remove the player class? If we consider
that an entity may be not only represented by it’s collection of
components, but also might only be it’s current configuration of
components, then there is the possibility of removing the core class of
Player. Removing this class can mean we no longer think of the player as
being the centre of the game, but also the class no longer existing
means that any code is no longer tied to itself.

    struct Orientation { Vec pos, up, forward, right; };
    SparseArray<Orientation> orientationArray;
    SparseArray<Vec> velocityArray;
    SparseArray<float> healthArray;
    SparseArray<int> xpArray, usedPowerupsArray, controllerID, bulletCount;
    struct Attributes { int SPEED, JUMP, STRENGTH, DODGE; };
    SparseArray<Attributes> attributeArray;
    SparseArray<bool> godmodeArray, controllable, isVisible;
    SparseArray<AnimID> currentAnim, animGoal;
    SparseArray<SoundHandle> playingSound;
    SparseArray<AssetID> modelArray;
    SparseArray<LocomotionType> locoModelArray;
    SparseArray<Array<ItemType> > inventoryArray;

    void RenderUpdate() {
        foreach( {index,assetID} in modelArray ) {
            if( index in isVisible ) {
                gRenderer.AddModel( assetID, orientationArray[ index ] );
            }
        }
    }
    void PhysicsUpdate {
        foreach( {index,vel} in velocityArray ) {
            if( index in modelArray ) {
                ApplyCollisionAndResponse( orientationArray[index], vel, modelArray[ index ] );
            }
        }
    }
    void ControlUpdate() {
        foreach( {index,control} in controllerID ) {
            if( controllable[ index ] ) {
                Pad pad = GetPad( control.controller );
                if( pad.IsPressed( SHOOT ) ) {
                    if( inventoryArray[ index ].bulletCount > 0 ) {
                        animArray[ index ].currentAnimGoal = SHOOT_ONCE;
                    }
                }
            }
        }
    }
    void UpdateAnims() {
        foreach( {index, anim} in currentAnim ) {
            if( anim == SHOOT_ONCE ) {
                anim = SHOT;
                inventoryArray[index].bulletCount -= 1;
                playingSound = PlaySound( GUNFIRE );
            }
        }
    }
    int NewPlayer( int padID, Vec startPoint ) {
        int ID = newID();
        controllerID[ ID ] padID;
        GetAsset( "PlayerModel", ID ); // adds a request to put the player model into modelArray[ID]
        orientationArray[ ID ] = Orientation(startPoint);
        velocityArray[ ID ] = VecZero();
        return ID;
    }

Moving away from a player class means that many other classes can be
invented without adding much code. Allowing script to generate new
classes by composition increases the power of script to dramatically
increase the apparent complexity of the game without adding more code.
What is also of major benefit is that all the different entities in the
game now run the same code at the same time. everyone’s physics is
updated before they are rendered[^4] and everyone’s controls (whether
they be player or AI) are updated before they are animated. Having the
managers control when the code is executed is a large part of the leap
towards fully parallelisable code.

[^1]: Gas Powered Games, Looking Glass Studios, Insomniac, Neversoft all
    used component based objects

[^2]: Gas Powered Games released a web article about their component
    based architecture back in 2004, read it at
    http://garage.gaspowered.com/?q=su\_301

[^3]: GPG:DG uses GO or Game-Objects, but we stick with the term entity
    because it has become the standard term.

[^4]: or is updated while the rendering is happening on another thread
