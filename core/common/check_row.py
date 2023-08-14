from .modify_element import modify_element

def check_row(row):
    if "birth_number" in row:
            date_of_birth = modify_element(row["birth_number"])
            if len(date_of_birth) < 10 and len(date_of_birth) >= 1:
                date_of_birth = date_of_birth.zfill(10)
                row["birth_number"] = date_of_birth
    return row