from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.models import Cook, Dish, DishType


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


class DishTypeListView(generic.ListView):
    model = DishType
    # context_object_name = "dish_type_list"
    template_name = "kitchen/dishtype_list.html"
    paginate_by = 5
    queryset = DishType.objects.all()


class DishTypeCreateView(generic.CreateView):
    model = DishType
    fields = "__all__"
    paginate_by = 7
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    fields = "__all__"
    paginate_by = 7
    success_url = reverse_lazy("kitchen:dish-type-list")