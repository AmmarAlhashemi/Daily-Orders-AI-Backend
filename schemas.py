from pydantic import BaseModel


class Transaction(BaseModel):
    serial: str
    recipient_name: str
    account_number: str = ""
    amount: float = 0.0
    remark: str = ""
    designated_person: str = ""
    ai_warning: str = ""


class ParseOrdersRequest(BaseModel):
    raw_data: str
    use_fallback: bool = False

class ParseOrdersResponse(BaseModel):
    transactions: list[Transaction]


class SmartSplitRequest(BaseModel):
    excel_data: list[dict]
    use_fallback: bool = False


class SmartSplitResponse(BaseModel):
    delete_from_ENTITY_A: list[str]
    delete_from_ENTITY_B: list[str]
