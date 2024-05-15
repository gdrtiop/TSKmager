from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Task, Project, Complaint


class UserRegisterForm(UserCreationForm):
    """
    Переопределенная форма регистрации пользователей
    """

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте свой логин'})
            self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте свой пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите придуманный пароль'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class ProfileForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        min_length=2,
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        min_length=2,
        required=False,
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        min_length=2,
        required=False,
    )

    class Meta:
        field = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": 'Ваш новый логин'})
        self.fields['email'].widget.attrs.update({"placeholder": 'Ваш новый email'})
        self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
        self.fields['last_name'].widget.attrs.update({"placeholder": 'Ваша фамилия'})


class CreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['name'].required = True


class AddUserForm(forms.Form):
    new_memb = forms.CharField(
        label='Добавить участника',
        widget=forms.TextInput(attrs={'placeholder': 'Введите никнейм'}),
        max_length=300,
        min_length=1,
        required=True,
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
        }

    done = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    who_done = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['description'].required = False

        instance = kwargs.get('instance')
        if instance:
            self.fields['who_done'].initial = instance.who_done
            self.fields['done'].initial = instance.done
            self.fields['name'].initial = instance.name
            self.fields['description'].initial = instance.description


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше предложение или ваша жалоба'}),
        }


class AnswerComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ответ'}),
        }