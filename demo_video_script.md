# Demo Video Script (2-3 minutes)

Use this as a guide when recording the demo video. Aim for around 2:30.

## Setup before recording

1. Open the notebook in Colab
2. Have your Groq API key ready
3. Make sure the runtime is connected
4. Optionally clear all outputs first so the viewer sees them populate live

---

## Script

### Intro (15-20 seconds)

> "Hi, this is the demo for my AI-Powered LinkedIn Post Generator assignment. I built this using LangChain, and it generates professional LinkedIn posts based on a topic and a language that the user provides. The interesting part is that it uses a conditional routing agent to decide which of two specialized writer agents should generate the post."

### Show the architecture (20-25 seconds)

> "The flow is simple. The user gives a topic and a language. A router agent first classifies the topic as either Tech or General. Based on that classification, the request is routed to either a Tech Writer Agent or a General Writer Agent. The chosen writer then produces the final LinkedIn post. I implemented the conditional handover using LangChain's RunnableBranch."

*(While saying this, scroll through the notebook from top to bottom to show the structure)*

### Run the setup cells (15 seconds)

> "Let me run the setup cells first. Installing LangChain and Groq, then I'll paste my API key."

*(Run cells 1, 2, 3 - install, API key, LLM init)*

### Show the router (20 seconds)

> "Here's the router agent. It only outputs one word: Tech or General. Watch what it does with four different test topics."

*(Run the router test cell)*

> "AI in Healthcare gets classified as Tech, Work-Life Balance as General, Cybersecurity Trends as Tech, Leadership in Crisis as General. So the classification is working."

### Demo 1 - Tech in English (25-30 seconds)

> "Demo one. Topic: AI in Healthcare. Language: English. The router should send this to the Tech Writer."

*(Run Demo 1 cell)*

> "Classified as Tech, routed to the Tech Writer Agent. And here's the post - two paragraphs, professional tone, ends with a question."

### Demo 2 - General in Bengali (25-30 seconds)

> "Demo two. Topic: Work-Life Balance for Young Professionals. Language: Bengali. This should go to the General Writer."

*(Run Demo 2 cell)*

> "Classified as General, routed to the General Writer Agent. The post is in Bengali script, three paragraphs, ends with a call-to-action. The conditional routing and the language switching are both working."

### Wrap up (15 seconds)

> "I also included two bonus demos in the notebook - a Tech topic in Bengali and a General topic in English - to show that the routing and language are independent. The README has the full architecture diagram and a summary of how everything fits together. Thanks for watching."

---

## Tips for recording

- Use OBS Studio or the built-in screen recorder (Windows: Win+G for Game Bar, Mac: Cmd+Shift+5)
- Keep your face cam off if you prefer - just narrate over the screen
- If you mess up a line, just keep going - small mistakes are fine, only re-record if a cell errors out
- Make sure the cell outputs are clearly visible (zoom in on Colab if needed)
- Total target: 2:00 to 3:00. Anything in that window is fine.

## What to upload

Save the video as `demo.mp4` and upload it alongside the notebook (Google Drive, YouTube unlisted, or wherever the assignment asks).
