# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Node
from .serializers import NodeSerializer


class NodeViewSet(viewsets.ViewSet):
    queryset = Node.objects.all().filter(parent=None)
    serializer_class = NodeSerializer

    def list(self, request):
        return Response(Node.dump_bulk2())

    def post(self, request, *args, **kwargs):
        node_raw = request.data.get('node', {})
        parent_raw = request.data.get('nextParentNode', {})

        try:
            node = Node.objects.get(pk=node_raw.get('id'))
            parent = None

            if (parent_raw):
                parent = Node.objects.get(pk=parent_raw.get('id'))

            node.parent = parent
            node.save()
        except Node.DoesNotExists as e:
            return Response({'success': False, 'message': e.message}, status=400)

        return Response({'success': True})
