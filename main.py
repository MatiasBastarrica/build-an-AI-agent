import sys
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

    final_response = ""
    
    for _ in range(20):
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
        messages.append(message)
        if message.tool_calls == None or len(message.tool_calls) == 0:
            final_response = response.choices[0].message.content
            break
        else:
            for tool_call in message.tool_calls: 
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        if _ == 19:
            print(f"Error: Unable to answer in less than {_} tries")
            sys.exit(1)

    print(f"Final result:\n{final_response}")
    

                   


if __name__ == "__main__":
    main()
