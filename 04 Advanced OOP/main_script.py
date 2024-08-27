import demomodule


if __name__ == '__main__':
    print('This is *main_script.py*. My __name__ is "{}".'.format(__name__))
    print('This is *main_script.py*. I imported demomodule with __name__ "{}".'.format(demomodule.__name__))
    print('This is *main_script.py*. Computing the squares up to 400:')
    
    for i in range(21):
        print(demomodule.square(i), end=' ')
