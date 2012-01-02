from django import forms

class Comment_Form(forms.Form):
	author = forms.CharField(max_length = 50, label="Name")
	email = forms.EmailField(required = False)
	body = forms.CharField(label="Comment", widget=forms.Textarea)