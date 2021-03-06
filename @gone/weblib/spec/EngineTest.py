"""
testEngine.py - unit tests for weblib.Engine
"""
__ver__="$Id$"

import os
import unittest
import weblib
from weblib import Engine, Request, RequestBuilder
from handy import trim

class EngineTest(unittest.TestCase):

    def setUp(self):
        self.builder = RequestBuilder()

    def test_globals(self):
        myscript = trim(
            """
            import weblib
            assert isinstance(REQ, weblib.Request)
            assert isinstance(RES, weblib.Response)
            assert isinstance(ENG, weblib.Engine)
            """)
        eng = Engine(script=myscript)
        eng.run()
        assert eng.result == Engine.SUCCESS, eng.error
        

    def test_print(self):
        import sys, StringIO
        eng = Engine(script=trim(
            """
            import weblib
            print >> RES, 'this should show'
            print 'this should not'
            """))
        tempout, sys.stdout = sys.stdout, StringIO.StringIO()
        eng.run()
        sys.stdout, tempout = tempout, sys.stdout
        assert eng.response.buffer == "this should show\n", \
               "doesn't grab prints after import weblib!"
        assert tempout.getvalue() == "this should not\n", \
               "doesn't print rest to stdout"


    def test_exit(self):
        try:
            eng = Engine(script="raise SystemExit")
            eng.run()
            gotError = 0
        except SystemExit:
            gotError = 1
        assert not gotError, "Engine doesn't trap sys.exit()!"


    def test_runtwice(self):
        eng = Engine(script='print >> RES, "hello"')
        eng.run()
        try:
            eng.run()
            gotError = 0 
        except:
            gotError = 1
        assert gotError, "you should not be able to use engine twice!"

    def test_on_exit(self):
        """
        engine.do_on_exit(XXX) should remember XXX and call it at end of page.
        """
        def nothing():
            pass
        
        eng = Engine(script="")
        assert len(eng._exitstuff)==0, \
               "exitstuff not empty by default"
        
        eng.do_on_exit(nothing)
        assert len(eng._exitstuff)==1, \
               "do_on_exit doesn't add to exitstuff" 

        eng._exitstuff = []
        
        eng = Engine(script=trim(
            """
            # underscores on next line are just for emacs.. (trim strips them)
        ___ def cleanup():   
                print >> RES, 'wokka wokka wokka'
            ENG.do_on_exit(cleanup)
            """))
        eng.execute(eng.script)
        assert len(eng._exitstuff) == 1, \
               "didn't register exit function: %s" % str(eng._exitstuff)
        eng._exit()
        assert eng.response.buffer=='wokka wokka wokka\n', \
               "got wrong response: %s" % eng.response.buffer
        


    def test_result(self):
        eng = Engine(script='1+1')
        assert eng.result == None, \
               "engine.result doesn't default to None"

        eng.run()
        assert eng.result == eng.SUCCESS, \
               "engine.result doesn't return SUCCESS on success"

        eng = Engine(script="print 'cat' + 5")
        eng.run()
        assert eng.result == eng.EXCEPTION, \
               "engine.result doesn't return EXCEPTION on error."

        eng = Engine("assert 1==0, 'math is working.. :('")
        eng.run()
        assert eng.result == eng.FAILURE, \
               "engine.result doesn't return FAILURE on assertion failure."

        eng = Engine("import weblib; raise weblib.Redirect, 'url?query'")
        eng.run()
        assert eng.result == eng.REDIRECT, \
               "engine.result doesn't return REDIRECT on redirect."

    ## CGI-SPECIFIC (needs to move) ############################

    ## @TODO: this is really a test of Request
    def test_request(self):
        os.environ["QUERY_STRING"]="enginetest"

        engine = Engine(script="")
        assert engine.request.query.string=="enginetest", \
               "engine has wrong default request"
        del engine

        req = self.builder.build(querystring="e=mc2&this=a+test")
        engine = Engine("pass", request=req)
        assert engine.request.query.string=="e=mc2&this=a+test", \
               "engine has wrong passed-in request:" + \
               engine.request.query.string

    #@TODO: move to testRequest
    def test_form(self):
        weblib.MYFORM = {"a":"bcd"}
        try:
            myscript = trim(
                """
                import weblib
                assert REQ.form is weblib.MYFORM, \
                    'request uses wrong form'
                """)
            req = self.builder.build(form=weblib.MYFORM)
            eng = weblib.Engine(request=req, script=myscript)
            eng.run()
            assert eng.result == eng.SUCCESS, eng.result
        finally:
            del weblib.MYFORM

    def test_hadProblem(self):
        e = Engine(script="x = 1"); e.run()
        assert not e.hadProblem()
        e = Engine(script="raise hell"); e.run()
        assert e.hadProblem()
        e = Engine(script="assert 0"); e.run()
        assert e.hadProblem()


    def test__main__(self):
        e = Engine(script=trim(
            """
            if __name__=='__main__':
               print >> RES, 'sup?'
            """))
        e.run()
        assert e.response.buffer =="sup?\n"
        
            

    # engine needs to set pathinfo so that response
    # can redirect to ?lsakdfjlsdkafj
    # scripts should not pull it out of os.environ
    # because that won't work for twisted
    # instead, the engine for each service should
    # do this. (twisted, cgi, etc...)
    def test_pathInfo(self):
        eng = Engine(script=open("spec/pathinfo.app"))
        assert eng.request.pathInfo == "spec/pathinfo.app", \
               "Engine doesn't set .pathInfo correctly for open()ed scripts."


    def test_redirectToQuerystring(self):
        eng = Engine("import weblib; raise weblib.Redirect('?x=1')",
                     request=RequestBuilder().build(path="test.app"))
        eng.run()
        assert ('Location', 'test.app?x=1') in eng.response.headers

    
