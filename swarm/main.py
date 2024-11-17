import subprocess
import uuid
from pathlib import Path

from openai import AzureOpenAI

from swarm import Agent, Swarm

client = Swarm(client=AzureOpenAI(azure_deployment="gpt-4o-mini"))


# def transfer_to_agent_b():
#     return agent_b


# agent_a = Agent(
#     name="Agent A",
#     instructions="You are a helpful agent.",
#     functions=[transfer_to_agent_b],
# )

# agent_b = Agent(
#     name="Agent B",
#     instructions="Only speak in Haikus.",
# )

# response = client.run(
#     agent=agent_a,
#     messages=[{"role": "user", "content": "I want to talk to agent B."}],
# )


def transfer_to_code_executor():
    return code_executor


code_writer = Agent(
    name="Code Writer",
    instructions="You are a code writer.",
    functions=[transfer_to_code_executor],
)

work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)


def execute_code(context_variables, code):
    file = f"{work_dir}/{uuid.uuid4()}.py"

    with open(file, "w") as f:
        f.write(code)

    output = subprocess.run(
        ["python", file],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return output.stdout


code_executor = Agent(
    name="Code Executor",
    instructions="You are a code executor.",
    functions=[execute_code],
)

response = client.run(
    agent=code_writer,
    messages=[
        {
            "role": "user",
            "content": "Write a Python program that greets the user John and then print the result",
        }
    ],
    context_variables={"user_name": "John"},
    debug=True,
)

code_executor


print(response.messages[-1]["content"])
