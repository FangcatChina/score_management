from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from .models import User, Group
class ScoreForm(forms.Form):
    score = forms.IntegerField(label='积分')
    reason = forms.CharField(label='原因', widget=forms.Textarea)
class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id']
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 汉化用户名标签和帮助文本
        self.fields['username'].label = '用户名'
        self.fields['username'].help_text = '必填项。150 个字符以内。只能包含字母、数字和 @/./+/-/_ 字符。'
        # 汉化密码 1 标签和帮助文本
        self.fields['password1'].label = '密码'
        self.fields['password1'].help_text = '你的密码不能和其他个人信息太相似。你的密码必须包含至少 8 个字符。你的密码不能是常见密码。你的密码不能全部为数字。'
        # 汉化密码 2 标签和帮助文本
        self.fields['password2'].label = '确认密码'
        self.fields['password2'].help_text = '请再次输入相同的密码，以验证输入的正确性。'

    class Meta:
        model = User
        fields = ('username',  'password1', 'password2')
        

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'special_score']

class AssignStudentToGroupForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())

class BatchScoreForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
    score = forms.IntegerField()
    reason = forms.CharField()

class UpdateGroupSpecialScoreForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['special_score']