<div align="center">

# 🚀 InterviewAce AI — Your Personal Interview Wingman

> **Stop guessing. Start preparing. Land the job.**
> A multi-agent AI system that does the heavy lifting — company research, resume analysis, 50 tailored questions, salary intel, and a full prep kit — all in under 5 minutes.

---

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA%20NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
</div>

---

## 🤔 Why This Exists

Most people walk into interviews unprepared — they Google the company 10 minutes before, guess what questions might come up, and have no idea what salary to ask for.

**InterviewAce AI fixes that.**

It researches the company, digs into your resume, matches it against the job description, builds 50 questions tailored to YOUR experience, and even hands you word-for-word salary negotiation scripts. For every job seeker — freshers, mid-level, and senior professionals alike.

---

## ✨ What It Does

| 🔍 Research | 📝 Analysis | 🎯 Coaching |
|---|---|---|
| Company overview & culture | Resume vs JD keyword match | 25 technical questions |
| Interview rounds & format | Before/after bullet rewrites | 25 behavioral questions |
| Glassdoor & AmbitionBox reviews | Missing skills identification | Topic-wise study plan |
| Real salary data (not LLM guesses!) | Readiness score (1–10) | Salary negotiation scripts |

---

## 🧠 How the Agents Work Together

```
  You fill the form
        │
        ▼
┌───────────────┐     ┌──────────────────────┐     ┌──────────────────┐     ┌────────────────┐
│  INPUT AGENT  │────▶│   RESEARCH AGENT     │────▶│   COACH AGENT   │────▶│ REPORT AGENT  │
│               │     │                      │     │                  │     │                │
│ Validates &   │     │ NVIDIA NIM + Tavily  │     │ Groq (6 calls)  │     │ Assembles &    │
│ cleans your   │     │ 10 web searches      │     │ Resume review    │     │ formats your   │
│ inputs        │     │ Salary extraction    │     │ 50 questions     │     │ full prep kit  │
│               │     │ Company synthesis    │     │ Salary scripts   │     │ → Download!    │
└───────────────┘     └──────────────────────┘     └──────────────────┘     └────────────────┘
```

**Agent 1 (NVIDIA NIM)** — Runs 10 Tavily searches, pulls real salary numbers via regex from AmbitionBox/Glassdoor, and synthesizes everything into structured insights.

**Agent 2 (Groq — Llama 3.3 70B)** — Makes 6 focused LLM calls for resume analysis, study plan, 25 technical + 25 behavioral questions, and salary negotiation scripts.

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/PriyankaSawant11/InterviewAce-AI.git
cd InterviewAce-AI
```

### 2. Set up Python environment
```bash
# Create virtual environment
py -3.11 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add your API keys
```bash
cp .env.example .env
# Open .env and fill in your 3 free API keys
```

### 5. Launch the app
```bash
streamlit run app.py
```
🌐 Opens at **http://localhost:8501**

---

## 🔑 3 Free API Keys You Need

No credit card required for any of them!

