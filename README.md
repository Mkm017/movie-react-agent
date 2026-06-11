# Movie Recommendation ReAct Agent

## Demo

![Movie Recommendation Agent Demo](assets/demo.png)

## Overview

This project implements a **ReAct (Reasoning + Acting) Agent** using **LangChain** and **Google Gemini**.

Instead of returning hardcoded movie recommendations, the agent:

1. Understands the user's request.
2. Extracts movie constraints (genre, release period, certification).
3. Calls a live TMDB API tool.
4. Retrieves fresh movie data.
5. Generates a recommendation based on the results.

### Example

User Request:

```text
Recommend a horror movie from the 90s rated R
```

Agent Reasoning:

* Horror → Genre filter
* 90s → Release years 1990–1999
* R → Certification filter

Tool Call:

```json
{
  "genre": "horror",
  "start_year": 1990,
  "end_year": 1999,
  "certification": "R"
}
```

The recommendation is generated using live TMDB data.

---

# Project Structure

```text
movie-react-agent/
│
├── main.py
├── tmdb_tool.py
├── requirements.txt
├── .env
└── README.md
```

### File Description

| File             | Purpose                          |
| ---------------- | -------------------------------- |
| main.py          | Creates and runs the ReAct agent |
| tmdb_tool.py     | TMDB API tool used by the agent  |
| requirements.txt | Project dependencies             |
| .env             | API keys                         |
| README.md        | Project documentation            |

---

# Prerequisites

* Python 3.12
* Google Gemini API Key
* TMDB API Key
* VS Code (recommended)

---

# Create Python 3.12 Virtual Environment

Verify Python 3.12:

```powershell
py -3.12 --version
```

Create virtual environment:

```bash
py -3.12 -m venv venv
```

Activate(Windows):

```bash
venv\Scripts\Activate.ps1
```

You should see:

```text
(venv)
```

in your terminal.

---

# Install Dependencies


```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TMDB_API_KEY=your_tmdb_api_key
```

---

# Running the Project

Start the agent:

```bash
python main.py
```

Example:

```text
Enter your request:

Recommend a horror movie from the 90s rated R
```

---

# Example ReAct Flow

```text
Question:
Recommend a horror movie from the 90s rated R

Thought:
Identify genre

Thought:
Identify year range

Thought:
Identify certification

Action:
movie_search_tool

Action Input:
{
  "genre": "horror",
  "start_year": 1990,
  "end_year": 1999,
  "certification": "R"
}

Observation:
Matching movies returned from TMDB

Thought:
Analyze results and choose the best recommendation

Final Answer:
Recommend Scream (1996)
```

---

# Error Handling

The project includes handling for:

* Missing Gemini API key
* Missing TMDB API key
* Invalid JSON tool input
* Unsupported genres
* Invalid year ranges
* TMDB API errors
* Network timeouts
* No matching movies found

---

