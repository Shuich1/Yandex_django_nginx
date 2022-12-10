from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type').annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(persons__personfilmwork__role='actor')
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(persons__personfilmwork__role='director')
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(persons__personfilmwork__role='writer')
                ),
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    paginate_by = 50
    http_method_names = ['get']

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    model = Filmwork
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        return self.get_queryset().get(id=self.kwargs['pk'])
