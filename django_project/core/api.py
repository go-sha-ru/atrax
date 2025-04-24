from ninja import Router

from core.models import NumberingRegister
from core.schema import PhoneInfoResponseSchema, PhoneInfoInputSchema

router = Router()


@router.get("/", response=PhoneInfoResponseSchema)
def get_phone(request, phone_number):
    code = phone_number[1: 4]
    phone = phone_number[4:]
    if info := NumberingRegister.objects.filter(code=code, start__lte=phone, end__lte=phone).first():
        return {"phone": phone_number, "operator": info.operator, "region": info.region}
    return {}


@router.post("/", response=PhoneInfoResponseSchema)
def get_phone(request, payload: PhoneInfoInputSchema):
    code = payload.phone[1: 4]
    phone = payload.phone[4:]
    if info := NumberingRegister.objects.filter(code=code, start__lte=phone, end__lte=phone).first():
        return {"phone": payload.phone, "operator": info.operator, "region": info.region}
    return {}
