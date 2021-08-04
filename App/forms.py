import datetime
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

ADVANCE_RESERVATION_DAYS = 14

class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=20)
    password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput())

class ReservationForm(forms.Form):
    name = forms.CharField(label='Guest Name', max_length=20)
    num = forms.IntegerField(label='How many people?', max_value=10, min_value=1)
    timeslot= forms.DateTimeField(label='Date and Time', input_formats = ["%d.%m.%Y %H:%M"], widget=DateTimePickerInput(options={
        'format': 'DD.MM.YYYY HH:mm',
        'minDate': datetime.datetime.today().strftime('%m/%d/%Y'),
        'maxDate': (datetime.datetime.today() + datetime.timedelta(days=ADVANCE_RESERVATION_DAYS)).strftime('%m/%d/%Y'),
        'stepping': 60,
        'enabledHours': [12, 13, 14, 15, 16, 17, 18, 19, 20],
        'sideBySide': True,
    }))

    def __init__(self, *args, **kwargs):
        guest = kwargs.pop('guest')
        super().__init__(*args, **kwargs)

        if guest is not None:
            self.fields['name'].initial = guest
            self.fields['name'].widget.attrs['readonly'] = True


class CreateUserForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    login = forms.CharField(label='login', max_length=20)
    password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput())
    passagain = forms.CharField(label='passagain', max_length=20, widget=forms.PasswordInput())