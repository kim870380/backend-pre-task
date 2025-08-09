from rest_framework import viewsets, filters
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.pagination import CursorPagination
from .models import Contact, Label
from .serializers import (
    ContactListSerializer,
    ContactDetailSerializer,
    ContactCreateUpdateSerializer,
    LabelSerializer,
)

class ContactCursorPagination(CursorPagination):
    page_size = 20
    ordering = 'created_at'
    cursor_query_param = 'cursor'
    
class LabelViewSet(viewsets.ModelViewSet):
    """
    list:   GET  /contact-label/
    create: POST /contact-label/
    retrieve: GET /contact-label/{id}/
    destroy: DELETE /contact-label/{id}/
    """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    

class ContactViewSet(viewsets.ModelViewSet):
    """
    list:   GET  /contact/?ordering=name|email|phone
    create: POST /contact/
    detail: GET /contact/{id}/
    update: PUT /contact/{id}/
    delete: DELETE /contact/{id}/
    """
    queryset = Contact.objects.all().order_by('created_at', 'id')
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    parser_classes   = [JSONParser, FormParser, MultiPartParser]
    pagination_class = ContactCursorPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'email', 'phone']

    ordering = ['created_at', 'id']

    def get_serializer_class(self):
        if self.action == 'list':
            return ContactListSerializer
        if self.action == 'retrieve':
            return ContactDetailSerializer
        return ContactCreateUpdateSerializer
