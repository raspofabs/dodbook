Finding lowest or highest is a sorting problem
----------------------------------------------

In some circumstances you don’t even really need to search. If the
reason for searching is to find something within a range, such as
finding the closest food, or shelter, or cover, then the problem isn’t
really one of searching, but one of sorting. In the first few runs of a
query, the search might literally do a real search to find the results,
but if it’s run often enough, there is no reason not to promote the
query to a runtime updating sorted subset of some other tables’ data. If
you need the nearest three elements, then you keep a sorted list of the
nearest three elements, and when an element has an update, insertion or
deletion, you can update the sorted three with that information. For
insertions or modifications that bring elements that are not in the set
closer, you can check that the element is closer and pop the lowest
before adding the new element to the sorted best. If there is a
deletion, or a modification that makes one in the sorted set a contender
for elimination, a quick check of the rest of the elements to find a new
best set might be necessary. If you keep a larger than necessary set of
best values, however, then you might find that this never happens.

~~~~ {caption="keeping" more="" than="" you="" need=""}
Array<int> bigArray;
Array<int> bestValue;
const int LIMIT = 3;

void AddValue( int newValue ) {
    bigArray.push( newValue );
    bestValue.sortedinsert( newValue );
    if( bestValue.size() > LIMIT )
        bestValue.erase(bestValue.begin());
}
void RemoveValue( int deletedValue ) {
    bigArray.remove( deletedValue );
    bestValue.remove( deletedValue );
}
int GetBestValue() {
    if( bestValue.size() ) {
        return bestValue.top();
    } else {
        int best = bigArray.findbest();
        bestvalue.push( best );
        return best;
    }
}
~~~~

The trick is to find, at runtime, the best value to use that covers the
solution requirement. The only way to do that is to check the data at
runtime. For this, either keep logs, or run the tests with dynamic
resizing based on feedback from the table’s query optimiser.

