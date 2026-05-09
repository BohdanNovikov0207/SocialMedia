from django import forms

class FirstLoginForm(forms.Form):
    # last_name в базе данных
    displayname = forms.CharField(
        max_length= 20,
        label= 'Псевдонім автора',
        widget= forms.TextInput(attrs = {
            'placeholder': 'Введіть Псевдонім автора',
            'autofocus': True,
            'class': 'gray-text'
        }
        )
    )
    # username в базе данных
    username = forms.CharField(
        max_length= 12,
        label= 'Ім`я користувача',
        widget= forms.TextInput(attrs = {
            'placeholder': '@',
            'class': 'gray-text'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        displayname = cleaned_data.get('displayname')
        username = cleaned_data.get('username')

        cleaned_data["displayname"] = displayname
        cleaned_data["username"] = f"@{username}"

        return self.cleaned_data