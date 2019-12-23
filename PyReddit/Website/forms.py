from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'Title'}), help_text = 'Maximum 50 characters')
    description = forms.CharField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'Description'}), help_text = 'Maximum 300 characters')
    content = forms.CharField(required = False, widget = forms.Textarea(attrs = {'placeholder': 'Content of the blog.....', 'class': 'content-create'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'content']
    
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if len(title) == 0:
            raise forms.ValidationError('Title is required!')
        if len(title) > 50:
            raise forms.ValidationError('Title should contains at most 50 characters')
        return title
    
    def clean_description(self, *args, **kwargs):
        description = self.cleaned_data.get('description')
        if len(description) == 0:
            raise forms.ValidationError('Description is required!')
        if len(description) > 300:
            raise forms.ValidationError(f'Description should contains at most 300 characters, but contains {len(description)} characters!')
        return description
    
    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get('content')
        if len(content) == 0:
            raise forms.ValidationError('Content is required!')
        return content