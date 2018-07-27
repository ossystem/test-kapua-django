# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.db import models
from treebeard.mp_tree import MP_Node, get_result_class


class Node(MP_Node):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True)

    node_order_by = ['path']

    def __unicode__(self):
        return 'Node: %s' % self.title

    @classmethod
    def dump_bulk2(cls, parent=None, keep_ids=True):
        """Dumps a tree branch to a python data structure."""

        cls = get_result_class(cls)

        # Because of fix_tree, this method assumes that the depth
        # and numchild properties in the nodes can be incorrect,
        # so no helper methods are used
        qset = cls._get_serializable_model().objects.all()
        if parent:
            qset = qset.filter(path__startswith=parent.path)
        ret, lnk = [], {}
        for pyobj in serializers.serialize('python', qset):
            # django's serializer stores the attributes in 'fields'
            fields = pyobj['fields']
            path = fields['path']
            depth = int(len(path) / cls.steplen)
            # this will be useless in load_bulk
            del fields['depth']
            del fields['path']
            del fields['numchild']
            if 'id' in fields:
                # this happens immediately after a load_bulk
                del fields['id']

            newobj = fields
            if keep_ids:
                newobj['id'] = pyobj['pk']

            if (not parent and depth == 1) or\
               (parent and len(path) == len(parent.path)):
                ret.append(newobj)
            else:
                parentpath = cls._get_basepath(path, depth - 1)
                parentobj = lnk[parentpath]
                if 'children' not in parentobj:
                    parentobj['children'] = []
                parentobj['children'].append(newobj)
            lnk[path] = newobj
        return ret
