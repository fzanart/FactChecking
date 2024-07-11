import re
from .aux import get_llm
from .prompts import (
    zero_shot_retrieval_template,
    few_shot_retrieval_template,
    cot_retrieval_template,
)
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import PromptTemplate

prompts = {
    "zero_shot": zero_shot_retrieval_template,
    "few_shot": few_shot_retrieval_template,
    "cot": cot_retrieval_template,
}


def keyword_search_result(statement, model, prompt_template):

    llm = get_llm(model)
    prompt = PromptTemplate(
        template=prompts.get(prompt_template), input_variables=["statement"]
    )
    chain = prompt | llm
    keywords = chain.invoke({"statement": statement})

    if prompt_template == "cot":
        kw = re.findall(r"(?<=The keyword search could be:\s).*", keywords.content)
        if kw:
            return kw[0]

    return keywords.content


def get_urls(keywords):

    search = DuckDuckGoSearchResults()
    results = search.run(keywords)
    urls = re.findall(r"link: ([^\]]+)", results)

    return urls
