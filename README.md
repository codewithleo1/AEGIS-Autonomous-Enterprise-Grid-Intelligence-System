# ⚡ AEGIS — Autonomous Enterprise Grid Intelligence System

> An AI-powered enterprise IT helpdesk built with Groq's LLaMA 3.3-70b, FastAPI, and React.
> No LangChain. No wrappers. Pure tool-use loop in ~50 lines.

**🔴 Live Demo (Employee Portal):** https://aegis-autonomous-enterprise-grid-in-seven.vercel.app  
**🟢 Live Demo (Agent Dashboard):** https://aegis-autonomous-enterprise-grid-in-alpha.vercel.app  
**📦 Backend API:** https://aegis-helpdesk.onrender.com/health  
**💻 GitHub:** https://github.com/codewithleo1/AEGIS-Autonomous-Enterprise-Grid-Intelligence-System

---

## 🎯 What Is AEGIS?

AEGIS is a production-grade AI helpdesk assistant for TechCorp's internal IT team.
Employees can raise tickets, check status, look up colleagues, and generate reports —
all through a natural language chat interface powered by Groq's ultra-fast LPU inference.

Built to demonstrate **SaaS-level AI engineering** without LangChain or any agent framework.

---

## 🖥️ Screenshots

### Employee Portal — Login
![Employee Login](docs/01_employee-login.png)

### Employee Portal — AI Chat with Live Agent Activity
> Three-panel UI: ticket sidebar · AI chat · live tool call trace

![Employee Portal](docs/02_employee-portal.png)

### Employee Portal — Ticket Created via Natural Language
> Employee describes the issue in plain English. AEGIS calls `create_ticket`, returns a structured confirmation.

![Ticket Created](docs/03_ticket-created.png)

### Agent Dashboard — Login
![Agent Dashboard Login](docs/04_IT-agent-dashboard-login.png)

### Agent Dashboard — Full Ticket Queue
> 28 tickets sorted by priority (CRITICAL → HIGH → MEDIUM → LOW). Filter by status or priority.

![Agent Dashboard](docs/05_agent-dashboard.png)

### Agent Dashboard — Resolve Ticket Modal
> Agent adds a resolution note before closing a ticket. PATCH request updates PostgreSQL in real time.

![Resolve Modal](docs/06_resolve-modal.png)

### Backend API — Swagger UI
> All routes documented. Lock icons indicate JWT-protected endpoints.

![Swagger API](docs/07_swagger-api.png)

---

## 🏗️ Architecture

```
User (Browser)
    ↓ HTTPS
Vercel (React + Vite frontend)
    ↓ POST /ask  Authorization: Bearer <JWT>
Render (FastAPI backend)
    ├── Auth middleware — JWT verification
    ├── Rate limiting — SlowAPI (30 req/min)
    ├── Groq API — llama-3.3-70b-versatile
    │   └── Tool-use loop (finish_reason == "tool_calls")
    ├── Tool Executor — dispatches to 6 business tools
    ├── Upstash Redis — per-session conversation memory
    └── Supabase PostgreSQL — tickets + employees
```

### How the Tool-Use Loop Works

