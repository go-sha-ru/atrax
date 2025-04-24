from ninja import Schema


class PhoneInfoInputSchema(Schema):
    phone: str


class PhoneInfoResponseSchema(Schema):
    phone: int
    operator: str
    region: str
