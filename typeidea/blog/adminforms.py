from django import forms


class PostadminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False) #将摘要设置为多行文本,另一种解决方法是修改model
