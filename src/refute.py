from search import keyword_search_result, get_urls
from retrieve import fetch_url, parse_html, split_into_chunked_docs, retrieve_docs
from process import stance_detection


def fact_checking_pipeline(model, claim, keyword_template):

    evidence = {}
    relevant_text = []

    keywords = keyword_search_result(claim, model, keyword_template)
    source_url = get_urls(keywords)
    for url in source_url:
        html = fetch_url(url)
        text_content = parse_html(html)
        chunked_docs = split_into_chunked_docs(text_content)
        evidence_docs = retrieve_docs(chunked_docs, keywords)
        answer = stance_detection(model, evidence_docs, claim)

        for i, doc in enumerate(evidence_docs):
            relevant_text.append(
                {str(i): doc, "stance": answer.get(str(i)).get("stance")}
            )

        evidence[url] = relevant_text
        relevant_text = []

    return evidence


# combines everything

# links + evidence + stance


# {url : [
#        {'0': chunk of text, 'stance': 'label'},
#       {'1': chunk of text, 'stance': 'label'},
#       {'2': chunk of text, 'stance': 'label'}
#       ]}
#
#
