from django.urls import path, include
from rest_framework import routers

from api.views_pack.views import (IdeasPerCategListView, IdeasPerCategListView,
                                  IdeasFollowing, TagIdeasListSlug)

from api.views_pack.tags_views import TagList, TagIdeasListName
from api.views_pack.categs_views import CatListIdeaForm, CategoryList

from api.views_pack.profile_views import (
    ProfileRetrUpdateDestroyView, ProfileRetrView,
    ShowFollowingRetrView,
    RetrieveFollowers, UnFollowUser, FollowAuthorView,
)
from api.views_pack.comment_views import CommentAPIView, CommentListView
from api.views_pack.viewsets import IdeaViewSet, IdeaRelations

router = routers.DefaultRouter()

router.register(r'relations', IdeaRelations)  # ,basename='useridearelation')
router.register(r'ideas', IdeaViewSet, basename="idea")
router.register(r'comments', CommentAPIView, basename='comment')

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories-create-idea/', CatListIdeaForm.as_view(), name='category-create-idea'),
    path('cats/<slug>/', IdeasPerCategListView.as_view(), name="cat-per-idea"),
    path('ideas-collection/', include(router.urls)),
    path('feed-ideas/<unid>/', IdeasFollowing.as_view(), name='user-following-ideas'),
    # private api for profile,userinfo (profile + user)
    path('profile-owner/<unid>/', ProfileRetrUpdateDestroyView.as_view(), name="profile-owner"),
    # public api profile
    path('profile-info/<pk>/', ProfileRetrView.as_view(), name="profile-info"),
    # tags
    path('tags/', TagList.as_view(), name="tags-list"),
    path('tags/<slug>/', TagIdeasListSlug.as_view(), name="tag-per-ideas-slug"),
    path('tags-name/<name>/', TagIdeasListName.as_view(), name="tag-per-ideas-name"),
    # following smb
    path('following/<unid>/', ShowFollowingRetrView.as_view(), name='show-following'),
    path('followers/<id>/', RetrieveFollowers.as_view(), name='show-followers'),
    path('unfollow/', UnFollowUser.as_view(), name='unfollow-user'),
    path('add-following/', FollowAuthorView.as_view(), name='add-to-following'),
    # fetch all comments
    path('idea/comments/<slug>/', CommentListView.as_view(), name='fetch-comments')

]
