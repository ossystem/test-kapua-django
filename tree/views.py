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
        return Response(Node.dump_bulk2())

    @action(methods=['post'], detail=False)
    def update_tree(self, request, *args, **kwargs):
        root = request.data.get('move', {})
        treeData = root.get('treeData')

        def process_node(node):
            node['data'] = {
                'id': node['id'],
                'title': node['title'],
                'subtitle': node['subtitle'],
                'test_field': node['test_field'],
            }

            if node.get('children'):
                map(process_node, node['children'])

            return node

        try:
            # dangerous. but otherwise tree reordering won't work
            Node.load_bulk(map(process_node, treeData))
        except Exception as e:
            return Response({'success': False, 'message': e.message},
                            status=400)

        return Response({'success': True})
