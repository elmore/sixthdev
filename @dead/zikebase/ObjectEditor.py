"""
A class for editing zdc.Objects

$Id$
"""
import weblib

class ObjectEditor(weblib.Actor):
    """A class for editing descendents of zdc.Object"""

    ## attributes ########################################

    what   = None # what class?
    object = None # an instance of the class
    input  = {}

    ## constructor #######################################

    def __init__(self, what, input=None, **args):
        """ex: objed=ObjectEditor(Person, fName="fred", lName="smith")"""
        weblib.Actor.__init__(self, input)
        self.what = what
        self.object = apply(self.newObject, (), args)


    ## public methods ####################################

    def newObject(self, **which):
        """Create a new instance of whatever class we're editing."""
        
        ## this next bit is python magic that will
        ## create a "what" and pass "where" to the
        ## constructor, assigning the result to self.object
        ##
        ## in the example above, objed.object would be
        ## a Person object representing "fred smith".
        
        return apply(self.what, (), which)

    
    def tuplize(self, input):
        if type(input) != type(()):
            return (input)
        else:
            return input


    ## actions ###########################################

    def act_delete(self):
        self.object.delete()
        self.object = self.newObject()
        

    def act_save(self):
        import string
        
        expected = {}
        __expect__ = self.input.get("__expect__", ())
        if type(__expect__) == type(""):
            field, value = string.split(__expect__, ";")
            expected[field]=value
        else:
            # it's a tuple
            for item in __expect__:
                field, value = string.split(item, ";")
                expected[field] = value
                
        for field in self.object.getEditableAttrs():
            if self.input.has_key(field):
                setattr(self.object, field, self.input[field])
            elif expected.has_key(field):
                setattr(self.object, field, expected[field])

        #@TODO: get rid of editable tuples, or add __expect__
        for field in self.object.getEditableTuples():
            if self.input.has_key(field):
                setattr(self.object, field, self.tuplize(self.input[field]))
        self.object.save()

