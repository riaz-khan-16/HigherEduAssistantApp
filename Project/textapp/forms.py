from django import forms

class TextForm(forms.Form):
    filename = forms.CharField(label='Filename', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea)


    