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

