from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish


class ModelTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Test")

        self.assertEqual(str(dish_type), dish_type.name)

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first name",
            last_name="Test last name",
        )

        self.assertEqual(str(cook),
                         f"{cook.username} ({cook.first_name}"
                         f" {cook.last_name})")

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="Test")
        dish = Dish.objects.create(
            name="Test",
            dish_type=dish_type,
            price=12
        )

        self.assertEqual(str(dish), dish.name)

    def test_create_cook_with_years_of_experience(self):
        username = "test"
        password = "test12345"
        years_of_experience = 14
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(cook.username, username)
        self.assertTrue(cook.check_password(password))
        self.assertEqual(cook.years_of_experience, years_of_experience)
