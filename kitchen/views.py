from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from kitchen.forms import (
    CookCreationForm,
    CookUpdateForm,
    DishTypeSearchForm,
    DishSearchForm,
    CookSearchForm,
    DishForm
)
from kitchen.models import Cook, Dish, DishType


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 5
    queryset = DishType.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        name = self.request.GET.get("name", "")

        context = super(DishTypeListView, self).get_context_data(**kwargs)
        context["search_form"] = DishTypeSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = DishTypeSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5
    queryset = Dish.objects.all().select_related("dish_type")

    def get_context_data(self, *, object_list=None, **kwargs):
        name = self.request.GET.get("name", "")

        context = super(DishListView, self).get_context_data(**kwargs)
        context["search_form"] = DishSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5
    queryset = Cook.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        username = self.request.GET.get("username", "")

        context = super(CookListView, self).get_context_data(**kwargs)
        context["search_form"] = CookSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        form = CookSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return self.queryset


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


def manage_cook(request, pk):
    user = get_user_model().objects.get(id=request.user.id)
    dish = Dish.objects.get(id=pk)

    if user in dish.cooks.all():
        dish.cooks.remove(user)
    else:
        dish.cooks.add(user)

    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