### 🟢 Groq — Ultra-fast LLM for coaching
| | |
|---|---|
| Free Tier | 14,400 requests/day |
| Sign Up | [console.groq.com](https://console.groq.com) |
| Key looks like | `gsk_...` |

### 🟢 NVIDIA NIM — Research synthesis
| | |
|---|---|
| Free Tier | 1,000 credits on signup |
| Sign Up | [build.nvidia.com](https://build.nvidia.com) |
| Key looks like | `nvapi-...` |

### 🟢 Tavily — AI-powered web search
| | |
|---|---|
| Free Tier | 1,000 searches/month |
| Sign Up | [app.tavily.com](https://app.tavily.com) |
| Key looks like | `tvly-...` |

Your `.env` file should look like:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🎮 How to Use It

1. **Enter Company Name** — e.g. `Google`, `Infosys`, `Razorpay`
2. **Enter Your Target Role** — e.g. `Data Scientist`, `ML Engineer`
3. **Enter Experience** — e.g. `Fresher`, `2 years`, `5 years`
4. **Paste the Job Description** — copy it directly from the job posting
5. **Upload Your Resume** — PDF format
6. **Click "Prepare Me for the Interview"** — sit back for 3–5 minutes

### What you get back:

```
🟢 Readiness Score        — Are you ready? Honest rating out of 10
🏢 Company Brief          — What you MUST know before walking in
💡 Key Facts              — Funding, tech stack, recent news
🔄 Interview Process      — Round-by-round breakdown
🏛️ Culture & Reviews      — Real employee experiences
📝 Resume Review          — Keyword gaps + rewritten bullets
📚 Study Plan             — What to study, in what order, how long
🎤 50 Questions           — 25 technical + 25 behavioral
💰 Salary Strategy        — Real data + word-for-word scripts
🚩 Red Flags              — Concerns worth knowing upfront
📥 Download Report        — Take it all offline
```

---

## 🛠 Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Agent Orchestration | LangGraph | Manages the multi-agent workflow as a graph |
| Research LLM | NVIDIA NIM — Llama 3.1 70B | Deep synthesis of web research |
| Coaching LLM | Groq — Llama 3.3 70B | Ultra-fast generation for coaching outputs |
| Web Search | Tavily | Structured, content-rich search results |
| PDF Parsing | PyMuPDF | Reliable resume text extraction |
| UI | Streamlit | Clean, interactive web app |
| Config | python-dotenv | Secure API key management |

---

## 📁 Project Structure

```
InterviewAce-AI/
│
├── .streamlit/
│   └── config.toml          # Custom dark theme
│
├── nodes/
│   ├── collect_input.py     # Input validation
│   ├── agent1_research.py   # NVIDIA NIM + Tavily research
│   ├── agent2_coach.py      # Groq coaching (6 LLM calls)
│   └── generate_report.py   # Report assembly
│
├── tools/
│   ├── search_tool.py       # Tavily search wrapper
│   └── scraper_tool.py      # URL content extraction
│
├── utils/
│   └── resume_parser.py     # PDF text extraction
│
├── app.py                   # Streamlit UI
├── graph.py                 # LangGraph state + graph
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⏱ Performance

| Phase | Time | What's Happening |
|---|---|---|
| Web searches (10x) | ~12 sec | Parallel Tavily searches |
| NVIDIA synthesis | 2–3 min | One big LLM call |
| Groq coaching (6x) | ~2 min | 6 calls with rate-limit delays |
| **Total** | **3–5 min** | Complete prep kit ready |

---

## 🐛 Common Issues & Fixes

| Problem | Fix |
|---|---|
| `Groq 429 error` | Wait 60 seconds (rate limit). Daily limit? Wait 24 hrs. |
| `NVIDIA 504 timeout` | Try again — occasional latency on free tier |
| `venv not activating (Windows)` | Run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Python version error` | Use Python 3.11 specifically |
| `Missing fitz` | Run: `pip install pymupdf` |
| `Missing tavily-python` | Run: `pip install tavily-python` |
| Salary shows `UNVERIFIED` | Pages didn't have explicit ₹ amounts — LLM estimate used |

---

## 🔍 Reading Terminal Logs

Every API call is logged so you know exactly what's happening:

```
[AGENT1] INFO: Search 3/10: Glassdoor reviews
[AGENT1] DEBUG: Search result: 1832 chars
[AGENT1] INFO: NVIDIA NIM response: 3116 chars
[AGENT2] INFO: Groq 'resume review': 2863 chars
[AGENT2] INFO: JSON parsed OK ✅
[AGENT2] ERROR: JSON parse FAILED ❌ → check this line
```

---

## 🙋 Who Is This For?

- 🎓 **Freshers** applying for their first job
- 💼 **Mid-level professionals** switching companies
- 🧑‍💻 **Senior folks** targeting competitive roles
- 🌏 **Anyone** who wants to walk in prepared, not panicked

---

## 📜 License

MIT License — free to use, modify, and share.

---

<div align="center">

**Built with [LangGraph](https://github.com/langchain-ai/langgraph) · [NVIDIA NIM](https://build.nvidia.com) · [Groq](https://groq.com) · [Tavily](https://tavily.com) · [Streamlit](https://streamlit.io)**

*All free-tier APIs. No GPU required. Runs on any laptop.*

<p align="center">⭐ Star this repo if it helped you land an interview!</p>

</div>