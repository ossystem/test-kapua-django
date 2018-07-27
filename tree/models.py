# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.db import models
from treebeard.al_tree import AL_Node


class Node(AL_Node):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey('self', related_name='children',
                               null=True, db_index=True)

    sib_order = models.PositiveIntegerField(default=1)
    test_field = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return 'Node: %s' % self.title

    @classmethod
    def dump_bulk2(cls, parent=None, keep_ids=True):
        """Dumps a tree branch to a python data structure."""

        serializable_cls = cls._get_serializable_model()
        if (
                parent and serializable_cls != cls and
                parent.__class__ != serializable_cls
        ):
            parent = serializable_cls.objects.get(pk=parent.pk)

        # a list of nodes: not really a queryset, but it works
        objs = serializable_cls.get_tree(parent)

        ret, lnk = [], {}
        for node, pyobj in zip(objs, serializers.serialize('python', objs)):
            depth = node.get_depth()
            # django's serializer stores the attributes in 'fields'
            fields = pyobj['fields']
            del fields['parent']

            # non-sorted trees have this
            if 'sib_order' in fields:
                del fields['sib_order']

            if 'id' in fields:
                del fields['id']

            newobj = fields
            if keep_ids:
                newobj['id'] = pyobj['pk']

            if (not parent and depth == 1) or\
               (parent and depth == parent.get_depth()):
                ret.append(newobj)
            else:
                parentobj = lnk[node.parent_id]
                if 'children' not in parentobj:
                    parentobj['children'] = []
                parentobj['children'].append(newobj)
            lnk[node.pk] = newobj
        return ret
