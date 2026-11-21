# Talking Tomatoes 🍅
### Your AI-Powered Entertainment Companion

Talking Tomatoes is an AI-powered entertainment companion designed to make discovering, exploring, and keeping track of movies and TV shows more personal and interactive.

Powered by a large language model (LLM), the application understands natural-language requests, uses external tools to retrieve entertainment information, and maintains user-specific preferences and viewing activity.

Unlike a traditional recommendation system, Talking Tomatoes is being developed as an interactive AI agent that can understand user context, perform tasks, and manage a personalised entertainment library.

---

## Project Objectives

- Build an AI agent capable of understanding natural-language entertainment requests.
- Enable movie and TV show discovery through The Movie Database (TMDB) API.
- Maintain personalised user preferences and viewing history.
- Provide personalised recommendations using user context.
- Support spoiler-conscious conversations based on viewing progress.
- Develop a modular, multi-user application with persistent storage.

---

## Current Features

### 1. AI-Powered Agent
- Natural-language interaction using Groq.
- Tool/function calling for external operations.
- Custom agent execution loop.
- Multiple tool integrations.
- Error handling for tool execution.

### 2. Movie and TV Discovery
Integrated with the TMDB API.

Supported operations:
- Search movies.
- Search TV shows.
- Discover movies and TV shows.
- Retrieve movie and TV show details.
- Find similar movies and TV shows.
- Retrieve supported genres.

### 3. User Management and Database
SQLite provides persistent user-specific storage.

Implemented functionality:
- User creation and retrieval.
- General preferences.
- Liked and disliked genres.
- Personal entertainment library.
- Watchlist, currently watching, completed, and dropped statuses.
- Favourite titles.
- TV viewing progress.
- Viewing history and ratings.

### 4. Database-Integrated Agent
The AI agent can interact with the database through dedicated tools.

- Retrieve user preferences.
- Access personal library information.
- Retrieve viewing history.
- Request database updates through natural language.
- Require explicit confirmation before executing database write operations.
- Isolate database records by user ID.

### 5. Testing
Automated tests using pytest cover:
- Database operations.
- Tool execution.
- Agent behaviour.
- Confirmation workflows.
- Database integration.
- User data isolation.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Groq API | Large language model inference |
| GPT-OSS-20B | Language model |
| TMDB API | Movie and TV show data |
| SQLite | Persistent database |
| Requests | HTTP communication |
| Python-dotenv | Environment configuration |
| Pytest | Automated testing |

---

## System Architecture

Talking Tomatoes follows a modular architecture separating the AI agent, tools, external services, and database operations.

```text
                USER
                  |
                  v
             AI AGENT
                  |
           Groq LLM API
                  |
                  v
             TOOL CALLS
                  |
          TOOL EXECUTOR
             /       \
            /         \
           v           v
      TMDB TOOLS   DATABASE TOOLS
           |           |
           v           v
       TMDB API      SQLite
                       |
                 USER-SPECIFIC
                      DATA
```

Database write operations pass through a confirmation mechanism before execution.

---

## Project Structure

```text
Talking-Tomatoes/
│
├── src/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── tool_executor.py
│   │   └── confirmation.py
│   │
│   ├── tools/
│   │   ├── movie_discovery.py
│   │   ├── tool_schemas.py
│   │   └── database_tools.py
│   │
│   ├── services/
│   │   └── tmdb_client.py
│   │
│   └── database/
│       ├── connection.py
│       ├── schema.py
│       └── operations.py
│
├── tests/
│   ├── test_movie_discovery.py
│   ├── test_tool_executor.py
│   ├── test_agent.py
│   ├── test_database.py
│   └── test_agent_database_integration.py
│
├── data/
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
├── README.md
└── run_groq.py
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Fatimaaasaleem/Talking-Tomatoes.git

cd Talking-Tomatoes
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Add your Groq API key and TMDB API credentials using the environment variable names expected by the application.

Never commit API keys or other secrets to GitHub.

### 5. Run the application

```bash
python run_groq.py
```

---

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

The project includes unit tests and integration tests using an isolated temporary SQLite database.

---

## Development Roadmap

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Basic AI tool-calling agent | Completed |
| Phase 2 | TMDB API integration | Completed |
| Phase 3 | SQLite database and agent integration | Completed |
| Phase 4 | Personalised recommendations and feedback | In progress |
| Phase 5 | Spoiler-safe entertainment companion | Planned |
| Phase 6 | Authentication, FastAPI and frontend | Planned |
| Phase 7 | Testing, refinement and deployment | Planned |

---

## Future Vision

Talking Tomatoes aims to evolve into a personalised entertainment companion that understands not only what users want to watch, but also their preferences, viewing habits, interests, and feedback.

Future development will focus on:

- Context-aware personalised recommendations.
- Recommendation feedback and preference learning.
- Spoiler-conscious conversations.
- Authentication and multi-user application support.
- Web-based user interface.
- Production deployment and scalability.

---

## Author

**Fatima Saleem**

Computer Science Student | AI and Machine Learning Enthusiast

GitHub: [Fatimaaasaleem](https://github.com/Fatimaaasaleem)

---

*Talking Tomatoes is an ongoing software development project focused on building practical AI-powered applications using LLMs, APIs, tool calling, and persistent user context.*