import logging
from llm.ollama_client import OllamaClient
from rag.retriever import Retriever

logger = logging.getLogger(__name__)

class DebateEngine:
    def __init__(self, llm_client: OllamaClient, retriever: Retriever):
        self.llm = llm_client
        self.retriever = retriever

    def run_debate(self, question, agents, rounds=1):
        """
        Run a debate among agents. Yields responses as they come in.
        """
        debate_history = []
        
        # Round 1: Initial responses
        logger.info("Starting Round 1: Initial Responses")
        
        for agent in agents:
            logger.info(f"Agent {agent.name} is thinking...")
            
            # Retrieve context
            context = self.retriever.get_context(agent.domain_collection, question)
            
            # Construct prompt
            prompt = f"""
            User Question: {question}
            
            Context from your domain ({agent.domain_collection}):
            {context}
            
            Please provide your analysis and recommendations based on your role.
            """
            
            response = self.llm.generate(prompt, system_prompt=agent.system_prompt)
            response_text = response.get("response", "")
            
            entry = {
                "round": 1,
                "agent": agent.name,
                "response": response_text
            }
            debate_history.append(entry)
            yield entry
            
        if rounds > 1:
            # Round 2: Critique / Refinement (Optional)
            pass

