"""
Generic class for hierarchical structures.
"""
__ver__="$Id$"

import zdc
import zikebase

class Node(zdc.RecordObject):
    __super = zdc.RecordObject
    _tablename = "base_node"
    _tuples = ["crumbs", "children"] # @TODO: clean this up!

    def _init(self):
        self.__super._init(self)
        self._kids = None

    def _new(self):
        self.__super._new(self)
        self.name = ''
        self.descript = ''
        self._data['parentID'] = 0
        self._data['path'] = ''

    def get_crumbs(self):
        #@TODO: how do i handle stuff like this????????????????
        import zikebase
        return map(lambda id: zikebase.Node(self._ds, ID=id),
                   map(lambda n: n["ID"],
                       self.q_crumbs()))

    def get_children(self):
        if self._kids is None:
            self._kids = zdc.LinkSet(self, zikebase.Node, "parentID")
        return self._kids

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
        #@TODO: raise "q_children is deprecated"
        res = []
        if self.ID is not None:
            res = self._table.select(parentID=self.ID)
        return res


    def set_path(self, value):
        raise TypeError, "path is read only."


    def set_ID(self, value):
        # @TODO: use something like this for generic type checking?
        self._data["ID"] = int(value)
        

    def set_parentID(self, value):
        assert int(value) != self.ID, \
               "A node can't be its own parent!"
        self._data["parentID"]=int(value)
        

    def get_parent(self):
        if self.parentID:
            return Node(self._ds, ID=self.parentID)
        else:
            return None
            

    def delete(self):
        assert len(self.children)==0, \
               "Cannot delete a Node that has children."
        self.__super.delete(self)


    def save(self):
        # _updatePaths saves ourselves AND the children:
        self._updatePaths(self.parent)
        if self._kids is not None:
            self._kids.save()

    def _updatePaths(self, parent=None):
        # this is a recursive version.. It's probably really slow.
        
        if parent:
            self._data["path"] = parent.path + "/" + self.name
        else:
            self._data["path"] = self.name

        self.__super.save(self)
        
        for kid in self.q_children():
            child = Node(self._ds, ID=kid["ID"])
            child._updatePaths(parent=self)
            child.save()  
