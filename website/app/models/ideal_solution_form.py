from django import forms


class IdealSolutionPostForm(forms.ModelForm):
    play = forms.FileField(null=True, blank=True, verbous_name='Файл', upload_to='play')
    solution = forms.FileField(null=True, blank=True, verbous_name='Файл', upload_to='ideal_solution')
