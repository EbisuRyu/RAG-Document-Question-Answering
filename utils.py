import chainlit as cl
import torch
from chainlit.types import AskFileResponse
from transformers import BitsAndBytesConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.vectorstores import Chroma


def process_file(file: AskFileResponse, text_splitter):
    """
    Process the uploaded file based on its type and split the text into chunks.

    Args:
        file (AskFileResponse): The uploaded file.
        text_splitter (RecursiveCharacterTextSplitter): The text splitter to use for splitting the text.

    Returns:
        List[Document]: The processed and split documents.
    """
    try:
        if file.type == "text/plain":
            loader = TextLoader(file.path)
        elif file.type == "application/pdf":
            loader = PyPDFLoader(file.path)
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs
    except Exception as e:
        print(f"Error processing file: {e}")
        return []


def get_vector_db(file: AskFileResponse, text_splitter, embedding):
    """
    Create a vector database from the uploaded file.

    Args:
        file (AskFileResponse): The uploaded file.
        text_splitter (RecursiveCharacterTextSplitter): The text splitter to use.
        embedding (HuggingFaceEmbeddings): The embedding model to use.

    Returns:
        Chroma: The vector database.
    """
    try:
        docs = process_file(file, text_splitter)
        cl.user_session.set("docs", docs)
        vector_db = Chroma.from_documents(documents=docs, embedding=embedding)
        return vector_db
    except Exception as e:
        print(f"Error creating vector DB: {e}")
        return None


def get_huggingface_llm(model_name: str = "lmsys/vicuna-7b-v1.5", max_new_token: int = 512):
    """
    Load a HuggingFace model with quantization and create a language model pipeline.

    Args:
        model_name (str): The name of the HuggingFace model to load.
        max_new_token (int): The maximum number of new tokens to generate.

    Returns:
        HuggingFacePipeline: The HuggingFace language model pipeline.
    """
    try:
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=nf4_config,
            low_cpu_mem_usage=True
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        model_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=max_new_token,
            pad_token_id=tokenizer.eos_token_id,
            device_map="auto"
        )

        llm = HuggingFacePipeline(pipeline=model_pipeline)
        return llm
    except Exception as e:
        print(f"Error loading HuggingFace model: {e}")
        return None
