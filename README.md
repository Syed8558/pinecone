📄 PDF Similarity Search using Pinecone

This project builds a semantic search system over 1000 PDF documents using Pinecone Vector Database and Sentence Transformers.
It allows users to enter a query and retrieves the Top 5 most similar PDFs in less than 8 seconds.

🚀 Features

Upload and index 1000 PDF documents into Pinecone

Generate embeddings using all-MiniLM-L6-v2

Store embeddings with PDF filename as metadata

Perform fast similarity search

Return Top 5 similar PDFs for a query

Measure query response time

Works in VS Code and terminal

🛠 Tech Stack

Python

Pinecone (Vector Database)

SentenceTransformers (Embeddings)

PyPDF (PDF text extraction)

📁 Project Structure
pinecone_pdf_search/
│
├── pdfs/                     # Folder containing 1000 PDFs
├── pdf_similarity_search.py  # Main script
└── README.md

⚙️ Installation
1. Install dependencies
pip install pinecone-client sentence-transformers pypdf

2. Set Pinecone API Key

Create a Pinecone account at:
👉 https://app.pinecone.io

Copy your API key and set it as an environment variable.

Windows (PowerShell):
setx PINECONE_API_KEY "your_api_key_here"


Restart VS Code after setting it.

Verify:

echo $env:PINECONE_API_KEY

▶️ How to Run
1. Place your PDFs

Put all PDF files inside:

pdfs/


Example:

pdfs/
 ├── resume1.pdf
 ├── resume2.pdf
 ├── resume3.pdf

2. Run the program
python pdf_similarity_search.py

3. Enter query

Example:

Enter your query: machine learning engineer resume


Output:

Query time: 0.92 seconds

Top 5 similar PDFs:
1. resume_101.pdf (score=0.91)
2. ai_profile.pdf (score=0.88)
3. data_engineer.pdf (score=0.86)
4. ml_resume.pdf (score=0.84)
5. python_resume.pdf (score=0.82)


Type exit to quit.

⏱ Performance

PDF ingestion: ~3–5 minutes (one time only)

Query time: < 1 second

Meets assignment requirement: < 8 seconds

🧠 How It Works

Extract text from each PDF

Convert text into embeddings using SentenceTransformer

Store embeddings in Pinecone with unique IDs

Convert user query into embedding

Perform vector similarity search in Pinecone

Return Top 5 similar PDFs

📌 Key Concepts

UUID: Used to uniquely identify each PDF vector

Metadata: Stores PDF filename for retrieval

Cosine similarity: Used for vector comparison

Serverless Pinecone index for fast querying

✅ Assignment Objectives Met

✔ Pinecone collection created
✔ 1000 PDFs indexed
✔ Query response < 8 seconds
✔ Top 5 similar PDFs returned
✔ Professional project structure

🔮 Future Improvements

Add text chunking for higher accuracy

Build Streamlit or FastAPI UI

Add caching

Dockerize the application

Add logging and error handling

👨‍💻 Author

SYED SADATH G
PDF Similarity Search Project using Pinecone & NLP
