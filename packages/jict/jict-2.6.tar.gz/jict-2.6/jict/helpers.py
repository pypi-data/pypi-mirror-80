from time import time
from threading import Thread
import os

def evaluate(foo, itter=1 , threaded = False ):

    if threaded == True:
        def threadedfoo():
            Thread(target = lambda: evaluate(foo,itter) ).start()

        threadedfoo()
        return

    t0 = time()
    for _ in range(itter):
        foo()

    print( time() - t0, "seconds wall time" )

def sqlconnect(str):
    if 'mysql-connector' in nolibs:
        raise Exception('strore sql rquieres \'mysql-connector\' module')

    user,pawd,host,database = re.findall(
        "(.*):(.*)@([0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}):(.*)"
    , str )[0]
    cnt = mysql.connector.connect(
        host = host,
        database = database,
        user = user,
        password = pawd
    )
    return cnt


def file( *args, **kwargs ):
    dirname = os.path.dirname(filestr)

    if os.path.isfile( filestr ):
        return open( *args, **kwargs )

    else:
        if not os.path.exists( dirname ):
            os.makedirs( dirname )

        f = open( *args, **kwargs )
        f.write("")
        f.close()

    return open( *args, **kwargs )
