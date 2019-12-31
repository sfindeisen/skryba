f_verbose = False

def set_verbose(verbose):
    global f_verbose
    f_verbose = bool(verbose)

def debug(msg):
    global f_verbose
    if (f_verbose):
        print('[debug] {}'.format(msg))

def info(msg):
    print('[info] {}'.format(msg))

def warning(msg):
    print('[warning] {}'.format(msg))
