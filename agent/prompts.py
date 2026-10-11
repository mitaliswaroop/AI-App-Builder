def planner_prompt(user_prompt: str) -> str:
    PLANNER_PROMPT = f"""
You are the PLANNER agent. Convert the user prompt into a COMPLETE engineering project plan.

User request:
{user_prompt}
    """
    return PLANNER_PROMPT



def architect_prompt(plan: str) -> str:
    ARCHITECT_PROMPT = f"""
You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.

RULES:
- For each FILE in the plan, create one or more IMPLEMENTATION TASKS.
- In each task description:
    * Specify exactly what to implement.
    * Name the variables, functions, classes, and components to be defined.
    * Mention how this task depends on or will be used by previous tasks.
    * Include integration details: imports, expected function signatures, data flow.
- Order tasks so that dependencies are implemented first.
- Each step must be SELF-CONTAINED but also carry FORWARD the relevant context from earlier tasks.

CRITICAL INSTRUCTION: You MUST output your entire response as a valid JSON object. 
The JSON object MUST have a single root key named "implementation_steps" which contains the array of task objects.
Each task object in the array MUST have EXACTLY two keys: "filepath" (the file to create/edit) and "task_description" (the instructions).
DO NOT output any conversational text, markdown, or preamble before or after the JSON.

Project Plan:
{plan}
    """
    return ARCHITECT_PROMPT



def coder_system_prompt() -> str:
    CODER_SYSTEM_PROMPT = """
You are the CODER agent.
You are implementing a specific engineering task.
You have access to tools to read and write files.
CRITICAL: To list files in a directory, you MUST use the tool named `list_files`. DO NOT use `list_file`.

Always:
- Review all existing files to maintain compatibility.
- Implement the FULL file content, integrating with other modules.
- Maintain consistent naming of variables, functions, and imports.
- When a module is imported from another file, ensure it exists and is implemented as described.
    """
    return CODER_SYSTEM_PROMPT