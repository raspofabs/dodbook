Finding random is a hash/tree issue
-----------------------------------

For some tables, the values change very often. For a tree representation
to be high performance, it’s best not to have a high number of
modifications as each one could trigger the need for a rebalance. Of
course, if you do all your modifications in one stage of processing,
then rebalance, and then all your reads in another, then you’re probably
going to be okay still using a tree. If you have many different queries
on some data, you can end up with multiple different indexes. How
frequently the entries are changed should influence how you store your
index data. Keeping a tree around for each query could become expensive,
but would be cheaper than a hash table in most implementations. Hash
tables become cheaper where there are many modifications interspersed
with lookups, trees are cheaper where the data is mostly static, or at
least hangs around for a while. When the data becomes constant, a
perfect hash can trump a tree. Trees can be quickly made from data,
faster than hash tables which need you to run a hash function per entry
being inserted. Hash tables can be quickly updated and can take up only
marginally more space than trees if implemented with care. Perfect hash
tables use precalculated hash functions to generate an index, and don’t
require any space other than is used to store the constants and the
array of pointers or offsets into the original table. If you have the
time, then you might find a perfect hash that returns the actual
indexes. I’m not sure we have that long though.

For example, if we need to find the position of someone given their
gamertag, the players won’t be sorted by gamertag normally, so we need a
gamertag to player lookup. This data is mostly constant during game so
would be better suited to a tree or perfect hash if we could generate
one fast enough. Generally, people leave games and join them, so a tree
is probably as static a container as is sensible to use. Given the
number of players isn’t likely to go over a ten thousand at any point, a
trie based off the gamertag hash value should provide very quick lookup.

A hash can be more useful when the table is more chaotic, for example,
messages have senders and recipients. If we need to do something with
all the messages from or to one sender or recipient, then at least one
of those is not going to be the normal sorted order of the table.
Because the table is in constant flux, keeping a tree is virtually
useless, also the hash table variant can handle multiple entries with
the same key a lot easier than a tree implementation as it can use the
standard linked list of entries in a hash bucket to collect all the
messages with a certain sender/recipient.
