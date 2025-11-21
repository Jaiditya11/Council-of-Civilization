import streamlit as st
import sys
import os

# Add project root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.ollama_client import OllamaClient
from rag.retriever import Retriever
from orchestrator.agents_loader import load_agents
from orchestrator.debate_engine import DebateEngine
from orchestrator.consensus_engine import ConsensusEngine

st.set_page_config(page_title="Council of Civilizations", layout="wide")

st.title("🏛️ Council of Civilizations")
st.markdown("### Multi-Agent AI Parliament for Future Planning")

# Sidebar for configuration
st.sidebar.header("Configuration")
model_name = st.sidebar.text_input("Ollama Model", value="mistral")

# Initialize components
@st.cache_resource
def get_components(model):
    llm_client = OllamaClient(model=model)
    retriever = Retriever()
    agents = load_agents()
    return llm_client, retriever, agents

llm_client, retriever, agents = get_components(model_name)

# Agent Selection
st.sidebar.subheader("Select Council Members")
selected_agent_names = st.sidebar.multiselect(
    "Choose agents to include in the debate:",
    [agent.name for agent in agents],
    default=[agent.name for agent in agents]
)

selected_agents = [a for a in agents if a.name in selected_agent_names]

# Main Input
question = st.text_area("Enter your question for the Council:", height=100, placeholder="e.g., How can we reduce road accidents in India by 50% in 5 years?")

if st.button("Convene Council"):
    if not question:
        st.warning("Please enter a question.")
    elif not selected_agents:
        st.warning("Please select at least one agent.")
    else:
        # Run Debate
        st.subheader("🗣️ Council Debate")
        debate_engine = DebateEngine(llm_client, retriever)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        debate_history = []
        
        # We'll manually run the debate loop here to update UI
        # Or we can modify DebateEngine to yield results. 
        # For simplicity, let's just run it and show results.
        
        with st.spinner("The Council is deliberating..."):
            # Create a container for the debate output
            debate_container = st.container()
            
            for entry in debate_engine.run_debate(question, selected_agents):
                debate_history.append(entry)
                with debate_container:
                    with st.expander(f"{entry['agent']} Response", expanded=True):
                        st.markdown(entry['response'])
        
        # Consensus
        st.subheader("📜 Council Consensus Plan")
        with st.spinner("The Moderator is drafting the final plan..."):
            consensus_engine = ConsensusEngine(llm_client)
            final_plan = consensus_engine.generate_consensus(question, debate_history)
            st.markdown(final_plan)

st.markdown("---")
st.markdown("*Made by Jaiditya Nair*")
