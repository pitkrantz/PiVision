moin = [1,2,3,4,4,5]

def check(inputCircles):
    result = []
    for i in inputCircles:
        if i not in result:
            result.append(i)
    return result

print(moin)
moin = check(moin)
print(moin)