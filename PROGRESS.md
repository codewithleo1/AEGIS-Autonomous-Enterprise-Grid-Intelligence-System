# AEGIS — Autonomous Enterprise Grid Intelligence System
# PROGRESS.md
> Paste this file at the start of every new Claude chat to resume instantly.
> Tell Claude: "Read this fully before we continue. We are on Step X."

---

## 🤖 Project Identity

- **Name:** AEGIS
- **Full Name:** Autonomous Enterprise Grid Intelligence System
- **Company:** TechCorp Internal IT Helpdesk
- **Builder:** Leo (Code With Leo / CWL brand)
- **Version:** 1.0 (Groq native tool-use, no LangChain)
- **Purpose:** Land an AI Engineer role by demonstrating production-grade AI systems

---

## 🎯 Project Overview

Building an industry SaaS-level Enterprise Helpdesk AI using:
- Groq's **OpenAI-compatible tool-use API** with llama-3.3-70b-versatile (no LangChain — cleaner, more reliable)
- FastAPI backend with API key auth + rate limiting
- PostgreSQL for ticket/employee data persistence
- Redis for per-session conversation memory
- React + Vite frontend
- Docker + docker-compose for deployment

**Portfolio Goal:** Demonstrate to employers the ability to build
production-grade AI systems using Groq's API with real
SaaS patterns (auth, rate limiting, async DB, session memory).

**GitHub:** https://github.com/codewithleo1/AEGIS-Autonomous-Enterprise-Grid-Intelligence-System
**Live Demo:** [add deployed URL here]

---

## 🧑‍💻 Developer Environment

- OS: Windows
- Editor: VS Code
- Shell: PowerShell
- Package Manager: uv (NOT pip)
- Python: 3.12
- Linter: ruff

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Cost |
|---|---|---|---|
| LLM | llama-3.3-70b-versatile via Groq SDK | latest | Free tier (14,400 req/day) |
| Backend | FastAPI | ≥0.139 | Free |
| Validation | Pydantic v2 | ≥2.0 | Free |
| Session Store | Upstash Redis | 7+ | Free tier (10k cmd/day) |
| Database | Supabase PostgreSQL | 15+ | Free tier (500MB) |
| ORM | SQLAlchemy async | 2.0+ | Free |
| Frontend | React + Vite | latest | Free |
| Frontend Hosting | Vercel | latest | Free tier |
| Backend Hosting | Fly.io | latest | Free tier (3 VMs) |
| Deployment | Docker + docker-compose | latest | Free |
| Linter | Ruff | latest | Free |
| CI/CD | GitHub Actions | latest | Free (2000 min/month) |

> ✅ Every tool in this stack has a free tier. No paid services required.

---

## 📁 Folder Structure

---

aegis/
├── PROGRESS.md                  ← project brain (this file)
├── .env                         ← secrets (never commit)
├── .env.example                 ← safe template (commit this)
├── .gitignore
├── pyproject.toml               ← uv manages dependencies here
├── backend/
│   ├── main.py                  ← FastAPI app entry point
│   ├── config.py                ← all settings via pydantic-settings
│   ├── logger.py                ← centralised logging utility
│   ├── api/
│   │   ├── routes/
│   │   │   ├── helpdesk.py      ← POST /ask, DELETE /session/{id}
│   │   │   ├── tickets.py       ← GET /tickets (list + filter)
│   │   │   └── health.py        ← GET /health
│   │   └── middleware/
│   │       ├── auth.py          ← API key header verification
│   │       └── rate_limit.py    ← slowapi 30 req/min per key
│   ├── agent/
│   │   ├── groq_client.py       ← Groq SDK + tool-use loop
│   │   ├── tools.py             ← 6 tool JSON schemas (OpenAI format)
│   │   └── tool_executor.py     ← dispatches tool calls to services
│   ├── services/
│   │   ├── ticket_service.py    ← create/get/list/update tickets
│   │   ├── employee_service.py  ← get employee info
│   │   └── report_service.py    ← generate summary reports
│   ├── db/
│   │   ├── postgres.py          ← async SQLAlchemy engine + session
│   │   ├── redis_session.py     ← save/load per-session chat history
│   │   └── models.py            ← ORM table definitions
│   └── schemas/
│       ├── request.py           ← AskRequest Pydantic model
│       └── response.py          ← AskResponse Pydantic model
├── frontend/                    ← React app (Phase 3)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── ToolActivityPanel.jsx
│   │   └── api/
│   │       └── helpdesk.js      ← axios calls to FastAPI
│   └── package.json
└── docker/
├── Dockerfile               ← multi-stage build
└── docker-compose.yml       ← app + postgres + redis

