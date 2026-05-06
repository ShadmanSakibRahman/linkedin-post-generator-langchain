# LinkedIn Post Generator

This is my assignment for the AI Agents module. I built an AI agent using LangChain that takes a topic and a language from the user and generates a professional LinkedIn post.

The main idea of this project is the conditional routing part. Instead of one big writer that handles every kind of topic, I made two specialized writer agents and a small router agent that decides which one should handle the request. If the topic is something tech related, the request goes to the Tech Writer Agent. Otherwise it goes to the General Writer Agent.

## How the agent works

When you give it a topic and a language, the flow is basically this. First the router agent reads the topic and classifies it as either Tech or General. The router is just a small LLM call with a strict prompt that forces it to output only one word, either Tech or General. Then based on that classification, the request gets handed over to one of the two writer agents. The chosen writer takes the topic and the language and generates the actual LinkedIn post.

The routing logic is implemented using RunnableBranch from LangChain. RunnableBranch takes a list of conditions and runnables and picks the first one whose condition is true. I am using a small lambda function as the condition that checks if the router output starts with the word tech, and if it does it picks the tech writer chain. Otherwise it falls through to the general writer as the default.

I had to use startswith and lowercasing instead of a strict equality check because LLMs sometimes add a trailing period or change the capitalization even when you tell them not to, and that would break a strict equality check.

## What is in each file

LinkedIn_Post_Generator_ShadmanSakibRahman.ipynb is the main notebook. It has all the code, the router agent, both writer agents, the routing logic, and four demo cells at the bottom that show the agent working on different topics and languages.

README.md is this file.

build_notebook.py is the python script I used to generate the notebook programmatically. I wrote it because the notebook has a lot of cells and editing JSON by hand is annoying.

demo_video_script.md is just the script I followed when recording the demo video.

## How to run it

Open the ipynb file in Google Colab. The first code cell installs the required packages which are langchain, langchain-groq, and langchain-core. The second cell asks for a Groq API key. You can get a free one from console.groq.com slash keys. Paste the key into the input box and press enter. After that just run the rest of the cells in order or use Runtime then Run all.

The four demos at the bottom are. Demo 1 is AI in Healthcare in English which goes to the Tech Writer. Demo 2 is Work-Life Balance for Young Professionals in Bengali which goes to the General Writer. Demo 3 is The Rise of Edge Computing in Bengali which is a Tech topic but in a different language. Demo 4 is Leadership Lessons from Failure in English which goes to the General Writer.

Demos 1 and 2 are the two required demos from the assignment. The other two are extra to show that the routing and the language switching work independently of each other.

## What I learned

The harder part was not actually the writer agents. It was making the router output reliable enough to drive the branching. Even with a strict system prompt the LLM sometimes adds extra characters, so the conditional check needs to be a bit forgiving.

The other thing I had to think about was making the two writers actually feel different. If both writers have similar prompts the output sounds the same regardless of which one ran, which kind of defeats the whole point of having two specialized agents. So I gave the Tech Writer a credible and forward-looking voice and the General Writer a warmer and more human voice, and that made the outputs noticeably different in tone.

## Tools used

Python 3, LangChain, langchain-groq, Groq API with the llama-3.3-70b-versatile model, Google Colab.

## Author

Md. Shadman Sakib Rahman
