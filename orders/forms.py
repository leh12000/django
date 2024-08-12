from django import forms
from orders.models import Commande


class CommandeForm(forms.ModelForm):
    class Meta:
        model=Commande
        fields=[
            "first_name",
            "last_name",
            "email",
            "phone",
            "address_line_1",
            "address_line_2",
            "country",
            "state",
            "order_note",
        ]