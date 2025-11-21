import logging
from llm.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

class ConsensusEngine:
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client

    def generate_consensus(self, question, debate_history):
        """
        Generate a consensus plan based on the debate history.
        """
        logger.info("Generating Consensus Plan...")
        
        # Aggregate all responses
        aggregated_responses = ""
        for entry in debate_history:
            aggregated_responses += f"--- Agent: {entry['agent']} ---\n{entry['response']}\n\n"
            
        # Moderator System Prompt
        system_prompt = """
        You are the Moderator of the Council of Civilizations.
        Your goal is to synthesize the advice of various experts into a cohesive, actionable plan.
        
        Structure your response as follows:
        1. Executive Summary
        2. Key Recommendations (Short-term, Mid-term, Long-term)
        3. Potential Risks and Mitigations
        4. Conclusion
        
        Resolve conflicts between agents by finding balanced trade-offs.
        """
        
        prompt = f"""
        User Question: {question}
        
        Expert Opinions:
        {aggregated_responses}
        
        Please create the final Council Report.
        """
        
        response = self.llm.generate(prompt, system_prompt=system_prompt)
        return response.get("response", "")
