from langchain_core.prompts import ChatPromptTemplate

prompt= ChatPromptTemplate.from_template(
    """You are a highly capable assistant trained to analyse and summarize documents.
    Return only valid JSON matching the exact schema below.
    {format_instruction}
    
    Analyze this document:
    {document_text}"""
    )