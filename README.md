# Karnaugh Map solver

Minimize a boolean expression using kmaps, works for any number of bits.

Works like this:

1. Find all possible "islands" of 1's.
2. Find all the possible groups we can make.
3. Remove the redundant groups.
4. Check all possible combinations, to find the minimum group.
