from django.contrib import admin
from blogs.models import Blog, Post

class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ('title', 'description', 'user', 'enabled','order','is_highlight')
    search_fields = ['title', 'description']

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        obj.save()

    def queryset(self, request):
        qs = super(BlogAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'user', 'publication_date', 'status', 'enable_comments')
    search_fields = ['title', 'content']
    list_filter = ('status', 'enable_comments')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'enable_comments',
            'status', 'publication_date',
            )
        }),
    )

    class Media:
        js = [
            '/media/jquery/jquery-1.4.2.min.js',
            '/media/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/media/tinymce_setup/tinymce_setup.js',
            #'/media/filebrowser/js/TinyMCEAdmin.js',
        ]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
            obj.blog = request.user.blog
        obj.save()

    def queryset(self, request):
        qs = super(PostAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)

