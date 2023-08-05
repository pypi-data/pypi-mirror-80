import redditsfinder

if __name__ == '__main__':  # System arguments. CHANGE TO ARGPARSER

    if len(sys.argv) == 1:
        print('Remember to add a username')
        print('For help enter redditsfinder -h')

    elif len(sys.argv) == 2:

        if sys.argv[-1] == '-h':
            print('redditsfinder.py redditUsername returns every user post')
            print('-pics returns URLs of user's image uploads')
            print('-pics -d downloads  them')
        else:
            redditsfinder.main(sys.argv[-1], [''])

    elif len(sys.argv) >= 3:
        optArgs = [arg for arg in sys.argv[1:-1]]
        redditsfinder.main(sys.argv[-1], optArgs)
