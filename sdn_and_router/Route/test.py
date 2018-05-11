def clearCircle(newpopIndiv):
    for i in range(len(newpopIndiv)):
        if newpopIndiv.count(newpopIndiv[i]) > 1 and newpopIndiv[i] != -1:
            for j in range(i + 1, len(newpopIndiv)):
                if newpopIndiv[j] == newpopIndiv[i]:
                    newpopIndiv[j] = -1
                    break
                else:
                    newpopIndiv[j] = -1
    for i in range(len(newpopIndiv)):
        if newpopIndiv.count(-1)>0:
            newpopIndiv.remove(-1)
        else:
            break
    print(newpopIndiv)


if __name__ == '__main__':
    print("test")
    clearCircle([1, 3, 5, 2, 3, 7])

