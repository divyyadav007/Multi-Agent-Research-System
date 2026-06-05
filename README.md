# AI Research Assistant

An AI-powered research automation system that performs real-time web research, extracts relevant information from online sources, generates structured research reports, and automatically evaluates report quality using a multi-stage agentic workflow.

Built using LangChain, Mistral AI, Tavily Search API, and BeautifulSoup.

---

## Project Overview

Traditional LLMs rely on static training data and may not have access to the latest information.

This project solves that problem by combining:

- Real-time web search
- Intelligent source selection
- Web content extraction
- AI-powered report generation
- Automated quality evaluation

The system researches a topic end-to-end with minimal human intervention.

---

# Key Features

### Real-Time Research

Searches the web using Tavily Search API to retrieve recent and relevant information.

### Agent-Based Workflow

Uses specialized AI components for:

- Search
- Reading
- Writing
- Critique

### Intelligent Content Extraction

Scrapes and cleans webpage content using BeautifulSoup.

### Automated Report Writing

Generates structured research reports including:

- Introduction
- Key Findings
- Conclusion
- Sources

### Self-Evaluation Layer

A Critic module reviews generated reports and provides:

- Quality score
- Strengths
- Areas for improvement

### Modular Architecture

Each component is independently maintainable and extensible.

---

# System Architecture

```text
                    ┌────────────────────┐
                    │     User Topic     │
                    └─────────┬──────────┘
                              │
                              ▼

               ┌──────────────────────────┐
               │     Research Pipeline    │
               │      (pipeline.py)       │
               └────────────┬─────────────┘
                            │

        ┌───────────────────┼───────────────────┐
        ▼                                       ▼

┌─────────────────┐                  ┌─────────────────┐
│  Search Agent   │                  │  Reader Agent   │
└────────┬────────┘                  └────────┬────────┘
         │                                    │
         ▼                                    ▼

┌─────────────────┐                  ┌─────────────────┐
│ Tavily Search   │                  │ BeautifulSoup   │
│ Real-time Web   │                  │ Web Scraper     │
└────────┬────────┘                  └────────┬────────┘
         │                                    │
         └──────────────┬─────────────────────┘
                        ▼

              ┌──────────────────────┐
              │ Knowledge Aggregator │
              └──────────┬───────────┘
                         ▼

              ┌──────────────────────┐
              │    Writer Chain      │
              │ Report Generation    │
              └──────────┬───────────┘
                         ▼

              ┌──────────────────────┐
              │ Research Report      │
              └──────────┬───────────┘
                         ▼

              ┌──────────────────────┐
              │    Critic Chain      │
              │ Quality Evaluation   │
              └──────────┬───────────┘
                         ▼

              ┌──────────────────────┐
              │ Score + Feedback     │
              └──────────────────────┘
```

---

# Workflow

## Stage 1 — Search

The Search Agent uses Tavily Search API to retrieve recent information about the research topic.

Output:

- Titles
- URLs
- Content snippets

---

## Stage 2 — Reading

The Reader Agent analyzes search results and selects the most relevant source.

The selected webpage is scraped and cleaned using BeautifulSoup.

Output:

- Detailed webpage content

---

## Stage 3 — Report Generation

The Writer Chain combines:

- Search results
- Scraped content

and generates a structured research report.

Output Sections:

- Introduction
- Key Findings
- Conclusion
- Sources

---

## Stage 4 — Quality Assurance

The Critic Chain evaluates:

- Accuracy
- Structure
- Clarity
- Completeness

Output:

- Numerical score
- Strengths
- Areas to improve

---

# Tech Stack

## AI & LLM

- LangChain
- Mistral AI

## Search

- Tavily Search API

## Web Scraping

- BeautifulSoup4
- Requests

## Backend

- Python

## Configuration

- python-dotenv

## Logging

- Rich

---

# Project Structure

```bash
project/
│
├── agents.py
├── pipeline.py
├── tools.py
├── .env
├── requirements.txt
└── README.md
```

### agents.py

Contains:

- Search Agent
- Reader Agent
- Writer Chain
- Critic Chain

### tools.py

Contains:

- Tavily Search Tool
- URL Scraper Tool

### pipeline.py

Orchestrates the complete research workflow.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/AI-Research-Assistant.git

cd AI-Research-Assistant
```

## Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key

TAVILY_API_KEY=your_tavily_api_key
```

---

# Usage

Run:

```bash
python pipeline.py
```

Example:

```text
Enter Research Topic:

Latest Developments in Artificial Intelligence
```

---

# Sample Output

## Research Report

```text
Introduction
...

Key Findings
...

Conclusion
...

Sources
...
```

## Critic Review

```text
Score: 8.5/10

Strengths:
- Good source coverage
- Clear structure

Areas to Improve:
- Add more supporting evidence
- Include additional sources

Verdict:
Well-structured report with good factual grounding.
```

---

# Engineering Decisions

### Why Tavily?

Tavily provides LLM-optimized search results and real-time web access.

### Why BeautifulSoup?

It enables lightweight webpage extraction and content cleaning.

### Why Multi-Stage Workflow?

Separating Search, Reading, Writing, and Critique improves modularity and maintainability.

### Why Critic Chain?

Adds an automated quality assurance layer and reduces low-quality outputs.

---

# Challenges Solved

- Real-time information retrieval
- Source selection
- Content extraction
- Information synthesis
- Automated report evaluation
- Hallucination reduction through external search

---

# Future Improvements

Planned upgrades:

- LangGraph-based orchestration
- Parallel multi-source scraping
- Streamlit UI
- Docker deployment
- LangSmith tracing
- Structured output using Pydantic
- PDF export
- Human-in-the-loop review
- RAG integration
- Vector database support

---

# Resume Description

Developed an AI-powered Research Assistant using LangChain, Mistral AI, Tavily Search API, and BeautifulSoup.

Designed a multi-stage agentic workflow for real-time information retrieval, web content extraction, report generation, and automated quality evaluation.

Implemented end-to-end research automation capable of generating structured reports from live web data while reducing hallucinations through external knowledge retrieval.

---

# Interview Topics Covered

- Agentic AI Systems
- LangChain
- Tool Calling
- Prompt Engineering
- Web Scraping
- LLM Orchestration
- Information Retrieval
- Research Automation
- AI Evaluation Pipelines

---

# License

This project is developed for educational, research, and portfolio purposes.
