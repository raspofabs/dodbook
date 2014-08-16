Joins as intersections
----------------------

Sometimes, normalisation can mean you need to join tables together to
create the right situation for a query. Unlike RDBMS queries, we can
organise our queries much more carefully and use the algorithm from
merge sort to help us zip together two tables. As an alternative, we
don’t have to output to a table, it could be a pass through transform
that takes more than one table and generates a new stream into another
transform. For example, per entityRenderable, join with entityPosition
by entityID, to transform with AddRenderCall( Renderable, Position )

