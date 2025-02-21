from openai import OpenAI
import json

client = OpenAI()

# Define function for structured output
def extract_data(gratitude_note: str):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Based on the gratitude note provided, infer the groups or individuals who should be thanked, even if not explicitly stated. Provide detailed descriptions of their contributions and do not use words likely or possibly, etc."},
            {"role": "user", "content": f"Extract and infer the groups or individuals who contributed to this experience and should be thanked. Provide a detailed explanation of their contributions from this gratitude note:\n\n{gratitude_note}"}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "extract_data",
                    "description": "Extracts recipient groups and their contributions from a gratitude note. Provide detailed descriptions of their contributions in a structured JSON format and do not use words likely or possibly, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient_groups": {
                                "type": "array",
                                "description": "A list of groups and their contributions",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "group": {"type": "string", "description": "The group being thanked"},
                                        "description": {"type": "string", "description": "A detailed explanation of their contribution"}
                                    }
                                }
                            }
                        },
                        "required": ["recipient_groups"]
                    }
                }
            }
        ],
        tool_choice="auto"
    )

    return response.choices[0].message.tool_calls[0].function.arguments if response.choices[0].message.tool_calls else None

# Example gratitude note
gratitude_note = """
I really like building projects made with arduino microcontrollers. It’s really cool to wire up and program everything and 
it’s just so cool! I remember making my first arcade game with Arduino in high school engineering class and now I continue 
to do cool stuff with them!
"""
# Run extraction
output = extract_data(gratitude_note)
print(json.loads(output))
