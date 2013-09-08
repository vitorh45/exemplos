# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment
from comments.models import CustomComment

class CustomCommentsAdmin(CommentsAdmin):
    list_display = ('user_name','content_type','show_title','ip_address', 'submit_date', 'comment', 'is_public',)
    actions = ['make_public','unmake_public','delete']

    def get_actions(self, request):
        actions = super(CustomCommentsAdmin, self).get_actions(request)
        actions.pop('approve_comments')
        actions.pop('remove_comments')
        actions.pop('flag_comments')
        return actions

    def make_public(self, request, queryset):
        rows_updated = queryset.update(is_public=True)
        if rows_updated == 1:
            message_bit = u"1 comentário foi"
        else:
            message_bit = u"%s comentários foram" % rows_updated
        self.message_user(request, u"%s marcado(s) como Público com sucesso." % message_bit)
    make_public.short_description = u"Marcar comentários selecionados como públicos"

    def unmake_public(self, request, queryset):
        rows_updated = queryset.update(is_public=False)
        if rows_updated == 1:
            message_bit = u"1 comentário foi"
        else:
            message_bit = u"%s comentários foram" % rows_updated
        self.message_user(request, u"%s desmarcado(s) como Público com sucesso." % message_bit)
    unmake_public.short_description = u"Desmarcar comentários selecionados como públicos"

    def delete(self, request, queryset):
        rows_updated = queryset.delete()
        if rows_updated == 1:
            message_bit = u"1 comentário foi"
        else:
            message_bit = u"%s comentários foram" % rows_updated
        self.message_user(request, u"%s deletados com sucesso." % message_bit)
    delete.short_description = u"Deletar comentários selecionados"

    def show_title(self, obj):
        return obj.content_object.title
    show_title.short_description = 'Título'

admin.site.unregister(Comment)
admin.site.register(CustomComment, CustomCommentsAdmin)

