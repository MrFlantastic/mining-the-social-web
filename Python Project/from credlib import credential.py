from credlib import credential

def system_login(*args): # this is new function definition
#def system_login(hostname, username, password): # this was previous function definition

    if len(args) == 1 and isinstance(args[0], credential):
        hostname = args[0].hostname
        username = args[0].username
        password = args[0].password
    elif len(args) == 3:
        hostname = args[0]
        username = args[1]
        password = args[2]
    else:
        raise ValueError('Invalid arguments')

    do_login(hostname, username, password) # this is original system login call