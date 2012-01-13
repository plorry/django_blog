from django.contrib import admin
from blog.models import Blog, Comment
from gallery.models import Gallery, Image

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'body','creation_date')
	list_filter = ('creation_date',)
	ordering = ('-creation_date',)
	
admin.site.register(Blog, BlogAdmin)
admin.site.register(Gallery)
admin.site.register(Image)
admin.site.register(Comment)