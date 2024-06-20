from aux import parser, get_llm, clean_and_match
from prompts import stance_detection_template, template_merge
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel


def stance_detection(model, evidence_docs, claim):

    llm = get_llm(model)

    chains_dict = {}
    for i, chunk in enumerate(evidence_docs):
        prompt = PromptTemplate(
            template=stance_detection_template,
            input_variables=["claim"],
            partial_variables={
                "evidence": chunk,
                "format_instructions": parser.get_format_instructions(),
            },
        )

        # Dynamically name the chains based on their index
        chain_name = str(i)
        chains_dict[chain_name] = prompt | llm

    map_chain = RunnableParallel(**chains_dict)
    labels = map_chain.invoke({"claim": claim})
    # labels = clean_and_match(labels)

    return labels


# if len(labels) > 1 : merge_prompt
# TODO: move refute label filter outside merge answer?


def merge_answer(model, evidence_docs, labels, claim):

    llm = get_llm(model)
    # Identify 'refutes' labels
    relevant_keys = [
        int(key) for key in labels if labels[key]["stance"].lower() == "refutes"
    ]
    # Select the corresponding documents from evidence_docs
    evidence = {
        str(k): evidence_docs[k] for k, idx in zip(relevant_keys, evidence_docs)
    }

    if not evidence:

        return "No refuting evidence has been found"

    merge_prompt = PromptTemplate(
        template=template_merge, input_variables=["context", "claim"]
    )

    merge_chain = merge_prompt | llm
    answer = merge_chain.invoke({"context": evidence, "claim": claim})

    # Extract source URLs from the metadata of each document in the evidence
    source = "\n".join({doc.metadata["url"] for doc in evidence.values()})

    return answer, source
