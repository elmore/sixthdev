class Report:

    def show(self, model={}):
        print self.fetch(model)

    def fetch(self, model={}):
        import copy   # used by scope
        self.model = model
        scope = model
        scope_stack = []
        zres = ""
        import tpl_sslhead
        zres = zres+ tpl_sslhead.fetch(scope)
        import receipt
        zres = zres+ receipt.fetch(scope)
        import tpl_ssslfoot
        zres = zres+ tpl_ssslfoot.fetch(scope)
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
