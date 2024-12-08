import anthropic

client = anthropic.Anthropic()

def calculator(operation, operand1, operand2):
    if operation == "add":
        return operand1 + operand2
    elif operation == "subtract":
        return operand1 - operand2
    elif operation == "multiply":
        return operand1 * operand2
    elif operation == "divide":
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2
    else:
        raise ValueError(f"Unsupported operation: {operation}")

calculator_tool = {
    "name": "calculator",
    "description": "A simple calculator that performs basic arithmetic operations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The arithmetic operation to perform."
            },
            "operand1": {
                "type": "number",
                "description": "The first operand."
            },
            "operand2": {
                "type": "number",
                "description": "The second operand."
            }
        },
        "required": ["operation", "operand1", "operand2"]
    }
}

# A relatively simple math problem
response = client.messages.create(
    model="claude-3-haiku-20240307",
    messages=[{"role": "user", "content":"Multiply 1984135 by 9343116. Only respond with the result"}],
    max_tokens=400,
    tools=[calculator_tool]
)

print(response)
print()
print(response.content)

tool_name = response.content[0].name
tool_inputs = response.content[0].input

print("The Tool Name Claude Wants To Call:", tool_name)
print("The Inputs Claude Wants To Call It With:", tool_inputs)

operation = tool_inputs["operation"]
operand1 = tool_inputs["operand1"]
operand2 = tool_inputs["operand2"]

result = calculator(operation, operand1, operand2)
print("RESULT IS", result)

