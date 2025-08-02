from .file_parser import parse_file
fromm .vector_store import ingest_text, query

def process_file(file_path):
    text = parse_file(file_path)
    ingest_text(text)
    return "File processed and added to the knowledge base."

def answer_question(q):
    return query(query_text)

