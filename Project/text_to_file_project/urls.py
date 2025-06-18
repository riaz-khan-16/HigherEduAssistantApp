


from django.contrib import admin
from django.urls import path
from textapp.views import make_vecorstore,make_query,add_new_doc,getQuery

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_new/', add_new_doc, name='train'),
    path('make_vectordb/', make_vecorstore, name='vectorstore'),
    path('query/', make_query, name='query'),
    path('get_query/', getQuery, name='get_query'),

]