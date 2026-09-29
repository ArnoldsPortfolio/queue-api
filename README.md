# Queue API

Versioned HTTP API that accepts work and processes it through durable queues.

```
src/backend   FastAPI  :8040
src/frontend  Next.js  :3040
```

```bash
cd ~/queue-api/src/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8040
```

```bash
cd ~/queue-api/src/frontend
npm install && npm run dev
```
