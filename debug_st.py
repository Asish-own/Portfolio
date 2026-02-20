from sentence_transformers import SentenceTransformer

try:
    print("Testing SentenceTransformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("SentenceTransformer initialized.")
    emb = model.encode(["test"])
    print("Embedding success.")
except Exception as e:
    print(f"ST Error: {e}")
