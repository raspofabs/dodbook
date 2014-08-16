Structs of Arrays
-----------------

In addition to all the other benefits of keeping your runtime data in a
database style format, there is the opportunity to take advantage of
structures of arrays rather than arrays of structures. SoA has been
coined as a term to describe an access pattern for object data. It is
okay to keep hot and cold data side by side in an SoA object as data is
pulled into the cache by necessity rather than by accidental physical
location.

If your animation timekey/value class resembles this:

    struct Keyframe
    {
        float time, x,y,z;
    };
    struct Stream
    {
        Keyframe *keyframes;
    };

[src:animstruct]

then when you iterate over a large collection of them, all the data has
to be pulled into the cache at once. If we assume that a cacheline is
128 bytes, and the size of floats is 4 bytes, the Keyframe struct is 16
bytes. This means that every time you look up a key time, you
accidentally pull in four keys and all the associated keyframe data. If
you are doing a binary search of a 128 key stream, that could mean you
end up loading 128bytes of data and only using 4 bytes of it in up to 6
chops. If you change the data layout so that the searching takes place
in one array, and the data is stored separately, then you get structures
that look like this:

~~~~ {caption="struct" of="" arrays=""}
struct KeyData
{
    float x,y,z;
};
struct stream
{
    float *times;
    KeyData *values;
};
~~~~

[src:SoAclass]

Doing this means that for a 128 key stream, a binary search is going to
pull in at most three out of four cachelines, and the data lookup is
guaranteed to only require one.

Database technology also saw this, it’s called column oriented databases
and the provide better throughput for data processing over traditional
row oriented relational databases simply because irrelevant data is not
loaded when doing column aggregations or filtering.

