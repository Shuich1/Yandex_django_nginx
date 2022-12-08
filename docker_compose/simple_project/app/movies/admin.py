from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork
from django.utils.translation import gettext_lazy as _


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('name', 'description')


class RatingListFilter(admin.SimpleListFilter):
    title = _('rating ')

    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('1-2', _('1-2')),
            ('3-4', _('3-4')),
            ('5-6', _('5-6')),
            ('7-8', _('7-8')),
            ('9-10', _('9-10')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1-2':
            return queryset.filter(rating__range=[1, 2])
        if self.value() == '3-4':
            return queryset.filter(rating__range=[3, 4])
        if self.value() == '5-6':
            return queryset.filter(rating__range=[5, 6])
        if self.value() == '7-8':
            return queryset.filter(rating__range=[7, 8])
        if self.value() == '9-10':
            return queryset.filter(rating__range=[9, 10])


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'creation_date', 'rating',)
    list_filter = ('type', 'creation_date', RatingListFilter, )
    search_fields = ('title', 'description', 'id')
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('full_name',)
