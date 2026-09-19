
 Agentic RAG

«An intelligent Agentic Retrieval-Augmented Generation (RAG) system built with LangGraph, LangChain, ChromaDB, Hugging Face embeddings, FastAPI, and LLMs.»

Agentic RAG goes beyond traditional RAG by introducing an evaluation and decision-making loop. Instead of blindly generating an answer from retrieved documents, the system evaluates whether the retrieved context is relevant and can retry retrieval when the evidence is insufficient.

---

Overview

Traditional RAG generally follows:

User Question
      ↓
Retrieve Documents
      ↓
Generate Answer

This project introduces an agentic control flow:

                    ┌──────────────────┐
                    │   User Question  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Retrieve Context │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Grade Documents  │
                    └────────┬─────────┘
                             ↓
                       Relevant?
                      ╱          ╲
                    YES           NO
                     ↓             ↓
              ┌────────────┐   Retry Retrieval
              │  Generate  │        │
              │   Answer   │        └──────┐
              └─────┬──────┘               │
                    ↓                      │
                   END  ←──────────────────┘

The workflow is orchestrated using LangGraph, allowing the application to conditionally move between retrieval, evaluation, and generation steps.

---

 Key Features

-  PDF document ingestion
-  Recursive text chunking
-  Hugging Face sentence embeddings
-  ChromaDB vector storage
-  Semantic similarity search
- LLM-powered document relevance grading
-  Agentic retrieval loop
-  LangGraph state-based workflow
-  FastAPI backend
-  API-based document ingestion and querying
-  Retrieval attempt limit to prevent infinite loops

---

 What Makes It "Agentic"?

A conventional RAG pipeline assumes that the first retrieved documents are good enough.

This system introduces a feedback loop.

After retrieving documents, an LLM evaluates their relevance to the user's question.

If the retrieved context is relevant:

Retrieve → Grade → Generate

If the context is not relevant:

Retrieve → Grade → Retry Retrieval
                  ↑
                  └──────────────

The workflow therefore contains a decision point rather than being a purely linear pipeline.

This is implemented using LangGraph's conditional edges.

---

 Architecture

                         ┌───────────────┐
                         │    FastAPI    │
                         └───────┬───────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
                     ▼                       ▼
              Document Upload            User Query
                     │                       │
                     ▼                       ▼
              ┌─────────────┐        ┌─────────────┐
              │ PDF Loader  │        │ LangGraph   │
              └──────┬──────┘        │   Agent     │
                     │               └──────┬──────┘
                     ▼                      │
              ┌─────────────┐               ▼
              │ Text Split  │        ┌─────────────┐
              └──────┬──────┘        │  Retriever  │
                     │               └──────┬──────┘
                     ▼                      │
              ┌─────────────┐               ▼
              │  Embedding  │        ┌─────────────┐
              │    Model    │        │ ChromaDB    │
              └──────┬──────┘        └──────┬──────┘
                     │                      │
                     ▼                      ▼
              ┌─────────────┐        ┌─────────────┐
              │  ChromaDB   │◄───────│ Documents   │
              └─────────────┘        └─────────────┘
                                            │
                                            ▼
                                     ┌─────────────┐
                                     │   Grader    │
                                     └──────┬──────┘
                                            │
                                      ┌─────┴─────┐
                                      │           │
                                  Relevant    Irrelevant
                                      │           │
                                      ▼           │
                                  Generate        │
                                      │           │
                                      ▼           │
                                    Answer ◄──────┘

---

 Project Structure

agentic-rag/
│
├── ingest.py              # PDF ingestion and vector database creation
├── rag_pipeline.py        # LangGraph Agentic RAG workflow
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment configuration
├── README.md
└── LICENSE

---

Tech Stack

Technology| Purpose
 Python| Core programming language
 LangChain| RAG components and LLM integration
 LangGraph| Agentic workflow orchestration
 ChromaDB| Vector database
 Hugging Face| Embedding model
 FastAPI| Backend API
 PyPDF| PDF document loading
 LLM| Document grading and answer generation

---

 Workflow

1. Document Ingestion

A PDF is loaded and processed using a document loader.

PDF
 ↓
PyPDFLoader
 ↓
Documents

---

2. Text Splitting

Large documents are divided into smaller chunks using a recursive character text splitter.

Document
   ↓
Chunk 1
Chunk 2
Chunk 3
...

This allows the retriever to search smaller, semantically meaningful pieces of the document.

---

3. Embeddings

Each chunk is converted into a vector representation using a Hugging Face embedding model.

Text Chunk
    ↓
Embedding Model
    ↓
Vector

---

4. Vector Storage

The generated embeddings are stored in ChromaDB.

Documents
    ↓
Embeddings
    ↓
ChromaDB

---

5. Retrieval

When a user asks a question, the system performs semantic similarity search against the stored document vectors.

Question
   ↓
Embedding
   ↓
Similarity Search
   ↓
Top-k Documents

---

6. Document Grading

The retrieved documents are evaluated by an LLM.

The grader determines whether the retrieved context is relevant to answering the question.

Retrieved Documents
        +
      Question
        ↓
   LLM Grader
        ↓
Relevant / Not Relevant

---

7. Agentic Decision

The graph decides what to do next.

Relevant

Grade = Relevant
       ↓
Generate Answer
       ↓
      END

Not Relevant

