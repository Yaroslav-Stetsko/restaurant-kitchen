from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from kitchen.models import Cook, Dish


class CookCreationForm(UserCreationForm):
    MIN_EXP = 0
    MAX_EXP = 65

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data["years_of_experience"]

        if years_of_experience > CookUpdateForm.MAX_EXP:
            raise ValidationError(
                f"Years of experience must be less than {CookUpdateForm.MAX_EXP}"
            )

        if years_of_experience < CookUpdateForm.MIN_EXP:
            raise ValidationError(
                f"Years of experience must be more than {CookUpdateForm.MIN_EXP}"
            )

        return years_of_experience


class CookUpdateForm(forms.ModelForm):
    MIN_EXP = 0
    MAX_EXP = 65

    class Meta:
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data["years_of_experience"]

        if years_of_experience > CookUpdateForm.MAX_EXP:
            raise ValidationError(
                f"Years of experience must be less than {CookUpdateForm.MAX_EXP}"
            )

        if years_of_experience < CookUpdateForm.MIN_EXP:
            raise ValidationError(
                f"Years of experience must be more than {CookUpdateForm.MIN_EXP}"
            )

        return years_of_experience


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Username"}),
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Name"}),
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Name"}),
    )


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Dish
        fields = "__all__"
