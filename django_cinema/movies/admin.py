from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import *

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("name", "email")



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [ReviewInline]
    save_on_top = True
    actions = ['publish', 'unpublish']
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)

        if row_update == 1:
            message_bit = '1 record has been published'
        else:
            message_bit = f'{row_update} bits have been published'
        self.message_user(request, f'{message_bit}')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)

        if row_update == 1:
            message_bit = '1 record has been unpublished'
        else:
            message_bit = f'{row_update} bits have been unpublished'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Publish'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Unpublish'
    unpublish.allowed_permissions = ('change',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" ')

    get_image.short_description="Image"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")

    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" ')

    get_image.short_description="Image"



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "ip", "movie")


admin.site.register(RatingStar)
# Register your models here.

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"