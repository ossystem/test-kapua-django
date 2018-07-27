# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Node
from .serializers import NodeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    def list(self, request):
        # print(Node.find_problems())
        # print(Node.fix_tree(destructive=True))
        return Response(Node.dump_bulk2())

    @action(methods=['post'], detail=False)
    def update_tree(self, request, *args, **kwargs):
        root = request.data.get('move', {})

        node_raw = root.get('node', {})
        parent_raw = root.get('nextParentNode', {})
        prevPath = root.get('prevPath')
        nextPath = root.get('nextPath')

        try:
            node = Node.objects.get(pk=node_raw.get('id'))
            parent = None

            if len(prevPath) == len(nextPath):
                parent = node
            else:
                if (parent_raw):
                    parent = Node.objects.get(pk=parent_raw.get('id'))


            # node.parent = parent
            # node.move(parent, root.get('nextPath')[-1])
            pos = 'sorted_child'

            # if root.get('treeIndex') > root.get('prevTreeIndex'):
            #     pos = 'right'
            # else:
            #     pos = 'left'

            if parent:
                node.move(parent, pos='sorted-child')
            else:
                raise Exception('there is no parent')
            # node.save()
            Node.fix_tree()
            print(node, parent)
        except Exception as e:
        # except Node.DoesNotExists as e:
            print(e)
            return Response({'success': False, 'message': e.message}, status=400)

        return Response({'success': True})
