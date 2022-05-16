from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import Car


class BidForm(forms.Form):
    """user bid form"""
    user_bid = forms.IntegerField(label='Place your Bid')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_bid'].required = False
        self.label_suffix = ""


class CarForm(forms.ModelForm):
    """Car form"""
    class Meta:
        """CarForm Meta"""
        model = Car
        fields = '__all__'

        widgets = {
            'timeStart': DateTimePickerInput(),
            'timeEnd': DateTimePickerInput(),
            }
