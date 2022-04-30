from django import forms


class BidForm(forms.Form):
    """user bid form"""
    user_bid = forms.IntegerField(label='Place your Bid')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_bid'].required = False
        self.label_suffix = ""
