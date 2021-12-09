from django.contrib.auth.models import User

from thousand_one_inventions.models.address_type import AddressType
from thousand_one_inventions.models.base import BaseModel
from django.utils.translation import gettext_lazy as _
from django.db import models


class Address(BaseModel):
    place_id = models.CharField(
        max_length=100, default=None, null=True, blank=True
    )
    lat = models.DecimalField(
        default=None, null=True, blank=True, max_digits=19, decimal_places=10
    )
    lng = models.DecimalField(
        default=None, null=True, blank=True, max_digits=19, decimal_places=10
    )
    summary = models.CharField(max_length=250, blank=True, null=True)
    details = models.TextField(default=None, blank=True, null=True)

    postal_code = models.CharField(
        max_length=25, blank=True, null=True, default=None
    )

    def details_cleaned(self):
        # details were made to handle tons of data we got from nominatim
        # or google: we registered the results AFTER a '-- COMPUTED --' string:
        if self.details is None:
            return None
        idx = self.details.find("-- COMPUTED --")
        if idx >= 0:  # ignore what's after
            result = self.details[:idx].strip()
        else:
            result = self.details.strip()
        return result if result else None

    def as_dict(self):
        return {
            "summary": self.summary or None,
            "lat": self.lat or None,
            "lng": self.lng or None,
            "details": self.details_cleaned() or None,
            "postal_code": self.postal_code or None,
        }

    def __str__(self):
        if self.place_id is not None:
            place_id = self.str_clean(self.place_id)
        else:
            place_id = ""
        return (
            f"{place_id} {self.str_clean(self.summary, max_len=70)}"
            f'{self.str_clean(self.details, max_len=30, sep=" / ")}'
            f'{self.str_clean(self.postal_code)}'.strip()
        )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class EntityAddress(BaseModel):
    entity = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=False, null=False
    )
    address_type = models.ForeignKey(
        AddressType, models.CASCADE, blank=False, null=False
    )
    comment = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        result = (
            f"{str(self.entity)} -> {str(self.address)} "
            f"({str(self.address_type)})"
        )
        if self.comment:  # add the comment
            return f"{result} - {str(self.comment)}"
        return result
    def string(self):
        result = str(self.address)

        return result
    class Meta:
        verbose_name = _("Entity address")
        verbose_name_plural = _("Entity addresses")