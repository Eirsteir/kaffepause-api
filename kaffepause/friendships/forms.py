from django import forms

from .models import FriendshipStatus


class FriendshipStatusAdminForm(forms.ModelForm):
    class Meta:
        model = FriendshipStatus
        fields = "__all__"

    def duplicate_slug_check(self, status_slug):
        status_qs = FriendshipStatus.objects.filter(slug=status_slug)

        if self.instance.pk:
            status_qs = status_qs.exclude(pk=self.instance.pk)

        if status_qs.exists():
            raise forms.ValidationError(
                f"{status_slug} already in use on {status_qs[0]}"
            )

    def clean_slug(self):
        self.duplicate_slug_check(self.cleaned_data["slug"])
        return self.cleaned_data["slug"]

    def clean(self):
        if self.errors:
            return self.cleaned_data

        return self.cleaned_data
