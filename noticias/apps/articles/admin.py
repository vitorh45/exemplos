from django.contrib import admin
from apps.articles.models import Article, Channel, Section

class ArticleAdmin(admin.ModelAdmin):

    def preview(article):
       return '<ul class="tools"><li><a href="/noticias/%s/%s/preview" class="focus" target="_blank">Preview</a></li></ul>' % (article.channel.slug, article.slug)
    preview.allow_tags = True
    preview.short_description = u'Preview'

    date_hierarchy = 'created_date'
    list_display = ('title', 'channel','section','created_date', 'publication_date', 'status','is_urgent','is_mega_manchete', preview, 'comments_count')
    list_filter = ('status','channel', 'section')
    search_fields = ['title', 'headline', 'summary']
    fieldsets = (
        (None, {
            'fields': ('channel', 'section', 'title','title_secondary','headline', 'summary',
                'content', 'source', 'source_url', 'usermeuclick','author','picture','picture_subtitle','tags_string',
                'status', 'publication_date','is_urgent','is_mega_manchete','enable_comments',
            )
        }),
    )
    class Media:
        js = [

            '/media/js/jquery/jquery-1.4.2.min.js',
            '/media/tinymce/jscripts/tiny_mce/tiny_mce.js',
            #'/media/filebrowser/js/TinyMCEAdmin.js',
            '/media/tinymce_setup/tinymce_setup.js',

        ]
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = kwargs['request'].user.first_name + ' ' + kwargs['request'].user.last_name
            request = kwargs.pop("request", None)
        return super(ArticleAdmin,self).formfield_for_dbfield(db_field,**kwargs)

class ChannelAdmin(admin.ModelAdmin):
    pass

class SectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Section, SectionAdmin)

