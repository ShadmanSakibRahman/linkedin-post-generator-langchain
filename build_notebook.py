"""
Generates the LinkedIn Post Generator notebook programmatically.
Uses LangChain with conditional routing between Tech and General writer agents.
"""

import nbformat as nbf
import json

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text):
    cells.append(nbf.v4.new_code_cell(text))


# =====================================================================
# Title and Introduction
# =====================================================================
md("""# AI-Powered LinkedIn Post Generator

This notebook builds an AI Agent using LangChain that generates professional LinkedIn posts based on a user-provided topic and language.

The agent has a router that decides whether the topic is tech-related or general, and then hands off the writing job to one of two specialized writer agents. The output is a clean LinkedIn post with the right tone, length, and a closing call-to-action.

**Author:** Md. Shadman Sakib Rahman

## What this notebook actually does

1. Takes a topic and a language from the user
2. A router agent classifies the topic as either `Tech` or `General`
3. Based on that classification, the request is routed to either a Tech Writer Agent or a General Writer Agent
4. The selected writer generates a 2-4 paragraph LinkedIn post in the requested language, ending with a question or call-to-action

## Why I built it this way

Honestly the routing piece was the part I spent the most time thinking about. I could have just used one big writer with a long system prompt that handles every kind of topic, but the assignment specifically asked for two specialist agents and a conditional handover, so I went with LangChain's `RunnableBranch` which is the cleanest way to do conditional routing in LCEL chains. The router is itself a small LLM call that returns a single label, and that label is used to pick the next chain.""")


# =====================================================================
# Setup
# =====================================================================
md("""## Step 1: Install the required packages

I am using LangChain with Groq because Groq has a free tier and the inference is fast (llama-3.3-70b-versatile is the model). You can swap in any other LangChain-compatible LLM if you prefer (OpenAI, Gemini, etc.) by changing the LLM setup cell below.""")

code("""!pip install -q langchain langchain-groq langchain-core""")


md("""## Step 2: Imports and API key

You will need a free Groq API key from https://console.groq.com/keys. Paste it in when the input prompt shows up.""")

code("""import os
import getpass
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough

# Get Groq API key (you can also hard-code it but getpass is safer)
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

print("API key set. Ready to go.")""")


# =====================================================================
# LLM Setup
# =====================================================================
md("""## Step 3: Initialize the LLM

I am using `llama-3.3-70b-versatile` because it is currently the most capable free model on Groq and it handles multiple languages well (including Bengali, which I need for the second demo). Temperature is set to 0.7 to get reasonably creative posts without going off the rails.""")

code("""llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=1024,
)

# Quick sanity check
test_response = llm.invoke("Say hello in one short sentence.")
print(test_response.content)""")


# =====================================================================
# Router Agent
# =====================================================================
md("""## Step 4: Router Agent

The router's only job is to classify a topic into one of two buckets: `Tech` or `General`. I am keeping the prompt deliberately simple and forcing it to return only one of those two words so I can use the output directly in the conditional routing.""")

code("""router_prompt = ChatPromptTemplate.from_messages([
    ("system", \"\"\"You are a topic classifier for a LinkedIn post generator.
Your only job is to look at a topic and decide whether it is technology-related or not.

Tech topics include: AI, software development, programming, data science, machine learning, cybersecurity, cloud computing, devops, blockchain, robotics, IT infrastructure, gadgets, semiconductors, and similar.

General topics include: leadership, productivity, career advice, marketing, sales, finance, healthcare (non-tech aspects), education, work-life balance, mental health, social issues, business strategy, and anything else that is not primarily about technology.

Respond with ONLY one word: either "Tech" or "General". No explanation, no punctuation, just the single word.\"\"\"),
    ("human", "Topic: {topic}")
])

router_chain = router_prompt | llm | StrOutputParser()

# Test the router
print("Test 1 (AI in Healthcare):", router_chain.invoke({"topic": "AI in Healthcare"}))
print("Test 2 (Work-Life Balance):", router_chain.invoke({"topic": "Work-Life Balance"}))
print("Test 3 (Cybersecurity Trends):", router_chain.invoke({"topic": "Cybersecurity Trends"}))
print("Test 4 (Leadership in Crisis):", router_chain.invoke({"topic": "Leadership in Crisis"}))""")


