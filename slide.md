# Presenting: Building an AI Agent Step by Step

This updated plan consolidates the state-of-the-art architectural research into a single "Contrast" slide (Slide 9), reserving Slide 10 for an inspiring, high-level takeaway that ties the whole presentation together.

## User Review Required

Does this balance of Slide 9 (The Contrast) and Slide 10 (The Ultimate Takeaway) finalize the plan to your liking? If so, please approve and we will begin!

## Proposed Changes

We will build the presentation in `/Users/zichaoyang/Documents/agt/agent-presentation/index.html`. It will use Reveal.js via CDN.

### Presentation Outline (Slide by Slide)

1. **Slide 1: Building an AI Agent Step by Step**
   - *Concepts*: Educating people on how to construct an agent from scratch. Every step adds one core piece.

2. **Slide 2: What is an Agent?**
   - *Concepts*: Unlike simple completions, an agent is an LLM given tools, memory, and autonomy to take actions.

3. **Slide 3: Step 01 - Hello LLM**
   - *Code*:
     ```python
     def run_agent(prompt):
         return llm.generate(prompt)
     ```

4. **Slide 4: Step 02 - Chat Loop**
   - *Code*:
     ```python
     messages = []
     while True:
         user_input = input("You: ")
         messages.append(user_input)
         
         response = llm.generate(messages)
         messages.append(response)
         print("Agent:", response.text)
     ```

5. **Slide 5: Step 03 - Tool Use (The Hands)**
   - *Code*:
     ```python
     # We give the LLM tools to use
     response = llm.generate(messages, tools=[search_web])

     if response.tool_calls:
         result = execute(response.tool_calls)
         print("Tool Result:", result)
     else:
         print("Agent:", response.text)
     ```

6. **Slide 6: Step 04 - Agent Loop (Autonomy)**
   - *Code*:
     ```python
     while True: # Outer Loop: Conversation with Human
         user_input = input("You: ")
         messages.append(user_input)
         
         while True: # Inner Loop: Agent autonomy
             response = llm.generate(messages, tools=[search_web])
             messages.append(response)
             
             if response.tool_calls:
                 result = execute(response.tool_calls)
                 messages.append(result)
                 continue # Loop back so LLM sees result
                 
             print("Agent:", response.text)
             break # Agent is done, go back to outer loop
     ```

7. **Slide 7: Step 05 & 06 - Planning & Memory**
   - *Code*:
     ```python
     state = {"todos": [], "memory": ""}

     while True: # Inner Agent Loop
         context = messages + [f"State: {state}"]
         response = llm.generate(context, tools=[add_todo])
         
         if response.tool_calls:
             result = execute(response.tool_calls)
             state = update_state(state, result)
             continue
     ```

8. **Slide 8: Step 07 & 08 - Subagents & Teams**
   - *Code*:
     ```python
     def manager_agent(task):
         intent = classify_intent(task)
         
         if intent == "coding":
             return coder_agent(task)
         elif intent == "research":
             return search_agent(task)
     ```

9. **Slide 9: The Contrast (State-of-the-Art Architecture)**
    - *Concepts*: Contrasting our python loops against advanced, industrial implementations.
    - *Features*:
      - **Claude Code**: Uses *Auto Dream* background memory defragmentation and multi-agent *Orchestrator-Critic* pipelines.
      - **OpenHands**: Employs an *Event-Stream Architecture* inside a secure *Docker Sandbox* to execute tools safely.
      - **OpenClaw**: Utilizes a *Local-First Heartbeat Scheduler* for continuous, persistent background autonomy rather than blocking on a script.

10. **Slide 10: The Ultimate Takeaway**
    - *Concepts*: Demystifying the AI landscape bridging the gap between our code and the state-of-the-art.
    - *Key Message*: 
      - "Don't be intimidated by the jargon."
      - "No matter how advanced an AI agent is, at its absolute core it is just an **LLM embedded in a while-loop, calling functions.**" 
      - Once you build it yourself, the magic is gone, and the actual engineering begins.

## Verification Plan
### Manual Verification
- Output `index.html` file into the new directory. Ensure the layout logically concludes from the Step 08 code directly into the Contrast on Slide 9, culminating in the philosophical Takeaway on Slide 10.

