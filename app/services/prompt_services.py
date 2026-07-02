# ALL TEMPLATE PROMPTS NOT TESTED - NEED FINE-TUNING
TEMPLATES = {
    "explain_like_im_5": {
        "id": "explain_like_im_5",
        "name": "Explain Like I'm 5",
        "description": "Explains anything in easy-to-understand terms.",
        "system_prompt": "You are adept at breaking information down into understandable terms and concepts.",
        "template": "Explain {topic} to me as if I am 5 years old. Use simple words and analogies where appropriate.",
        "variables": ["topic"]
    },
    "pirate_coder": {
        "id": "pirate_coder",
        "name": "Pirate Coder",
        "description": "Explains code snippets in the voice of a pirate.",
        "system_prompt": "You are a savvy pirate kids coding instructor ages 10+. Explain the user's code in a pirate's voice.",
        "template": "Ahoy! Look at this code: \n\n{code}\n\nExplain what this does in the voice of a pirate.",
        "variables": ["code"]
    },
    "game_designer": {
        "id": "game_designer",
        "name": "Game Mechanic Brainstormer",
        "description": "Generates ideas for video game mechanics.",
        "system_prompt": "You are an exceptional game designer who loves to brainstorm. Come up with ideas based on a theme and mechanic type from the user.",
        "template": "I am making a game about {theme}. Give me 3 ideas for a unique {mechanic_type} mechanic.",
        "variables": ["theme", "mechanic_type"]
    }
}

def get_all_templates() -> list:
    return list(TEMPLATES.values())

def build_prompt(template_id: str, inputs: dict) -> str:
    if template_id not in TEMPLATES:
        raise ValueError(f"'{template_id}' not found.")
    
    template_data = TEMPLATES[template_id]
    built_user = template_data["template"]
    built_system = template_data["system_prompt"]
    
    missing = [var for var in template_data["variables"] if var not in inputs]
    if missing:
        raise ValueError(f"Missing required variables: {missing}")
    
    for var_name, var_value in inputs.items():
        placeholder = "{" + var_name + "}"
        built_user = built_user.replace(placeholder, var_value)
        built_system = built_system.replace(placeholder, var_value)
    
    return {
        "system_prompt": built_system,
        "template": built_user
    }