---

## ✅ Completed Steps

- [x] Step 1:  Project scaffold + uv init + folder structure
- [x] Step 2:  Install dependencies (fastapi, groq, pydantic-settings, etc.)
- [x] Step 3:  .env.example + .gitignore + config.py
- [x] Step 4:  Pydantic schemas — request.py + response.py
- [x] Step 5:  Tool definitions — tools.py (6 tool JSON schemas)
- [x] Step 6:  Groq client + tool-use loop — groq_client.py
- [x] Step 7:  Tool executor — tool_executor.py
- [x] Step 8:  Mock services — ticket, employee, report (in-memory)
- [x] Step 9:  FastAPI routes — health.py + helpdesk.py
- [x] Step 10: Auth middleware — auth.py
- [x] Step 11: Rate limiting — rate_limit.py
- [x] Step 12: Logging utility — logger.py
- [x] Step 13: main.py — wire everything together
- [x] Step 14: Test with curl + Swagger UI — 42/42 tests passing
- [x] Step 15: Redis session store — redis_session.py (Upstash)
- [x] Step 16: PostgreSQL models + async engine (Supabase)
- [ ] Step 17: Replace mock services with real DB queries
- [ ] Step 18: React frontend
- [ ] Step 19: Docker + docker-compose
- [ ] Step 20: Deploy — Fly.io + Vercel + Upstash + Supabase
- [ ] Step 21: Final README + screenshots for portfolio

---

## 🔄 Current Step

**Step 17 — Replace mock services with real DB queries**

Last action: PostgreSQL tables created on Supabase, async engine connected, 42 tests passing
Next action: Seed the DB with mock data, rewrite services to use real SQL queries

---

## ⏭️ Next Steps Queue

1. Create seed script to populate employees + tickets in Supabase
2. Rewrite employee_service.py — replace dict lookups with DB queries
3. Rewrite ticket_service.py — replace dict operations with DB queries
4. Rewrite report_service.py — replace in-memory aggregation with DB queries
5. Update tests to work with real DB
6. Run full test suite — confirm passing
7. Commit and move to Step 18 — React frontend

---

## 🐛 Gotchas & Known Bugs

> Every bug fixed gets added here immediately. Never repeat a known bug.

