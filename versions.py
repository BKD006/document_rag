import importlib.metadata
packages = [
    "langchain",
    "langchain_core",
    "python-dotenv",
    "langchain_groq",
    "langchain_openai",
    "ipykernel",
    "langchain_google_genai",
    "langchain_community",
    "pypdf",
    "faiss-cpu",
    "langchain-google-vertexai",
    "langchain-aws",
    "boto3",
    "structlog",
    "PyMuPDF",
    "pandas",
    "langchain-core[tracing]",
    "pytest",
    "streamlit",
    "docx2txt",
    "fastapi",
    "uvicorn",
    "python-multipart",
    "jinja2"
]

for pkg in packages:
    try:
        version = importlib.metadata.version(pkg)
        print(f"{pkg}=={version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{pkg} (not installed)")
