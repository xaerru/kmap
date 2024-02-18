# Karnaugh Map solver

Minimize a boolean expression using kmaps, works for any number of bits.

In a nutshell:

1. Find all possible "islands"/"floods" of 1's.
2. Find all the possible groups we can make.
3. Remove the redundant groups.
4. Check all possible combinations, to find the minimum group.

In more detail:

1. Iterate through the array of 4x4 kmaps, whenever you find a 1, do a recursive flood fill to find the island of 1. This flood fill can also extend to other 4x4 kmaps in the array.
2. Make a graph of all adjacent 1's while flooding it.
3. Make all such possible floods and add them to a common graph.
4. Now we need to find all possible groups we can make. We know that their length can only be a power of 2. We can easily find the groups of ones(just all the numbers which need to be 1). We can use the edge list of the graph to find out the groups of 2.
5. For groups of length bigger than 2, we iterate through the previous list of groups. For example to find out the possible groups of 4, we would iterate through the possible groups of 2. For each element in the group we find out the adjacent nodes to it which don't belong in the group. Then we just zip all these lists of each element and make a group which may or may not be valid.

6. To check if the group is valid we need to check if there are no repeated elements in the group and check that if each element in the group(let's say index i) has an edge with the element at index i+h. Where h can be 2,4,8,...floor(log2(length of group)). 
7. Now we have all the valid groups, we remove all the groups which are completely overlapped by another group.
8. Then we take the powerset of the list of all the groups and check for the minimum length grouping we can find.
