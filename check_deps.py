
try:
    import flask
    print("Flask ok")
except ImportError:
    print("Flask missing")

try:
    import groq
    print("Groq ok")
except ImportError:
    print("Groq missing")

try:
    import pypdf
    print("pypdf ok")
except ImportError:
    print("pypdf missing")

try:
    from sentence_transformers import SentenceTransformer
    print("sentence_transformers ok")
except ImportError:
    print("sentence_transformers missing")
