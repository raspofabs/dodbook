Searching
=========

When looking for specific data, it’s very important to remember why
you’re doing it. If the search is not necessary, then that’s your
biggest possible saving. Finding if a row exists in a table will be slow
if approached naively. You can manually add searching helpers such as
binary trees, hash tables, or just keep your table sorted by using
ordered insertion whenever you add to the table. If you’re looking to do
the latter, this could slow things down, as ordered inserts aren’t
normally concurrent, and adding extra helpers is normally a manual task.
In this section we find ways to combat all these problems.

