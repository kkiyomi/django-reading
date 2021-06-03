from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.utils import timezone

from .models import *


class ParaHomeListView(ListView):
    model = Product
    template_name = 'para/home.html'
    paginate_by = 15 * 2 * 10
    paginate_orphans = 4

    def get_queryset(self):
        return Product.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_date'] = timezone.now
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'para/product.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        slug = self.kwargs['slug']

        try:
            queryset = queryset.filter(slug=slug)
        except Exception as e:
            queryset = queryset.filter(uid=slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = f"{context['object'].name}"
        return context