import os
import json
from agents.base_agent import BankAgent
from memory.agent_memory import RegulatoryMemory
from tools.audit_logger import AuditLogger

class RegulatorySystem:
    def __init__(self):
        # 1. Initialize Infrastructure
        self.memory = RegulatoryMemory()
        self.audit = AuditLogger()

        # 2. Initialize the Team (The Agents)
        self.interpreter = BankAgent("Legal_Interpreter", "perceive.txt")
        self.analyst = BankAgent("Impact_Analyst", "plan.txt")
        self.executor = BankAgent("Reporting_Specialist", "act.txt")

    def run(self, raw_regulatory_text):
        print("=== Starting Regulatory Change Workflow ===")

        # STAGE 1: PERCEIVE
        # -----------------------------------------------
        interpretation, p_prompt = self.interpreter.execute_task(raw_regulatory_text)
        self.audit.log_entry("PERCEIVE", p_prompt, interpretation)
        print(f"Interpretation Complete: {interpretation}")

        # STAGE 2: PLAN
        # -----------------------------------------------
        roadmap, pl_prompt = self.analyst.execute_task(interpretation)
        self.audit.log_entry("PLAN", pl_prompt, roadmap)
        print(f"Roadmap Created: {roadmap}")

        # STAGE 3: ACT
        # -----------------------------------------------
        final_action, a_prompt = self.executor.execute_task(roadmap)
        self.audit.log_entry("ACT", a_prompt, final_action)
        print(f"Action Executed: {final_action}")

        # STAGE 4: MEMORY UPDATE
        # -----------------------------------------------
        self.memory.add_memory(
            doc_id=f"REG-{os.urandom(2).hex()}",
            text=raw_regulatory_text,
            metadata={"status": "Processed", "agent_chain": "Full"}
        )

        print("\n=== Workflow Successfully Completed ===")
        print("Audit trail and memory have been updated for compliance.")

if __name__ == "__main__":
    # Ensure folders exist
    for folder in ["prompts", "tools", "memory", "agents"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Initialize and Run
    sys = RegulatorySystem()
    sample_regulation = "New RBI Guideline: Increase CRR by 50 basis points."
    sys.run(sample_regulation)
