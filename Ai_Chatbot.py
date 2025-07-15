# Imports
import os
import ollama
import gradio as gr

# Initialize
MODEL = 'llama3.2'

system_message = "You are a helpful assistant"

# Simple chat function
def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    print("History is:")
    print(history)
    print("And messages is:")
    print(messages)

    stream = ollama.chat(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        part = getattr(chunk, 'message', chunk)
        content = getattr(part, 'content', '')  # safely get the text part
        response += content
    yield response

gr.ChatInterface(fn=chat, type="messages").launch()


# Updated system message with store-specific instructions
system_message = (
    "You are a helpful assistant in a clothes store. You should try to gently encourage "
    "the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. "
    "For example, if the customer says 'I'm looking to buy a hat', "
    "you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.' "
    "Encourage the customer to buy hats if they are unsure what to get."
)

# Updated chat function with store system message
def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    stream = ollama.chat(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        part = getattr(chunk, 'message', chunk)
        content = getattr(part, 'content', '')  # safely get the text part
        response += content
        yield response

gr.ChatInterface(fn=chat, type="messages").launch()


# Further updated system message to handle shoes specifically
system_message += (
    "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, "
    "but remind the customer to look at hats!"
)

gr.ChatInterface(fn=chat, type="messages").launch()


# Final chat function with conditional message adjustment (belts case)
# Fixed a bug brilliantly identified by student Gabor M.
def chat(message, history):
    relevant_system_message = system_message
    if 'belt' in message:
        relevant_system_message += (
            " The store does not sell belts; if you are asked for belts, be sure to point out other items on sale."
        )

    messages = [{"role": "system", "content": relevant_system_message}] + history + [{"role": "user", "content": message}]

    stream = ollama.chat(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        part = getattr(chunk, 'message', chunk)
        content = getattr(part, 'content', '')  # safely get the text part
        response += content
        yield response

# Launch final chat interface
gr.ChatInterface(fn=chat, type="messages").launch()
