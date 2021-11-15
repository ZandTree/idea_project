import logging

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Max,F
from django_filters.rest_framework import DjangoFilterBackend  # third party
from ideas.models import Idea, UserIdeaRelation
from rest_framework import status, viewsets
from rest_framework.filters import (OrderingFilter,  # built-in filters
                                    SearchFilter)
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from timestamp.broadcast_utils.idea_utils import (checkTagStringLength,
                                                  get_json_tags)

from api.permissions import IsAuthorOrIsStaffOrReadOnly
from api.serializers.ideas.idea_ser import IdeaSerializer
from api.serializers.user_idea_rel.user_idea_relation_ser import \
    UserIdeaRelSerializer

User = get_user_model()
logger = logging.getLogger('django')


class IdeaRelations(RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """to serve objects in through table"""
    queryset = UserIdeaRelation.objects.all()
    serializer_class = UserIdeaRelSerializer
    lookup_field = 'idea'
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_object(self):
        obj, _ = UserIdeaRelation.objects.get_or_create(idea_id=self.kwargs['idea'], user=self.request.user)
        return obj


class IdeaViewSet(viewsets.ModelViewSet):
    """
    custom filter:'title','categ','featured','status','author;
    odrering default: -created at = newest on top
    pagination for tests should be off
    """
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthorOrIsStaffOrReadOnly,)  
    lookup_field = 'slug'
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['featured', 'view_count']
    search_fields = ['title', 'lead_text', 'main_text']
    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('title', 'created_at', 'max_rating','avg_rating')
    # This will be used as the default ordering
    ordering = ('-created_at',)
    # only for testing
    # pagination_class= None

    
    def get_queryset(self):
        #  order_by(F('max_rating').desc(nulls_last=True)) does not change default 
        #  Postgres behaviour is to give NULL a higher sort value 
        
        queryset = Idea.objects.annotate(
            users_comments=Count('comments', distinct=True)                    
        ).select_related('author', 'categ').prefetch_related('tags').order_by(F('max_rating').desc(nulls_last=True))
       
        
        return queryset

    def update(self, request, *args, **kwargs):
        """let op: don't save twice to avoid err msg: file not img||corrupt
        thumbnail may come from front:
        1. as empty string = not img attached or removed
        2. as string = url of aws s3
        3. as InMemoryUploadedFile which needs validation by ser-er         
        """
        idea = self.get_object()
        setattr(request.data, '_mutable', True)
        thumbnail = request.data.get('thumbnail')
        if type(thumbnail) == str and len(thumbnail) != 0:
            request.data.pop('thumbnail')
        if type(thumbnail) == str and len(thumbnail) == 0:
            request.data['remove_file'] = True
        if type(thumbnail) != str:
            request.data['remove_file'] = True
        tags = request.data.get('tags')
        if tags is not None:
            if checkTagStringLength(tags):
                logger.warning(f'status 400: user {self.user.id} loads too long tags')
                return Response({"detail": "tag string is too long; should be max 50 chars"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data['tags'] = get_json_tags(tags)
                setattr(request.data, '_mutable', False)

        serializer = self.get_serializer(idea, data=request.data)
        if serializer.is_valid():
            pass
        else:
            logger.warning(f'status 400: {self.user.id} ser-er idea not valid {serializer.errors}')
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """ create object but before adding auth user to request.data and clean tags input before adding them to data"""
        if request.user.is_banned:
            logger.warning(f'status 403: banned user {request.user.id} create idea ')
            return Response({"error": "user is banned"}, status=status.HTTP_403_FORBIDDEN)
        setattr(request.data, '_mutable', True)
        tags = request.data.get('tags')
        if tags is not None:
            if checkTagStringLength(tags):
                logger.warning(f'status 400: user {request.user.id} loads too long tags')
                return Response({"detail": "tag string is too long; shouls be max 50 chars"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data['tags'] = get_json_tags(tags)
        setattr(request.data, '_mutable', False)
        return super().create(request, *args, **kwargs)
