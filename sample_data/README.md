# Sample data

Three sample documents so anyone can run RagFlow and judge it without supplying
their own files. Two are small hand written business documents, one is a real
public SEC filing, so you can see it work on both clean text and a dense real
world document.

| File | Type | Use case |
|---|---|---|
| acme_employee_handbook.txt | HR policy | Internal policy lookup |
| nimbus_product_faq.txt | Product FAQ | Support and pricing questions |
| nvidia_10k_excerpt.txt | Real SEC 10-K excerpt | Finance questions over a real document |

## Load them

Fully local and keyless with Ollama:

```bash
ollama serve &
ollama pull nomic-embed-text
ollama pull llama3.2:3b
EMBEDDING_PROVIDER=ollama LLM_MODEL=llama3.2:3b python scripts/load_sample_data.py
```

Or, with the service running:

```bash
make load-samples
```

Then start the UI (`make frontend`, at http://localhost:8501) and ask a question.

## Questions to try, with the expected answer

Handbook:
- How many vacation days do new employees get? (15, rising to 25 after five years)
- What is the remote work policy? (up to three days per week)

Product FAQ:
- What does the Nimbus Pro plan cost? (49 dollars per month billed annually)

NVIDIA 10-K:
- What are the building blocks of NVIDIA's platform? (GPUs, CPUs, CUDA, networking)

Honesty check (not in any document):
- What is Acme's parental leave policy? (it should say the documents do not cover this)

## Note on the naive baseline

RagFlow is the 2022 baseline of the line: a single dense retrieval pass with no
reranking. If an answer looks shallow on a harder question, that is expected.
The later rungs add hybrid search and reranking to address exactly that.
