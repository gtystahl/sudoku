def createConstraints():
    # This creates the contraints so I dont have to.
    mat = createMatrix()
    ret = []
    for a in range(9):
        row = []
        for b in range(9):
            item = mat[a][b]
            col = []

            # Here is the rows contraints
            for item2 in mat[a]:
                if not item2 in col and item2 != item:
                    col.append(item2)

            # Here is the column constraint
            for i in range(9):
                item2 = mat[i][b]
                if not item2 in col and item2 != item:
                    col.append(item2)

            # Here is the box. A little harder
            y = a // 3
            x = b // 3

            for c in range(3):
                for d in range(3):
                    item2 = mat[(y * 3) + c][(x * 3) + d]
                    if not item2 in col and item2 != item:
                        col.append(item2)
            row.append(col)
        ret.append(row)
    return ret




def createMatrix():
    # This creates the matrix. Will be printed out at the end to be turned in
    letters = "A B C D E F G H I"
    # letters = "A B C D"
    lets = letters.split(" ")
    ret = []
    for let in lets:
        lst = []
        for i in range(1,10):
            lst.append(let + str(i))
        ret.append(lst)
    return ret


def printStuff():
    print(createConstraints())
    print(createMatrix())


if __name__ == "__main__":
    printStuff()