# =====================================================================
# Tech Writer Agent
# =====================================================================
md("""## Step 5: Tech Writer Agent

The Tech Writer specializes in technology topics. I told it to use a credible, slightly forward-looking tone and to avoid both hype and overly dry corporate language. It also has to follow the assignment's structural requirements (2-4 short paragraphs, ends with a question or call-to-action, written in the requested language).""")

code("""tech_writer_prompt = ChatPromptTemplate.from_messages([
    ("system", \"\"\"You are a professional Tech Writer who creates LinkedIn posts about technology.

Your style:
- Credible and forward-looking, but not hypey
- Concrete enough that a technical person finds it useful, accessible enough that a non-engineer still gets it
- No filler buzzwords like "synergy" or "leverage" unless they actually fit
- No emoji-heavy openings, no "🚀 Excited to share..." cliches

Structure requirements (these are strict):
- 2 to 4 short paragraphs
- Professional, engaging tone
- End with one thoughtful question or call-to-action that invites discussion
- Write the entire post in the language specified by the user
- Do not include any markdown formatting, hashtags at the start, or "Here is your post" preamble. Just output the post text directly.\"\"\"),
    ("human", "Write a LinkedIn post about: {topic}\\n\\nLanguage: {language}")
])

tech_writer_chain = tech_writer_prompt | llm | StrOutputParser()""")


# =====================================================================
# General Writer Agent
# =====================================================================
md("""## Step 6: General Writer Agent

The General Writer handles non-tech topics. The tone here leans more human and reflective compared to the Tech Writer, since topics like leadership, work-life balance, and personal growth do better with a warmer voice.""")

code("""general_writer_prompt = ChatPromptTemplate.from_messages([
    ("system", \"\"\"You are a professional content writer who creates LinkedIn posts on non-technical professional topics like leadership, career, productivity, business, and personal growth.

Your style:
- Warm and human, but still professional
- Insightful without being preachy
- Personal where it makes sense, but not over-sharing
- No emoji-heavy openings, no "Excited to announce..." cliches

Structure requirements (these are strict):
- 2 to 4 short paragraphs
- Professional, engaging tone
- End with one thoughtful question or call-to-action that invites discussion
- Write the entire post in the language specified by the user
- Do not include any markdown formatting, hashtags at the start, or "Here is your post" preamble. Just output the post text directly.\"\"\"),
    ("human", "Write a LinkedIn post about: {topic}\\n\\nLanguage: {language}")
])

general_writer_chain = general_writer_prompt | llm | StrOutputParser()""")


# =====================================================================
# Conditional Routing
# =====================================================================
md("""## Step 7: Conditional Routing with RunnableBranch

This is where the handover actually happens. I use LangChain's `RunnableBranch` which takes a list of `(condition, runnable)` pairs and a default. It evaluates conditions in order and runs the first one that matches.

The flow is:
1. Take input dict `{topic, language}`
2. Run the router chain to get the classification, store it as `category`
3. Pass everything to the branch, which picks Tech Writer if `category` starts with "Tech" and General Writer otherwise

I am using `.startswith` rather than equality because LLMs sometimes add a trailing period or whitespace even when told not to, and this makes the routing more robust.""")

code("""def classify_topic(inputs):
    \"\"\"Run the router and add the category to the inputs dict.\"\"\"
    category = router_chain.invoke({"topic": inputs["topic"]}).strip()
    return {**inputs, "category": category}


# RunnableBranch handles the conditional handover
writer_branch = RunnableBranch(
    (lambda x: x["category"].lower().startswith("tech"), tech_writer_chain),
    general_writer_chain,  # default
)

# Full pipeline: classify -> route -> generate
linkedin_agent = RunnableLambda(classify_topic) | RunnablePassthrough.assign(
    post=writer_branch
)

print("Agent pipeline built successfully.")""")


