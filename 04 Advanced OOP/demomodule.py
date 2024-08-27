
def square(x):
    return x**2

print('This is *demomodule.py*. My __name__ is "{}".'.format(__name__))

if __name__ == '__main__':
    print('This is *demomodule.py*. I was executed as main program.')
    print('This is *demomodule.py*. Running test: calculating square(2):')
    print(square(2))