Grade = Not Relevant
       ↓
Retry Retrieval
       ↓
Grade Again

The retry loop is bounded to prevent infinite execution.

---

 LangGraph State

The workflow maintains state throughout execution.

Conceptually:

class AgentState(TypedDict):
    question: str
    documents: list
    answer: str
    trials: int

The state allows different nodes in the graph to communicate and update the workflow.

---

 API

The application exposes a FastAPI backend.

Upload a PDF

POST /upload

Uploads and processes a PDF for retrieval.

Ask a Question

POST /ask

Example request:

{
  "question": "What is the main topic discussed in the document?"
}

Example response:

{
  "answer": "..."
}

---

 Installation

1. Clone the repository

git clone https://github.com/antariksha-agi/agentic-rag.git

cd agentic-rag

2. Create a virtual environment

Windows

python -m venv .venv

.venv\Scripts\activate

Linux / macOS

python3 -m venv .venv

source .venv/bin/activate

---

3. Install dependencies

pip install -r requirements.txt

---

 Environment Variables

Create a ".env" file in the project root.

Add the API credentials required by the LLM provider used by the project.

Example:

OPENAI_API_KEY=your_api_key_here

« Never commit your API keys to GitHub.»

Add ".env" to ".gitignore":

.env
.venv/
__pycache__/

---

 Running the Application

Start the FastAPI server:

uvicorn main:app --reload

The API will be available locally at:

http://127.0.0.1:8000

FastAPI's interactive documentation can be accessed through:

/docs

---

 Example

Suppose you upload a document containing information about machine learning.

You ask:

"What is supervised learning?"

The system performs:

User Question
      ↓
Vector Search
      ↓
Retrieve Documents
      ↓
LLM Relevance Grader
      ↓
Relevant?
   ↙       ↘
 YES        NO
  ↓          ↓
Generate   Retry
  ↓          │
Answer ◄─────┘

The final answer is generated using the retrieved context rather than relying purely on the model's internal knowledge.

---

 Why LangGraph?

LangGraph is used because Agentic RAG workflows are naturally represented as graphs with state and conditional transitions.

Instead of writing a simple sequential pipeline:

retrieve()
generate()

we can represent decisions explicitly:

Retrieve
   ↓
Grade
   ↓
 ┌───────────────┐
 │ Conditional   │
 │    Routing    │
 └───────┬───────┘
         │
    ┌────┴────┐
    ↓         ↓
 Generate   Retrieve

This makes it easier to extend the system with additional agentic behaviors.

---

 Current Limitations

This project is an evolving implementation of Agentic RAG.

Current limitations include:

- Retrieval retries currently use the same user query.
- Retrieval quality can be improved with query rewriting.
- The document grader relies on LLM output.
- Structured outputs can make grading more robust.
- The vector store can be upgraded to persistent/production storage.
- Answer grounding/hallucination evaluation can be added.
- Source citations can be returned with answers.
- Authentication and production security are not yet implemented.
- Evaluation benchmarks are not yet included.

These are intentional areas for future development rather than hidden shortcomings.

---

 Roadmap

 Phase 1 — Basic Agentic RAG

- [x] PDF ingestion
- [x] Text splitting
- [x] Embeddings
- [x] Vector database
- [x] Semantic retrieval
- [x] Document relevance grading
- [x] Conditional LangGraph routing
- [x] Retrieval retry loop
- [x] FastAPI backend

 Phase 2 — Smarter Retrieval

- [ ] Query rewriting
- [ ] Retrieval with rewritten queries
- [ ] Better relevance grading
- [ ] Structured LLM outputs
- [ ] Metadata-aware retrieval
- [ ] Source/page tracking

 Phase 3 — Advanced Agentic RAG

- [ ] Hybrid search
- [ ] BM25 + vector retrieval
- [ ] Reranking
- [ ] Multi-query retrieval
- [ ] Query decomposition
- [ ] Answer relevance grading
- [ ] Hallucination detection
- [ ] Self-correction loop

 Phase 4 — Production

- [ ] Persistent vector storage
- [ ] Docker
- [ ] Authentication
- [ ] Rate limiting
- [ ] Logging
- [ ] Monitoring
- [ ] Automated evaluation
- [ ] CI/CD
- [ ] Cloud deployment
- [ ] Streaming responses

---

 Future Evaluation

The goal is not simply to demonstrate that the system produces answers.

Future versions will evaluate:

- Retrieval precision
- Retrieval recall
- Context relevance
- Answer faithfulness
- Answer correctness
- Latency
- Token usage
- Agent retry frequency

This will make it possible to measure whether agentic behavior actually improves the RAG system rather than simply adding complexity.

---

 Project Goals

This project was built to explore how modern AI systems can combine:

LLMs
 +
Vector Search
 +
RAG
 +
State
 +
Conditional Routing
 +
Evaluation
 +
Self-Correction

The long-term goal is to evolve this prototype into a robust production-grade Agentic RAG architecture capable of dynamically deciding how to retrieve, evaluate, and use information.

---

 Author
Antariksha

GitHub:
https://github.com/antariksha-agi

Repository:
https://github.com/antariksha-agi/agentic-rag

---

 Support

If you found this project useful or interesting, consider giving the repository a ⭐.

It helps the project get noticed and motivates further development.

---

 License

This project is licensed under the terms specified in the repository's "LICENSE" file.# agentic-rag