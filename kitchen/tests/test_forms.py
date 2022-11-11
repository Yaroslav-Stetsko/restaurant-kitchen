from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.forms import CookCreationForm


class CookFormTest(TestCase):
    def test_cook_creation_form_with_years_of_experience_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test3user123",
            "password2": "test3user123",
            "years_of_experience": 12,
            "first_name": "First",
            "last_name": "Last"
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_cook_creation_form_with_years_of_experience_invalid(self):
        form_data = {
            "username": "new_user",
            "password1": "test3user123",
            "password2": "test3user123",
            "years_of_experience": "12",
            "first_name": "First",
            "last_name": "Last"
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)


class CookUpdateTest(TestCase):
    def test_cook_update_form_valid(self):
        new_cook = get_user_model().objects.create_user(
            username="new_user",
            password="test3user123",
            years_of_experience=12,
            first_name="Testingtest",
            last_name="Testingtesttesttest"
        )
        self.client.force_login(new_cook)
        update_data = {
            "years_of_experience": 12,
            "first_name": "Testingtest",
            "last_name": "Testingtesttesttest",

        }

        self.client.post(reverse(
            "kitchen:cook-update",
            kwargs={"pk": new_cook.id}),
            data=update_data)

        cook = get_user_model().objects.get(pk=new_cook.id)
        self.assertEqual(
            cook.years_of_experience,
            update_data["years_of_experience"]
        )
        self.assertEqual(cook.first_name, update_data["first_name"])
        self.assertEqual(cook.last_name, update_data["last_name"])