```
1. User sends message
2. Groq receives: system prompt + chat history + tool schemas
3. Groq decides: answer directly OR call a tool
4. If tool needed → finish_reason = "tool_calls"
5. Backend executes tool → queries PostgreSQL
6. Tool result sent back as role="tool" with tool_call_id
7. Groq generates final human-readable response
8. Session history saved to Redis (Upstash)
9. Response returned to frontend
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| LLM | Groq llama-3.3-70b-versatile | Free (14,400 req/day), ultra-fast LPU inference |
| Backend | FastAPI + Python 3.12 | Async, fast, production-grade |
| Validation | Pydantic v2 | Industry standard for FastAPI |
| Auth | JWT (python-jose) | Stateless, role-based, no API key in browser |
| Session Store | Upstash Redis | Free tier, no infra to manage |
| Database | Supabase PostgreSQL | Free tier, 500MB, managed |
| ORM | SQLAlchemy async 2.0 | Non-blocking DB queries |
| Frontend | React + Vite + Tailwind | Fast, modern, zero-config |
| Frontend Hosting | Vercel | Free, auto-deploys from GitHub |
| Backend Hosting | Render | Free tier, permanent URL |
| Containerization | Docker + docker-compose | Production deployment pattern |
| Package Manager | uv | 10-100x faster than pip |
| Linter | Ruff | One tool replaces flake8 + black |

> ✅ Every service used has a free tier. Total cost to run: $0.

---

## 🤖 The 6 Business Tools

| Tool | Purpose |
|---|---|
| `create_ticket` | Raise a new IT support ticket with auto-assigned agent |
| `get_ticket_status` | Check status of any ticket by ID |
| `list_tickets` | List tickets with filters (status, priority, category) |
| `get_employee_info` | Look up employee profile by Employee ID |
| `update_ticket` | Update ticket status and add resolution notes |
| `generate_report` | Generate helpdesk summary report with breakdowns |

---

## 🔐 Auth & Security

- **JWT-based auth** — employees and agents log in and receive a signed token
- **Role-based access** — employees see only their own tickets; agents see all
- **No API key in browser** — frontend sends only JWT; API key never exposed to client
- **Rate limiting** — 30 requests/min per token via SlowAPI

---

## 🚀 Run Locally

### Prerequisites
- Python 3.12
- Node.js 18+
- uv (`pip install uv`)
- Docker Desktop (optional)

### 1. Clone the repo
```bash
git clone https://github.com/codewithleo1/AEGIS-Autonomous-Enterprise-Grid-Intelligence-System
cd AEGIS-Autonomous-Enterprise-Grid-Intelligence-System
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Fill in your keys in .env
```

Required keys:
```
GROQ_API_KEY=your_groq_key
AEGIS_API_KEY=your_chosen_api_key
DATABASE_URL=postgresql+asyncpg://...
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
JWT_SECRET=your_jwt_secret
APP_ENV=development
```

### 3. Install backend dependencies
```bash
uv sync
```

### 4. Seed the database
```bash
uv run python seed.py
```

### 5. Run the backend
```bash
uv run uvicorn backend.main:app --reload
```

### 6. Run the employee frontend
```bash
cd frontend
npm install
npm run dev
```

### 7. Run the agent dashboard
```bash
cd agent-dashboard
npm install
npm run dev
```

Open http://localhost:5173 (employee) and http://localhost:5174 (agent)

**Demo credentials:**

| Portal | Email | Password |
|---|---|---|
| Employee | raj.sharma@techcorp.com | aegis1234 |
| Agent | kiran.pillai@techcorp.com | aegis1234 |

### Or run with Docker
```bash
cd docker
docker compose up --build
```

---

## 🧪 Tests

```bash
uv run pytest tests/ -v
```

**30/30 tests passing** across:
- Auth middleware
- Health endpoint
- Helpdesk routes + session management
- Employee service
- Ticket service (CRUD)
- Report service
- Tool executor

---

## 💼 Key Engineering Decisions

**Why Groq over OpenAI/Anthropic?**  
Groq runs on custom LPU hardware — significantly faster inference than GPU-based APIs.
The free tier (14,400 req/day) is generous enough for production demo use.

**Why no LangChain?**  
LangChain adds abstraction layers, deprecated wrappers, and version conflicts.
Groq's SDK is OpenAI-compatible — the tool-use loop is ~50 lines of clean Python.

**Why async SQLAlchemy?**  
FastAPI is async. Mixing sync DB calls with an async framework blocks the event loop
and kills performance under concurrent load. Full async stack = non-blocking throughout.

**Why JWT over API key?**  
API keys exposed in the browser are a security risk — anyone can copy them from the network tab.
JWT tokens are short-lived, role-scoped, and never reveal backend secrets.

**Why mock services first?**  
Building the tool-use loop against in-memory dicts let us validate the entire
AI pipeline before touching a database. Faster iteration, cleaner separation of concerns.

---

## 📁 Project Structure

```
aegis/
├── backend/
│   ├── main.py              ← FastAPI app + middleware
│   ├── agent/
│   │   ├── groq_client.py   ← Groq SDK tool-use loop
│   │   ├── tools.py         ← 6 tool JSON schemas
│   │   └── tool_executor.py ← Dynamic tool dispatch
│   ├── services/            ← Business logic (DB queries)
│   ├── db/                  ← SQLAlchemy models + Redis session
│   ├── api/routes/          ← FastAPI route handlers
│   └── api/middleware/      ← JWT auth + rate limiting
├── frontend/                ← Employee portal (React + Vite)
├── agent-dashboard/         ← Agent portal (React + Vite)
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/                   ← 30 tests, all passing
└── seed.py                  ← DB seed script
```

---

## 👨‍💻 Built By

**Suraj Chopade** — AI Engineer  
[Code With Leo](https://github.com/codewithleo1) · Building production-grade AI systems

---

*Built to demonstrate production-grade AI engineering for job applications.*  
*Every architectural decision has a reason. Every line of code has a purpose.*
