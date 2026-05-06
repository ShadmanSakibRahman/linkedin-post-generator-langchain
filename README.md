# AI-Powered LinkedIn Post Generator

This is a Google Colab notebook where I built an AI Agent using LangChain that generates professional LinkedIn posts based on a user-provided topic and language. The agent uses conditional routing to decide whether to send the writing job to a Tech Writer Agent or a General Writer Agent.

## What this notebook actually does

You give the agent a **topic** (like "AI in Healthcare" or "Work-Life Balance") and a **language** (like English, Bengali, Spanish), and it:

1. Classifies the topic as either **Tech** or **General**
2. Routes the request to the appropriate writer agent
3. Generates a professional LinkedIn post that is 2-4 paragraphs long, written in the requested language, and ends with a thoughtful question or call-to-action

## Agent workflow and routing logic

```
            ┌─────────────────────┐
            │  User Input         │
            │  (topic, language)  │
            └──────────┬──────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │   Router Agent      │
            │  (classifies topic) │
            └──────────┬──────────┘
                       │
              ┌────────┴────────┐
              │                 │
        category =           category =
         "Tech"              "General"
              │                 │
              ▼                 ▼
       ┌────────────┐    ┌────────────┐
       │Tech Writer │    │  General   │
       │   Agent    │    │   Writer   │
       └─────┬──────┘    └─────┬──────┘
             │                 │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │  LinkedIn Post  │
             │  (final output) │
             └─────────────────┘
```

The conditional handover is implemented using LangChain's `RunnableBranch`. The router is a small LLM call that returns a single label ("Tech" or "General"), and that label is used to pick the next chain in the pipeline.

## Steps in the notebook

1. **Setup** - installs `langchain`, `langchain-groq`, `langchain-core`
2. **API Key** - prompts for a free Groq API key (from [console.groq.com](https://console.groq.com/keys))
3. **LLM Setup** - initializes `llama-3.3-70b-versatile` via Groq with temperature 0.7
4. **Router Agent** - classifies any topic into "Tech" or "General" with a one-word output
5. **Tech Writer Agent** - generates posts with a credible, forward-looking tone
6. **General Writer Agent** - generates posts with a warm, human, professional tone
7. **Conditional Routing** - uses `RunnableBranch` to hand off based on the router's classification
8. **Main pipeline** - puts everything together in one chain
9. **Demos** - runs four examples covering all combinations of Tech/General and English/Bengali
10. **Reflection** - what I learned

## How to run

1. Open `LinkedIn_Post_Generator_ShadmanSakibRahman.ipynb` in [Google Colab](https://colab.research.google.com/)
2. Run the first cell to install dependencies
3. When the API key prompt shows up, paste your free Groq API key
4. Run the rest of the cells in order
5. The four demos will print at the bottom showing the routing decision and the final post

## Demos included

| # | Topic | Language | Expected Routing |
|---|-------|----------|------------------|
| 1 | AI in Healthcare | English | Tech Writer |
| 2 | Work-Life Balance for Young Professionals | Bengali | General Writer |
| 3 | The Rise of Edge Computing | Bengali | Tech Writer |
| 4 | Leadership Lessons from Failure | English | General Writer |

Demos 1 and 2 cover the assignment's required examples (Tech in English, General in Bengali). The other two are bonus to show that the routing and language selection are independent.

## Why I made certain choices

- **Groq + llama-3.3-70b** - free tier, fast inference, and the 70B model handles Bengali well enough that I did not need a separate translation step
- **`.lower().startswith("tech")` for routing** - LLMs sometimes add trailing punctuation or change capitalization even when told not to, so this is more robust than strict equality
- **Two separate writer prompts with distinct voices** - "credible and forward-looking" for Tech vs "warm and human" for General, otherwise the posts end up sounding the same regardless of which agent ran

## Tools used

- Python 3
- LangChain (LCEL chains, RunnableBranch, RunnablePassthrough, RunnableLambda)
- Groq API (`llama-3.3-70b-versatile`)
- Google Colab

## Author

Md. Shadman Sakib Rahman
