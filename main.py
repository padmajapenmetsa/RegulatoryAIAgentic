import os
import json
from memory.agent_memory import RegulatoryMemory
from tools.audit_logger import AuditLogger

class RegulatoryAgent:
    def __init__(self):
        self.memory = RegulatoryMemory()
        self.audit = AuditLogger()
        self.prompts_dir = "prompts"

    def _load_prompt(self, filename, **kwargs):
        """Reads a prompt file and injects variables."""
        path = os.path.join(self.prompts_dir, f"{filename}.txt")
        try:
            with open(path, "r") as f:
                template = f.read()
            # Replace {{variable}} with actual data
            for key, value in kwargs.items():
                template = template.replace(f"{{{{{key}}}}}", str(value))
            return template
        except FileNotFoundError:
            return f"Error: Prompt file {filename}.txt not found."

    def perceive(self, raw_text):
        print("--- [STAGE 1: PERCEIVE] ---")
        # Load the specific Perceive prompt logic
        prompt = self._load_prompt("perceive", raw_document_text=raw_text)
        
        # Simulated LLM Response (In reality, you'd pass 'prompt' to Llama 3)
        perceived_data = {
            "issuing_body": "Basel Committee",
            "deadline": "2026-12-31",
            "impacted_reports": ["LCR_Liquidity_Report"],
            "urgency_score": "9"
        }
        self.audit.log_entry("PERCEIVE", prompt, json.dumps(perceived_data))
        return perceived_data

    def plan(self, context):
        print("--- [STAGE 2: PLAN] ---")
        prompt = self._load_prompt("plan", perceived_context=json.dumps(context))
        
        # Simulated logic mapping context to steps
        steps = ["Update SQL logic for LCR", "Draft SME Summary", "Human Sign-off"]
        self.audit.log_entry("PLAN", prompt, str(steps))
        return steps

    def act(self, steps):
        print("--- [STAGE 3: ACT] ---")
        for step in steps:
            prompt = self._load_prompt("act", current_step=step, tools_list="SQL_Generator, Jira")
            
            if "Human Sign-off" in step:
                print(f"Action: {step} -> Awaiting SME input...")
            else:
                print(f"Action: {step} -> Executed using Act Prompt Logic")
            
            self.audit.log_entry("ACT", prompt, f"Executed: {step}")

    def run(self, raw_circular):
        # 1. Perception
        context = self.perceive(raw_circular)
        # 2. Planning
        steps = self.plan(context)
        # 3. Action
        self.act(steps)
        print("\nWorkflow complete. Audit logs and Memory updated.")

if __name__ == "__main__":
    agent = RegulatoryAgent()
    input_text = "Circular 405: Banks must increase HQLA by 5% effective Dec 2026."
    agent.run(input_text)
