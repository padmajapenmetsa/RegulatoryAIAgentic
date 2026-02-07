import os

class BankAgent:
    def __init__(self, role, prompt_file):
        self.role = role
        self.prompt_file = prompt_file
        self.prompts_dir = "prompts"

    def _load_prompt(self, **kwargs):
        """Reads the prompt file and injects data into {{variables}}."""
        path = os.path.join(self.prompts_dir, self.prompt_file)
        if not os.path.exists(path):
            return f"Error: {self.prompt_file} not found."
            
        with open(path, "r") as f:
            template = f.read()
        
        for key, value in kwargs.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def execute_task(self, input_data):
        # 1. Prepare the prompt
        final_prompt = self._load_prompt(raw_document_text=input_data, 
                                        perceived_context=input_data, 
                                        current_step=input_data)
        
        print(f"\n>>> {self.role} is thinking...")
        
        # 2. Simulated LLM call (Replace this with your LLM API call)
        # In a real setup: response = llm.invoke(final_prompt)
        response = f"Result from {self.role} based on {self.prompt_file}"
        
        return response, final_prompt