| # | Bug | Fix |
|---|-----|-----|
| 1 | PowerShell: `&&` not supported | Always use separate lines |
| 2 | `uv run python` vs `python` | Always prefix with `uv run` |
| 3 | Groq SDK: `finish_reason` is `"tool_calls"` not `"stop"` when tool is needed | Always check `finish_reason == "tool_calls"` before reading text |
| 4 | Groq SDK: tool calls are in `message.tool_calls`, not `message.content` | Access via `response.choices[0].message.tool_calls` |
| 5 | Groq SDK: tool result must be sent back as role `"tool"` with matching `tool_call_id` | Always echo the `tool_call_id` from the tool call |
| 6 | Pydantic v2: `parse_obj()` removed | Use `model_validate()` instead |
| 7 | FastAPI: sync functions block async event loop | All route functions must be `async def` |
| 8 | SQLAlchemy 2.0: `session.execute()` returns `Row` not dict | Use `.mappings()` or `model_validate()` |
| 9 | Redis: connection not closed after use | Always use `async with` or `await r.aclose()` |
| 10 | Upstash Redis: requires REST URL + token, not standard redis:// URI | Use `upstash-redis` Python SDK or HTTP client |
| 11 | Supabase: connection string uses `postgresql+asyncpg://` not `postgres://` | Always use `postgresql+asyncpg://` for async SQLAlchemy |
| 12 | Supabase direct connection fails on Windows (IPv6 issue) | Use Session Pooler URL: aws-X-ap-south-1.pooler.supabase.com |
| 13 | Password with special chars (@ # $) in DATABASE_URL breaks URI | Use only letters and numbers in DB password |
| 14 | New-Item in PowerShell creates empty files | Use write_*.py helper scripts to write file content |

---

## 🧠 Key Decisions & Why

| Decision | Reason |
|---|---|
| Groq over Anthropic/OpenAI | 100% free tier (14,400 req/day), ultra-fast inference (LPU hardware) |
| llama-3.3-70b-versatile | Best open-source model for tool use on Groq; strong reasoning |
| Groq native SDK over LangChain | No deprecated wrappers, direct control over tool-calling loop, ~50 lines |
| OpenAI-compatible format | Groq uses OpenAI's tool schema — easy to switch providers if needed |
| uv over pip | 10-100x faster installs, modern Python standard |
| Pydantic v2 | Industry standard validation for FastAPI |
| Upstash Redis (free) over self-hosted | Free tier, no infra to manage, works with Fly.io |
| Supabase PostgreSQL (free) over self-hosted | Free tier, 500MB, managed backups |
| Async SQLAlchemy | Non-blocking DB = handles more concurrent users |
| Ruff over flake8+black | One tool replaces both, runs faster |
| Mock services first, real DB later | Lets us test tool loop without DB setup complexity |
| Fly.io over Render/Railway | Render removed free tier; Fly.io still has 3 free shared VMs |
| Vercel for frontend | Best free static + React hosting, zero config |
| 6 tools (added update_ticket) | Tickets need to be resolved; completes the helpdesk workflow |
| Centralised logger.py | Standard in production; logs every tool call for debugging |
| Session Pooler over Direct connection | Direct connection uses IPv6 which fails on Windows/some networks |

---

## 📝 Coding Rules (Never Break These)

1. **Explain concept before code** — learning is the priority
2. **One file at a time** — wait for terminal output before next file
3. **Never use `&&` in PowerShell** — always separate lines
4. **Always use `uv run` prefix** — never raw `python` command
5. **Run `uv run ruff check --fix` before every commit**
6. **Commit working code before extending it**
7. **Update PROGRESS.md after every completed step**
8. **Add every new bug to Gotchas immediately when found**
9. **Never re-introduce a bug from the Gotchas list**
10. **Check PROGRESS.md Gotchas before writing any new code**
11. **Always give all files upfront** — never one file at a time unless asked
12. **Always explain what changed and why before showing updated code**

---

## 💼 Portfolio Notes

**What to say in interviews:**
> "I built AEGIS — an Autonomous Enterprise Grid Intelligence System —
> using Groq's API with llama-3.3-70b-versatile, replacing LangChain entirely.
> The system routes employee queries to 6 business tools using OpenAI-compatible
> function calling, maintains per-session memory in Redis on Upstash, and is
> deployed on Fly.io with a FastAPI backend and PostgreSQL on Supabase.
> I chose Groq over other providers because it's completely free at scale
> and its LPU hardware delivers significantly faster inference than GPU-based APIs."

**Key concepts this project demonstrates:**
- LLM tool use / function calling (core AI engineering skill)
- Async Python — FastAPI + async SQLAlchemy
- Session memory management — Redis (Upstash)
- API security — key-based auth + rate limiting
- Production deployment — Docker + Fly.io + Vercel
- Clean architecture — separation of concerns across layers
- Centralised logging — production observability pattern
- Provider-agnostic design — OpenAI-compatible schema means easy LLM swap

---

## 📋 How to Resume in a New Chat

Paste this exactly at the top of a new Claude chat: