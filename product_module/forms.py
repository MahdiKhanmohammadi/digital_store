from django import forms


class CommentForm(forms.Form):
    comment_body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 6}), label='')
