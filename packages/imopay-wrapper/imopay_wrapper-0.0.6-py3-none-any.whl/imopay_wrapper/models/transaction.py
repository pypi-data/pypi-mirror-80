from typing import List
from dataclasses import dataclass

from .base import BaseImopayObj
from ..exceptions import FieldError
from ..validators import (
    validate_obj_attr_type,
    validate_obj_attr_in_collection,
    validate_date_isoformat,
    validate_date_1_gt_date_2,
)
from ..field import field


@dataclass
class BaseTransaction(BaseImopayObj):
    payer: str
    receiver: str
    reference_id: str
    amount: int
    description: str


@dataclass
class BaseConfiguration(BaseImopayObj):
    value: int
    charge_type: str

    PERCENTAGE = "p"
    FIXED = "f"
    DAILY_FIXED = "df"
    DAILY_PERCENTAGE = "dp"
    MONTHLY_PERCENTAGE = "mp"

    VALID_CHARGE_TYPES = {}

    def _validate_value(self):
        self.value = int(self.value)
        if self.value <= 0:
            raise FieldError("value", "O valor é menor do que 1!")

    def _validate_charge_type(self):
        validate_obj_attr_in_collection(self, "charge_type", self.VALID_CHARGE_TYPES)


@dataclass
class InterestConfiguration(BaseConfiguration):
    VALID_CHARGE_TYPES = {
        BaseConfiguration.DAILY_FIXED,
        BaseConfiguration.DAILY_PERCENTAGE,
        BaseConfiguration.MONTHLY_PERCENTAGE,
    }


@dataclass
class FineConfiguration(BaseConfiguration):
    VALID_CHARGE_TYPES = {BaseConfiguration.FIXED, BaseConfiguration.PERCENTAGE}


@dataclass
class DiscountConfiguration(FineConfiguration):
    date: str

    def _validate_date(self):
        validate_date_isoformat(self, "date", past=True, allow_today=True)


@dataclass
class InvoiceConfigurations(BaseImopayObj):
    fine: FineConfiguration = field(optional=True)
    interest: InterestConfiguration = field(optional=True)
    discounts: List[DiscountConfiguration] = field(optional=True, default=list)

    def _validate_fine(self):
        validate_obj_attr_type(self, "fine", dict)

    def _validate_interest(self):
        validate_obj_attr_type(self, "interest", dict)

    def _validate_discounts(self):
        validate_obj_attr_type(self, "discounts", list)

        for discount in self.discounts:
            validate_obj_attr_type(self, "discounts", dict, value=discount)

    def _init_nested_fields(self):
        if self.fine is not None:
            self.fine = FineConfiguration.from_dict(self.fine)

        if self.interest is not None:
            self.interest = InterestConfiguration.from_dict(self.interest)

        if self.discounts:
            for i, discount in enumerate(self.discounts):
                self.discounts[i] = DiscountConfiguration.from_dict(discount)

    def to_dict(self):
        """
        Por causa do typehint 'List' o to_dict original não funciona!

        Ao invés de solucionar isso, mais fácil sobreescrever o método
        no momento.
        """
        data = {}
        if self.fine:
            data["fine"] = self.fine.to_dict()

        if self.interest:
            data["interest"] = self.interest.to_dict()

        if self.discounts:
            data["discounts"] = [discount.to_dict() for discount in self.discounts]
        return data


@dataclass
class Invoice(BaseImopayObj):
    expiration_date: str
    limit_date: str
    configurations: InvoiceConfigurations = field(optional=True, default_factory=dict)

    def _init_nested_fields(self):
        if self.configurations is not None:
            self.configurations = InvoiceConfigurations.from_dict(self.configurations)

    def _validate_configurations(self):
        validate_obj_attr_type(self, "configurations", dict)

    def _validate_expiration_date(self):
        validate_date_isoformat(self, "expiration_date", future=True, allow_today=True)

    def _validate_limit_date(self):
        validate_date_isoformat(self, "limit_date", future=True, allow_today=True)
        validate_date_1_gt_date_2(
            "limit_date", self.limit_date, self.expiration_date, allow_equal=True
        )


@dataclass
class InvoiceTransaction(BaseTransaction):
    payment_method: Invoice

    def _init_nested_fields(self):
        self.payment_method = Invoice.from_dict(self.payment_method)

    def _validate_payment_method(self):
        validate_obj_attr_type(self, "payment_method", dict)
