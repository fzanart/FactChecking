import os
import re
import json
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

MODEL_CONFIG = {
    "openai": ChatOpenAI(
        temperature=0,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        openai_organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
        model_name="gpt-4-0125-preview",
    ),
    "mixtral": HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=1,
        top_k=1,
        huggingfacehub_api_token=os.environ.get("HF_API_KEY"),
        model_kwargs={
            "use_cache": False,
        },
    ),
    "gemini-pro": GoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
    ),
}


def get_llm(model_type):
    if model_type == "mixtral":
        return ChatHuggingFace(llm=MODEL_CONFIG.get(model_type))
    else:
        return MODEL_CONFIG.get(model_type)


class Stance(BaseModel):
    stance: str = Field(
        description="one of the following - support, refutes, no stance"
    )


parser = JsonOutputParser(pydantic_object=Stance)


# Function to clean the string and find the stance matches
def clean_and_match(data):
    # Define the cleaning pattern
    clean_pattern = re.compile(r"```|\bjson\b|\n|\s+", re.IGNORECASE)
    # Define the stance matching pattern
    stance_pattern = re.compile(
        r'{"stance":\s*["\'](no stance|refutes|supports)["\']}',
        re.IGNORECASE | re.DOTALL,
    )

    matches = {}
    for key, value in data.items():
        # Clean the string
        cleaned_value = clean_pattern.sub("", value.content)
        # Match the stance
        match = stance_pattern.search(cleaned_value)
        if match:
            matches[key] = json.loads(match.group())

    return matches
