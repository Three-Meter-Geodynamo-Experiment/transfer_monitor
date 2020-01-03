global s
s = 'global'
print(s)


def foo2():
    print(s)


def foo():
    global s
    s = 'local'
    print(s)


foo2()

foo()
print(s)

