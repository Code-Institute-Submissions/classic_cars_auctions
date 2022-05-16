from django import forms
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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'border-black rounded-0 form-control'

