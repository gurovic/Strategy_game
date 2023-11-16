from django import forms


class IdealSolutionPostForm(forms.ModelForm):
    play = forms.FileField()
    solution = forms.FileField()
