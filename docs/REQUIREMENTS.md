# Requirements

1. Support to all Zoro-DB API methods
2. Connection, authentication, retry and error handling
3. Fully managed embeddings workflow
4. Also Support embeddings from user side
5. Basic input validations

# Folder Structure

```text
zoro_client/
├── __init__.py
├── client.py
├── collections.py
├── embeddings/
│   ├── base.py
│   ├── openai.py
├── models/
│   ├── collection.py
│   ├── embedding.py
│   ├── point.py
│   ├── document.py
```

# Low Level Design Requirements

- class based
- tests for all components

# Personal Note

- don't use chatgpt to write code, read docs, experiment evrery single line
