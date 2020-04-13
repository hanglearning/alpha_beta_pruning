## Sample Run
```$ python alpha_beta_pruning.py "4 6 7 9 1 2 0 1 8 1 9 2"```</br>
```$ 3 6 7 11```</br></br>
Result veried in https://www.youtube.com/watch?v=xBXHtz4Gbdo

## Other References
https://www.youtube.com/watch?v=v6RgZBjc8og </br>
https://www.youtube.com/watch?v=zp3VMe0Jpf8

# Programming description:

The tree structure is fixed and is shown in the figure below. You need to write a program that receives 12 numbers separated by space from the user. The 12 input numbers will correspond to the 12 terminal nodes of the tree from left to right. Your program should print the index of the terminal states that will be pruned using the alpha-beta search algorithm. The indexes are fixed and are shown in the figure below (0 to 11). As an example case, if the middle red triangle should be pruned completely, your program must print: “4 5 6 7” referring to the four terminal nodes below that node.

![Image of TreeStructure](https://i.imgur.com/FAeTVmd.png)
