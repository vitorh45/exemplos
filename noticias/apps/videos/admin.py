from django.contrib import admin
from videos.models import Video

class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title','id_video','duration','publication_date', 'enable_comments','views_count')
    search_fields = ['title', 'content']
    list_filter = ('enable_comments',)
    fieldsets = (
        (None, {
            'fields': ('title', 'headline','content', 'id_video','tags_string','enable_comments',
            'publication_date',
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


admin.site.register(Video, VideoAdmin)

