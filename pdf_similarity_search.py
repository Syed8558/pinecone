import os
import time
import uuid
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
PDF_FOLDER_PATH = r"C:\Users\User\OneDrive\Desktop\pinecone_test\chromdb\1000"
INDEX_NAME = "pdf-similarity-index"
PINECONE_REGION = "us-east-1"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("Please set PINECONE_API_KEY environment variable")

# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_dim = model.get_sentence_embedding_dimension()
print("Embedding dimension:", embedding_dim)

# ---------------------------------------------------------
# INIT PINECONE
# ---------------------------------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=embedding_dim,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_REGION)
    )
    print("Index created successfully")
else:
    print("Index already exists")

index = pc.Index(INDEX_NAME)

# ---------------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------------
def extract_text_from_pdfs(folder_path):
    documents = []

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            reader = PdfReader(file_path)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "

            if text.strip():
                documents.append({
                    "id": str(uuid.uuid4()),
                    "text": text,
                    "source": file_name
                })

    return documents


print("Extracting text from PDFs...")
start_time = time.time()
documents = extract_text_from_pdfs(PDF_FOLDER_PATH)
print(f"Text extraction completed in {time.time() - start_time:.2f} seconds")
print(f"Total documents loaded: {len(documents)}")

# ---------------------------------------------------------
# GENERATE EMBEDDINGS
# ---------------------------------------------------------
texts = [doc["text"] for doc in documents]
ids = [doc["id"] for doc in documents]
metadatas = [{"source": doc["source"]} for doc in documents]

print("Generating embeddings...")
embeddings = model.encode(texts, batch_size=16, show_progress_bar=True).tolist()

# ---------------------------------------------------------
# UPSERT TO PINECONE
# ---------------------------------------------------------
print("Uploading vectors to Pinecone...")
BATCH_SIZE = 100

for i in range(0, len(ids), BATCH_SIZE):
    batch_vectors = []
    for j in range(i, min(i + BATCH_SIZE, len(ids))):
        batch_vectors.append((ids[j], embeddings[j], metadatas[j]))

    index.upsert(vectors=batch_vectors)
    print(f"Uploaded batch {(i//BATCH_SIZE) + 1}")

print("All PDFs uploaded successfully!")

# ---------------------------------------------------------
# QUERY LOOP
# ---------------------------------------------------------
while True:
    query = input("\nEnter your query (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    start_time = time.time()

    query_embedding = model.encode(query).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )

    end_time = time.time()

    print(f"\n⏱ Query time: {end_time - start_time:.2f} seconds")

    print("\n📄 Top 5 similar PDFs:")
    for i, match in enumerate(results["matches"], 1):
        print(f"{i}. {match['metadata']['source']} (score={match['score']:.3f})")

print("\nProgram finished.")


