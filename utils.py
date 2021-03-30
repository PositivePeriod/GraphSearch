def numToString(num):
    assert type(num) == int and num >= 0
    string = ""
    n = num + 1
    while n > 0:
        n, r = (n - 1) // 26, (n - 1) % 26
        string = chr(65 + r) + string
    return string


if __name__ == "__main__":
    for i in range(40):
        print(numToString(i), end=" ")