from langchain_openai import ChatOpenAI
from api.module.answer_prompt import related_prompt, create_system_prompt
from langchain import LLMChain
from langchain.schema import Document
from api.module.preprocessing import chunk_split
from langchain_community.callbacks import get_openai_callback
from langchain_community.vectorstores import Qdrant
from api.module.document_search import documents_search
from api.module.related_select import select
from typing import Optional, Any
import re


# ドキュメントをグルーピング
def group_sentence(related_data: list) -> list:
    related_info = []
    for relate in related_data:
        group = []
        split_text = chunk_split(relate.page_content)
        for i, text in enumerate(split_text):
            info = Document(
                page_content=text,
                metadata={
                    "filename": relate.metadata["filename"],
                    "fileid": relate.metadata["fileid"],
                    "rank": relate.metadata["rank"],
                    "item_number": i,
                },
            )
            group.append(info)
        related_info.append([group])
    return related_info


# 回答作成
def compose(selected_info_list: list, query: str, llm: Any) -> dict:
    prompt = create_system_prompt()
    string_info, fileid_list, for_log_quote_lines = related_prompt(
        selected_info_list
    )
    prompt_str = prompt.format(query=query, info=string_info)
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
    )
    try:
        with get_openai_callback() as cb:
            response = llm_chain.run({"query": query, "info": string_info})
    except Exception as e:
        print(e)
        response = "エラー: " + str(e)
    cost = cb.total_cost
    print(response)
    ret = re.findall(r"\[([0-9]+)\-[0-9]+\]", response)
    ret += re.findall(r"\[([0-9]+)\]", response)
    ret_lines = re.findall(r"\[([0-9]+\-[0-9]+)\]", response)
    nums_ref = sorted(list(set(map(int, ret))))

    res_quote_lines = [
        {"number": i, "sentence": line}
        for i, line in for_log_quote_lines
        if i in ret_lines
    ]
    res_quote_files = [
        {"number": i, "document_id": fileid}
        for i, fileid in enumerate(fileid_list)
        if i in nums_ref
    ]

    for_log_compose_data = {
        "prompt": prompt_str,
        "answer": response,
        "cost": cost,
        "res_line": res_quote_lines,
        "res_file": res_quote_files,
    }
    return for_log_compose_data


# 回答
async def answer(
    query: str,
    db: Qdrant,
    model: str = "gpt-3.5-turbo",
    mode: str = "default",
    relate_num: int = 3,
    filter: Optional[dict] = None,
) -> dict:
    llm = ChatOpenAI(temperature=0, model=model, timeout=300)
    if mode == "default":
        related_data, score_data = documents_search(
            db, query, top_k=relate_num, filter=filter
        )
        related_info = group_sentence(related_data)
    elif mode == "select":
        related_data, score_data = documents_search(
            db, query, top_k=relate_num, filter=filter
        )
        related_info, cost, for_log_select_data = await select(
            related_data, query
        )
    for_log_compose_data = compose(related_info, query, llm)
    return for_log_compose_data