# =====================================================================
# Main Function
# =====================================================================
md("""## Step 8: Main function for clean output

Wrapping everything in a small function so the demo cells stay readable.""")

code("""def generate_linkedin_post(topic: str, language: str):
    \"\"\"Run the full agent pipeline and pretty-print the result.\"\"\"
    print("=" * 70)
    print(f"INPUT")
    print("=" * 70)
    print(f"Topic:    {topic}")
    print(f"Language: {language}")
    print()

    result = linkedin_agent.invoke({"topic": topic, "language": language})

    print("=" * 70)
    print(f"ROUTING DECISION")
    print("=" * 70)
    print(f"Classified as: {result['category']}")
    chosen_agent = "Tech Writer Agent" if result['category'].lower().startswith("tech") else "General Writer Agent"
    print(f"Routed to:     {chosen_agent}")
    print()

    print("=" * 70)
    print(f"GENERATED LINKEDIN POST")
    print("=" * 70)
    print(result["post"])
    print("=" * 70)

    return result""")


# =====================================================================
# Demo 1
# =====================================================================
md("""## Demo 1: Tech Topic in English

First example uses a clearly tech-related topic. The router should classify this as `Tech` and hand it to the Tech Writer Agent.""")

code("""result_1 = generate_linkedin_post(
    topic="AI in Healthcare",
    language="English"
)""")


# =====================================================================
# Demo 2
# =====================================================================
md("""## Demo 2: General Topic in Bengali

Second example uses a non-tech topic in Bengali. The router should classify this as `General` and hand it to the General Writer Agent, which will then produce the entire post in Bengali script.""")

code("""result_2 = generate_linkedin_post(
    topic="Work-Life Balance for Young Professionals",
    language="Bengali"
)""")


# =====================================================================
# Bonus extra demo
# =====================================================================
md("""## Bonus Demo: Tech Topic in Bengali

Just to prove the language switching works regardless of which writer is picked.""")

code("""result_3 = generate_linkedin_post(
    topic="The Rise of Edge Computing",
    language="Bengali"
)""")


md("""## Bonus Demo: General Topic in English""")

code("""result_4 = generate_linkedin_post(
    topic="Leadership Lessons from Failure",
    language="English"
)""")


# =====================================================================
# Reflection
# =====================================================================
md("""## Reflection

Building this was a good way to actually understand how conditional routing works in LangChain instead of just reading about it. The hardest part was not the agents themselves but getting the router output to be reliable enough to drive the branching. Even with explicit "respond with ONLY one word" instructions, LLMs sometimes sneak in extra punctuation or capitalize differently, so I ended up using `.lower().startswith("tech")` instead of strict equality which made the routing much more robust.

The other thing I learned is that the two writers need clearly different system prompts, otherwise the output ends up sounding the same regardless of which agent ran. Pushing the Tech Writer toward "credible and forward-looking" and the General Writer toward "warm and human" gave the posts noticeably different voices, which is the whole point of having two agents instead of one. The Bengali generation worked surprisingly well with the 70B llama model - the output was natural enough that I did not need to do any post-processing.""")


# =====================================================================
# Save
# =====================================================================
nb["cells"] = cells

# Set kernel info
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "name": "python",
        "version": "3.10",
    },
    "colab": {"provenance": []},
}

output_path = "LinkedIn_Post_Generator_ShadmanSakibRahman.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook written to {output_path}")
print(f"Total cells: {len(cells)}")
print(f"  Markdown: {sum(1 for c in cells if c['cell_type'] == 'markdown')}")
print(f"  Code:     {sum(1 for c in cells if c['cell_type'] == 'code')}")
