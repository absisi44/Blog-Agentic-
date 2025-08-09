# Multilingual Blog Generator

## Overview

This project generates blog content in multiple languages using a language model pipeline built with **LangChain** and **FastAPI**.

The system:

- Accepts a topic and optional target language
- Generates a blog title and content
- Routes the content for translation if a specific language is requested
- Supports **Arabic** and **French** translations

## Features

- **Dynamic content generation** based on user topic input
- **Multilingual support** with translation nodes
- **Conditional routing** to select translation path
- **REST API** endpoint to generate blogs
- **Graph-based workflow** for modularity and scalability

## Workflow Diagram

![Flow Diagram](blog_flow.png)

## API Endpoint

**POST** `/blogs`

### Request Body Examples

```json
{
  "topic": "Agentic AI"
}
```

```json
{
  "topic": "Agentic AI",
  "language": "Arabic"
}
```

### Response Example

```json
{
  "data": {
    "title": "Exploring Agentic AI",
    "content": "..."
  }
}
```

## How It Works

1. **Topic only** → Generate blog in default language
2. **Topic + Language** → Generate blog then translate
3. **Graph nodes**:
   - `title_creation` → Generates blog title
   - `content_generation` → Produces blog content
   - `route` → Decides translation path
   - `arabic_translation` / `french_translation` → Translates to target language

## Tech Stack

- **FastAPI** for API endpoints
- **LangChain** for LLM workflow
- **Graph-based pipeline** for modular execution
- **Groq LLM** as the language model backend
- **Python-dotenv** for environment management
