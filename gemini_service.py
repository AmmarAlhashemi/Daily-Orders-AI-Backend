import json

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from schemas import ParseOrdersResponse
from schemas import SmartSplitResponse
from exceptions import PrimaryModelError, FallbackModelError



client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are a professional financial data auditor. Your task is to parse unstructured daily remittance order text and convert it into a highly accurate structured data table.

Strict Field Processing Rules:
1. Field (remark): Extract bank name only (e.g., BANK_1, BANK_2), order status only (e.g., URGENT, VERY URGENT), or both (e.g., BANK_2 VERY URGENT).
   - Automatically fix spelling errors in status keywords and write them in UPPERCASE.
   - Remove emojis and extraneous phrases (e.g., eliminate '‼️' or 'Give to').
   - Do NOT write any warning in ai_warning regarding status spelling corrections (silent cleaning).

2. Field (designated_person): If a specific person or entity name (ENTITY_A or ENTITY_B) is mentioned in remarks, extract it cleanly ('ENTITY_A' or 'ENTITY_B' only).
   - Correct phrasing like 'Enty B' to 'ENTITY_B', and 'Give to ENTITY_A' to 'ENTITY_A'. Leave empty if neither is mentioned.

3. Field (ai_warning): Reserved ONLY for critical financial and structural errors:
   - Correct points instead of commas in amounts (e.g., 7.750 becomes 7750.0).
   - Correct extra zeros (e.g., 15,4000 becomes 15400.0).
   - Detail any numeric financial corrections here.

4. General Rules: Ignore typos in structural words like AMOINT (treat as AMOUNT). If serial number is missing, add serial based on processing sequence.
"""


def parse_raw_orders(raw_data: str, use_fallback: bool = False) -> dict:
    model = "gemini-3.5-flash" if use_fallback else "gemini-3.6-flash"
    try:
        response = client.models.generate_content(
            model=model,
            contents=raw_data,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ParseOrdersResponse,
                temperature=0.0,
            ),
        )

    except Exception as error:
        if use_fallback:
            raise FallbackModelError(str(error))

        raise PrimaryModelError(str(error))

    return json.loads(response.text)


SPLIT_PROMPT_TEMPLATE = """
You are an expert financial accountant responsible for splitting daily remittance orders between two entities: ENTITY_A and ENTITY_B.
Here is the current JSON data:
{excel_data}

Strict Splitting Rules:
1. ENTITY_A File: Does NOT take orders containing a bank name in the remark field. Takes orders with account numbers starting with 100.
2. ENTITY_B File: Must strictly take any order containing other bank names (e.g., BANK_1, BANK_2, BANK_3, BANK_4, BANK_5, etc.).
3. Financial Balancing: Flexible orders (CBE or unspecified bank) should be distributed intelligently so that total amount and order count for both ENTITY_A and ENTITY_B are balanced as closely as possible.
4. Each serial number must appear in exactly one delete list (either delete_from_ENTITY_A or delete_from_ENTITY_B). Do not leave any order unclassified, and do not duplicate serials.

Rule #1 is top priority over total amount and count balancing.
Output: Return a structured JSON containing delete_from_ENTITY_A and delete_from_ENTITY_B arrays.
"""


def smart_split_data(excel_data: list,use_fallback: bool = False) -> dict:
    model = "gemini-3.5-flash" if use_fallback else "gemini-3.6-flash"
    split_prompt = SPLIT_PROMPT_TEMPLATE.format(
        excel_data=json.dumps(excel_data, ensure_ascii=False)
    )
    try:
        response = client.models.generate_content(
            model=model,
            contents=split_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SmartSplitResponse,
                temperature=0.0,
            ),
        )
    except Exception as error:
        if use_fallback:
            raise FallbackModelError(str(error))

        raise PrimaryModelError(str(error))

    return json.loads(response.text)