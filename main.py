import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function
import json

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= api_key,
    ) 
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )
    if response.usage == None:
        raise RuntimeError("No 'usage' property found")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    message = response.choices[0].message
    if message.tool_calls == None or len(message.tool_calls) == 0:
        print(response.choices[0].message.content)
    else:
        for tool_call in message.tool_calls: 
            function_args = json.loads(tool_call.function.arguments or "{}")
            # print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call)
            if args.verbose:
                print(f"-> {result_message['content']}")
                


if __name__ == "__main__":
    main()
