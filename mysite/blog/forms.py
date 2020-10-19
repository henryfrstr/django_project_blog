from django import forms
from .models import Comment, Post, Category


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'content',
        ]
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.TextInput(attrs={'class': 'form-control'}),
            "content": forms.Textarea(attrs={'class': 'form-control'}),
        }


class PostSearchForm(forms.Form):
    q = forms.CharField(label="Search For", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    c = forms.ModelChoiceField(required=False, label="Category",
                               queryset=Category.objects.all().order_by('name'))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['c'].required = False
