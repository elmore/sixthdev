
import zdc
import zikebase

class Node(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikebase.dbc, "base_node")
    _tuples = ["crumbs", "children"] # @TODO: clean this up!

    def _new(self):
        self.__super._new(self)
        self.name = ''
        self.descript = ''
        self.parentID = 0
        self._data['path'] = ''

    def get_crumbs(self):
        #@TODO: how do i handle stuff like this????????????????
        import zikebase
        return map(lambda id: zikebase.Node(ID=id),
                   map(lambda n: n["ID"],
                       self.q_crumbs()))

    def get_children(self):
        #@TODO: clean this junk up and make it a LinkSet!!!!
        import zikebase
        return map(lambda id: zikebase.Node(ID=id),
                   map(lambda n: n["ID"],
                       self.q_children()))
    

    def q_crumbs(self):
        """Returns a list of dicts containing the data for the nodes leading
        down to (but not including) this one."""

        res = []
        node = self
        while node.parentID:
            node = node.parent
            res.append( {"ID": node.ID, "name": node.name, "path": node.path } )

        res.reverse()  # because we want the crumbs to go down, and we went up
        return res
        


    def q_children(self):
        res = []
        cur = self._table.dbc.cursor()
        if self.ID is not None:
            cur.execute("select ID from base_node where parentID=%s" % self.ID)
            for row in cur.fetchall():
                node = Node(ID=row[0])
                res.append( {"ID": node.ID, "name": node.name, "path": node.path } )
        return res


    def set_path(self, value):
        raise TypeError, "path is read only."


    def set_ID(self, value):
        # @TODO: use something like this for generic type checking?
        self.__dict__["ID"] = int(value)
        

    def set_parentID(self, value):
        assert int(value) != self.ID, \
               "A node can't be its own parent!"
        self.__dict__["parentID"]=int(value)
        

    def get_parent(self):
        if self.parentID:
            return Node(ID=self.parentID)
        else:
            return None
            

    def delete(self):
        assert not self.q_children(), \
               "Cannot delete a Node that has children."
        zdc.RecordObject.delete(self)


    def save(self):
        # save ourselves AND the children:
        self._updatePaths(self.parent)
        

    def _updatePaths(self, parent=None):
        # this is a recursive version.. It's probably really slow.
        
        if parent:
            self.__dict__["path"] = parent.path + "/" + self.name
        else:
            self.__dict__["path"] = self.name

        zdc.RecordObject.save(self)
        
        for kid in self.q_children():
            child = Node(ID=kid["ID"]) # @TODO: maybe the object version IS better?
            child._updatePaths(parent=self)
            child.save()  
