
import ollama
from pathlib import Path

# Configuration

MODEL = "qwen3.5:0.8b"

SKILLS_DIRECTORY = Path("skills")


def load_skills():
    """
    Load all available skills from Markdown files.
    """

    skills = {}

    for file in SKILLS_DIRECTORY.glob("*.md"):

        skill_name = file.stem

        skill_content = file.read_text(encoding="utf-8")

        skills[skill_name] = skill_content

    return skills


def select_skill(user_input, available_skills):
    """
    Ask the LLM to select the appropriate skill.
    """

    skill_names = list(available_skills.keys())

    prompt = f"""
You are a skill selection assistant.

Available skills:
{skill_names}

User request:
{user_input}

Select the most appropriate skill.

Return ONLY its name from the available skills.
If none is appropriate, return general.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False
    )

    selected_skill = response.message.content.strip().lower()

    # Validate selection

    if selected_skill not in available_skills:
        return "general"

    return selected_skill


def execute_skill(user_input, skill_name, available_skills):
    """
    Execute the selected skill using its instructions.
    """

    if skill_name == "general":

        skill_instructions = (
            "You are a helpful general-purpose assistant.Answer simply and do not invent facts."
        )

    else:

        skill_instructions = available_skills[skill_name]

    messages = [
        {
            "role": "system",
            "content": skill_instructions
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        think=False
    )

    return response.message.content


def main():

    print("Local Qwen Skills Agent")
    print("=======================")

    # Load available skills

    available_skills = load_skills()

    print("\nAvailable skills:")

    for skill in available_skills:
        print(f"- {skill}")

    print("\nType 'exit' to quit.")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input:
            continue

        # Step 1: Select a skill

        skill_name = select_skill(
            user_input,
            available_skills
        )

        print(f"\n[Selected skill: {skill_name}]")

        # Step 2: Execute the selected skill

        answer = execute_skill(
            user_input,
            skill_name,
            available_skills
        )

        print("\nAssistant:")
        print(answer)


if __name__ == "__main__":
    main()
