from pydantic import BaseModel, field_validator

class Store(BaseModel):
    Store_Name:   str
    Address:      str   # ✅ fixed
    Pincode:      int
    Region:       str
    City:         str
    ETA:          str
    Timing:       str
    Phone_Number: str
    Cost:         str
    Good_for:     str
    Store_Url:    str
    Menu_Url:     str

    @field_validator('Pincode', mode='before')
    def pincode_must_be_int(cls, v):
        if v == "" or v is None:
            return 0
        return int(v)

    @field_validator('*', mode='before')  
    @classmethod
    def empty_str_default(cls, v):
        if isinstance(v, str):
            return v.strip() or " "
        return v