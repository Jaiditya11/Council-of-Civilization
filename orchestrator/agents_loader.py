import yaml
import os
import logging

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, name, role, domain_collection, system_prompt):
        self.name = name
        self.role = role
        self.domain_collection = domain_collection
        self.system_prompt = system_prompt

    def __repr__(self):
        return f"<Agent {self.name}>"

def load_agents(agents_dir="agents"):
    """
    Load all agent configurations from the agents directory.
    """
    agents = []
    if not os.path.exists(agents_dir):
        logger.warning(f"Agents directory not found: {agents_dir}")
        return agents

    for filename in os.listdir(agents_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(agents_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    config = yaml.safe_load(f)
                    agent = Agent(
                        name=config.get("name"),
                        role=config.get("role"),
                        domain_collection=config.get("domain_collection"),
                        system_prompt=config.get("system_prompt")
                    )
                    agents.append(agent)
                    logger.info(f"Loaded agent: {agent.name}")
            except Exception as e:
                logger.error(f"Error loading agent from {filename}: {e}")
    
    return agents
