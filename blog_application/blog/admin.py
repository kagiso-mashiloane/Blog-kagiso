from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('Article_Title', 'author', 'Article_Category', 'created_date', 'published_date')  # Add category to list display
    list_filter = ('Article_Category',)  # Add filter option in the sidebar
    
    # Optionally, customize the fields you want to show in the form for creating/editing a post
    fieldsets = (
        (None, {
            'fields': ('author', 'Article_Title', 'Article_Text', 'Article_Category', 'image')
        }),
        ('Date Information', {
            'fields': ('created_date', 'published_date'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Category) 