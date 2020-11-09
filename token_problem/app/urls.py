from django.urls import path
from app.views import (
    GenerateToken,
    TokenList,
    AssignToken,
    KeepAlive,
    DeallocateToken,
    DeleteToken,
)


urlpatterns = [
    path("generate-token/", GenerateToken.as_view(), name="generate-token"),
    path("token-list/", TokenList.as_view(), name="token-list"),
    path("assign-token/", AssignToken.as_view(), name="assign-token"),
    path("keep-alive/", KeepAlive.as_view(), name="keep-alive/"),
    path(
        "deallocate-token/<str:pk>/", DeallocateToken.as_view(), name="deallocate-token"
    ),
    path("delete-token/<str:pk>/", DeleteToken.as_view(), name="delete-token"),
]
