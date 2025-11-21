import logging
import argparse
from llm.ollama_client import OllamaClient
from rag.retriever import Retriever
from orchestrator.agents_loader import load_agents
from orchestrator.debate_engine import DebateEngine
from orchestrator.consensus_engine import ConsensusEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Council of Civilizations")
    parser.add_argument("--question", type=str, help="The question to ask the council")
    args = parser.parse_args()
    
    question = args.question
    if not question:
        question = input("Enter your question for the Council: ")
        
    # Initialize components
    llm_client = OllamaClient()
    retriever = Retriever()
    
    # Load Agents
    agents = load_agents()
    if not agents:
        logger.error("No agents found. Please check the agents/ directory.")
        return

    # Run Debate
    debate_engine = DebateEngine(llm_client, retriever)
    debate_history = []
    
    print("\n=== Council Debate ===\n")
    for entry in debate_engine.run_debate(question, agents):
        print(f"\n--- {entry['agent']} ---")
        print(entry['response'])
        debate_history.append(entry)
    
    # Generate Consensus
    consensus_engine = ConsensusEngine(llm_client)
    final_plan = consensus_engine.generate_consensus(question, debate_history)
    
    print("\n\n=== Council Consensus Plan ===\n")
    print(final_plan)

if __name__ == "__main__":
    main()
