import fitz
from unicodedata import normalize


def pdf_reader(
    file_data: Any, skip_page: list = [], table_save: bool = False
) -> str:
    doc = fitz.open(stream=file_data.read(), filetype="pdf")
    text_data = ""
    for page in range(len(doc)):
        page_data = doc[page]
        if page not in skip_page:
            text_data += page_data.get_text()
        if table_save:
            table_data = page_data.find_tables()
            if len(table_data.tables) == 0:
                continue
            table_text = ""
            for tbl in table_data:
                for t in tbl.extract():
                    if None in t:
                        t = [_t for _t in t if _t != None]
                    table_text += ":".join(t).replace("\n", "") + "\n"
                table_text += "\n"
    return text_data


def normalize_text(text_data: str, replace_str: str = "\u3000") -> str:
    clean_text = normalize("NFKC", text_data)
    clean_text = clean_text.replace(replace_str, " ")
    clean_text = clean_text.replace("\n", "")
    return clean_text
