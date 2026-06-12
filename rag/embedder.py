from mcp_server.github_client import get_repo_files
from mcp_server.github_client import get_file_content
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def embeder(repo_name):
    file_paths=get_repo_files(repo_name)
    file_content=[]
    for file in file_paths:
        file_content.append(get_file_content(file))
    
    
    text_split=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    file_content_list=[]
    for file in file_content:
        file_content_doc=Document(
            page_content=file.page_content,
            metadata={}
        )
        file_content_list.append(file_content_doc)
    split_file_content_doc=text_split(file_content_list)





    
