from django import forms

class NewsSearchForm(forms.Form):
    query = forms.CharField(label='Tìm tiêu đề', max_length=100, required=False)
