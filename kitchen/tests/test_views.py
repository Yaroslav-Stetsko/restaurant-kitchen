from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Cook, DishType, Dish

DISH_TYPE_URK = reverse("kitchen:dish-type-list")
DISH_TYPE_CREATE_URL = reverse("kitchen:dish-type-create")

DISH_URL = reverse("kitchen:dish-list")
DISH_CREATE_URL = reverse("kitchen:dish-create")


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test", password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_cook(self):

        response = self.client.get(reverse("kitchen:cook-list"))
        cook = Cook.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["cook_list"]), list(cook))
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_create_cook(self):
        form_data = {
            "username": "new_user",
            "password1": "testuser123",
            "password2": "testuser123",
            "years_of_experience": 12,
            "first_name": "First",
            "last_name": "Last",
        }
        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(
            new_user.years_of_experience, form_data["years_of_experience"]
        )

    def test_delete_cook(self):
        new_cook = get_user_model().objects.create_user(
            username="test784", password="Test11qq23", years_of_experience=12
        )
        self.client.force_login(new_cook)
        self.client.post(
            reverse("kitchen:cook-delete", kwargs={"pk": new_cook.id})
        )
        self.assertEqual(Cook.objects.count(), 1)


class PublicDishTypeTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DISH_TYPE_URK)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_dish_type(self):
        DishType.objects.create(
            name="Test1",
        )
        DishType.objects.create(
            name="Test2",
        )

        response = self.client.get(DISH_TYPE_URK)
        dish_type = DishType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dishtype_list"]), list(dish_type)
        )
        self.assertTemplateUsed(response, "kitchen/dishtype_list.html")

    def test_create_dish_type(self):
        form_data = {
            "name": "Test3",
        }

        self.client.post(DISH_TYPE_CREATE_URL, data=form_data)
        new_dish_type = DishType.objects.get(name=form_data["name"])

        self.assertEqual(new_dish_type.name, form_data["name"])

    def test_update_dish_type(self):
        new_dish_type = DishType.objects.create(
            name="Test name",
        )
        update_data = {
            "name": "Update name",
        }
        self.client.post(
            reverse(
                "kitchen:dish-type-update", kwargs={"pk": new_dish_type.id}
            ),
            data=update_data,
        )

        new_dish_type = DishType.objects.get(pk=new_dish_type.id)
        self.assertEqual(new_dish_type.name, update_data["name"])

    def test_delete_dish_type(self):
        new_dish_type = DishType.objects.create(
            name="Test name",
        )
        DishType.objects.create(
            name="Delete name",
        )

        self.client.post(
            reverse(
                "kitchen:dish-type-delete", kwargs={"pk": new_dish_type.id}
            )
        )
        self.assertEqual(DishType.objects.count(), 1)


class PublicDishTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DISH_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_dish(self):
        new_dish_type = DishType.objects.create(
            name="Test1",
        )
        Dish.objects.create(name="Test1", dish_type=new_dish_type, price=12)

        response = self.client.get(DISH_URL)
        dish = Dish.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dish_list"]), list(dish))
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_search_dish(self):
        new_dish_type = DishType.objects.create(
            name="Test name",
        )
        Dish.objects.create(
            name="Test name", dish_type=new_dish_type, price=12
        )
        Dish.objects.create(
            name="Test name", dish_type=new_dish_type, price=12
        )
        Dish.objects.create(
            name="Test name", dish_type=new_dish_type, price=12
        )

        search_param = "I4"
        response = self.client.get(DISH_URL + f"?name={search_param}")
        dish = Dish.objects.filter(name__icontains=search_param)
        self.assertEqual(list(response.context["dish_list"]), list(dish))

    def test_delete_dish(self):
        new_dish_type = DishType.objects.create(
            name="Test",
        )
        new_dish = Dish.objects.create(
            name="Test", dish_type=new_dish_type, price=12
        )
        Dish.objects.create(name="Test", dish_type=new_dish_type, price=12)

        self.client.post(
            reverse("kitchen:dish-delete", kwargs={"pk": new_dish.id})
        )
        self.assertEqual(Dish.objects.count(), 1)
