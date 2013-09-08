from django.conf import settings
from googleanalytics import Connection

def get_analytics_connection():
    connection = Connection('befteranalytics@gmail.com', 's0d4!SODA@')
    #connection = Connection('email', 'senha')
    account = connection.get_accounts()[3]
    return account

def get_filter_for_article():
    filter_for_article = [
        ['pagePath', '=~', '^/noticias/.*/[a-z0-9\-]+' , 'OR']
        #['pagePath', '=~', '^/noticias/.*/.*' , 'OR']
    ]
    return filter_for_article

def get_filter_for_blog():
    filter_for_blog = [
        ['pagePath', '=~', '^/colunistas/[a-z\-]+/[a-z0-9\-]+' , 'OR']
        #['pagePath', '=~', '^/noticias/.*/.*' , 'OR']
    ]
    return filter_for_blog

def get_filter_for_video():
    filter_for_video = [
        ['pagePath', '=~', '^/videos/[a-z0-9]+' , 'OR']
        #['pagePath', '=~', '^/noticias/.*/.*' , 'OR']
    ]
    return filter_for_video

