#
# testAuth.py - unit tests for Auth.py
#

import unittest
import weblib
import string
from ziketools import trim                                                         

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # auth requires a PATH_INFO variable.. otherwise,
        # it doesn't know where to redirect the form.
        self.myReq = weblib.Request(environ={"PATH_INFO":"dummy.py"})


    def check_engine(self):
        auth = weblib.Auth()
        assert auth.engine==weblib, "auth.engine doesn't default to weblib. :/"
        assert weblib.auth is auth, "auth doesn't register itself with weblib"


    def check_check(self):

        engine = weblib.Engine(request=self.myReq,
                               script="import weblib; weblib.auth.check()" )
        engine.run()

        assert string.find(engine.response.buffer, weblib.Auth.PLEASELOGIN), \
               "check doesn't show login screen"
        

    def check_prompt(self):
        engine = weblib.Engine(request=self.myReq, script=trim(
            """
            from weblib import auth
            auth.check()
            print "hello"
            """))
        engine.run()

        assert string.find(engine.response.buffer, engine.auth.PLEASELOGIN) > -1, \
               "doesn't show prompt!"


    def nocheck_Login(self):
        pass

    def nocheck_Logout(self):
        pass

    def nocheck_Fetch(self):
        pass

    def nocheck_Validate(self):
        pass

    def nocheck_EncodeNormal(self):
        pass

    def nocheck_EncodePassword(self):
        pass
    
    def nocheck_Recovery(self):
        pass

    def nocheck_Persistence(self):
        pass
    
    def tearDown(self):
        pass
        #del self.auth 

