from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change help texts
        self.fields["username"].help_text = "Choose a username (letters & numbers only)"
        self.fields["password1"].help_text = "Minimum 8 characters"
        self.fields["password2"].help_text = "Enter same password again"
