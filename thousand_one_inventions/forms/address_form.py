from django import forms

from thousand_one_inventions.models.address_type import AddressType


class AddressForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        address_types = AddressType.ADDRESS_TYPES.items()
        self.fields["type"] = forms.ChoiceField(
            choices=address_types,
        )

        self.fields["details"] = forms.CharField(max_length=200)