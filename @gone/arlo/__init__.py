"""
arlo: an object-relational mapping system
"""
__ver__="$Id$"

from LinkInjector import *
from LinkSetInjector import *
from Clerk import *
from CallbackClerk import *

def MockClerk(dbmap=None):
    from storage import MockStorage
    return Clerk(MockStorage(), dbmap or AutoSchema())


