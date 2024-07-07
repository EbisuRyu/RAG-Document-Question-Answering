# 📄 RAG Document QA Chatbot

The PDF QA Chatbot is a system that uses `Chainlit` and `LangChain` tools to provide answers to questions related to the content in uploaded PDF or text files. This system leverages HuggingFace's large language model to process and retrieve information from documents.

## ✨ Features

- 📤 Upload PDF or text files.
- 🔍 Split text from documents into smaller chunks.
- 📚 Create a vector database from the split documents.
- 🔄 Support for search and retrieval of information from documents.
- ❓ Answer questions based on the document content.

## 🛠️ Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/EbisuRyu/RAG-Document-Question-Answering.git
    cd RAG-Document-Question-Answering
    ```

2. **Create and activate a virtual environment** (recommended):
    ```sh
    conda env create -f environment.yml
    conda activate rag-env
    ```

3. **Or you can install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

## 🚀 Local Deployment

1. **Run the application:**:
    ```sh
    chainlit run app.py
    ```

2. **Interact with the chatbot**:
    - 📤 Upload a PDF or text file.
    - ❓ Ask questions about the content in the uploaded file.

## 🌐 Online Access via Ngrok

To make the chatbot accessible over the internet using ngrok, follow these steps:

1. **Register for an ngrok account**:
    - Go to [ngrok](https://ngrok.com/) and sign up for an account.

2. **Authentication Token**:
    - After registering, get your authentication token from the ngrok dashboard.

3. **Install and Authenticate Ngrok**:
    ```sh
    pip install -q ngrok
    ngrok config add-authtoken YOUR_AUTH_TOKEN
    ```

4. **Establish a Tunnel**:
    ```python
    public_url = ngrok.connect(8000).public_url
    print(public_url)
    ```

5. **Launch the Chatbot**:
    ```sh
    chainlit run app.py 
    ```

6. **Access the Chatbot**:

    Navigate to the provided ngrok URL to interact with your chatbot remotely.

## 🙏 Acknowledgements

- The `Chainlit` library for making chatbot development easy.
- HuggingFace for providing powerful language models.
- The `LangChain` community for excellent tools and support.
