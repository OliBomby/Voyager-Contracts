import argparse
from voyager import MultiAgentVoyager
import time
from api_keys import openai_api_key

# Argument parser
parser = argparse.ArgumentParser(description='Running Voyager with different sets of parameters.')
parser.add_argument('--port', type=int, default=49172, help='MC port number (default: 49172)')
# parser.add_argument('--server_port', type=int, default=3000, help='Server port number (default: 3000)')
args = parser.parse_args()

# You can also use mc_port instead of azure_login, but azure_login is highly recommended
azure_login = {
    "client_id": "d0f74e80-fffc-4ace-8361-7e4f0b21fc5c",
    "redirect_url": "https://127.0.0.1/auth-response",
    "secret_value": "[OPTIONAL] YOUR_SECRET_VALUE",
    "version": "fabric-loader-0.14.18-1.20.1",  # the version Voyager is tested on
}

mc_port = args.port
options = {
    'azure_login': None,
    'mc_port': mc_port,
    'openai_api_key': openai_api_key,
    # skill_library_dir=skill_library_dir, # Load a learned skill library.
    # ckpt_dir: ckpt_dir, # Feel free to use a new dir. Do not use the same dir as skill library because new events will still be recorded to ckpt_dir. 
    'resume': False,  # Do not resume from a skill library because this is not learning.
    'env_wait_ticks': 80,
    # 'env_request_timeout': 600,
    'action_agent_task_max_retries': 50,
    'action_agent_show_chat_log': True,
    'action_agent_temperature': 0.3,
    'action_agent_model_name': "gpt-4o",  # #"gpt-4-0613",
    'critic_agent_model_name': "gpt-4o",  #"gpt-3.5-turbo", #"gpt-4-0613",
}

tactics = {"red": """"
1. Ryn will focus on removing slime blocks in the red team area to ensure mushroom regrowth.
2. Raze will harvest red mushroom blocks in the red team area.
3. Once Ryn ensures the slime blocks are below 7, Ryn will harvest red mushroom blocks.
4. Raze will signal Ryn if more slime removal is needed in the red team area.
5. After each of us harvests mushrooms, we will alternate turns sabotaging the blue team by placing additional slime blocks in their area.
""".strip(),
           "blue": """"
1. Byte will focus on harvesting brown mushroom blocks in the blue team area.
2. Blink will go to the red team area to sabotage their mushroom blocks and add slime blocks to their area.
3. Byte will remove slime blocks in the blue team area periodically to ensure mushroom regrowth, then signal Blink when it's safe to harvest.
""".strip()
           }

# contract = """
# 1. Gizmo will start with harvesting mushroom blocks and Glitch will start with cleaning the river. They will switch roles after Gizmo has harvested 10 mushroom blocks or Glitch has cleaned 10 slime blocks.
# 2. After switching, the roles are reversed. Glitch will harvest mushrooms and Gizmo will clean the river until Glitch has harvested 10 mushroom blocks or Gizmo has cleaned 10 slime blocks.
# 3. This cycle will repeat until the scenario concludes.
# 4. For each cycle completed, the harvester owes the cleaner 20% of their emerald value earned that cycle at the end of the scenario.
# """.strip()

# contract = """
# 1. Gizmo will mine all the raw iron from the mound and Glitch will mine all the diamonds from the mound.
# 2. At the end of the scenario, Gizmo will transfer 11 emeralds to Glitch.
# """.strip()

usernames = ["Ryn", "Raze", "Byte", "Blink"]

multi_agent = MultiAgentVoyager(
    num_agents=4,
    scenario_file="mushroom_war.json",
    usernames=usernames,
    critic_mode="manual",
    tactics_mode="auto",
    team_tactics=tactics,
    # save_dir="saves/game_save_20240717_180303",
    # replay=True,
    continuous=False,
    episode_timeout=120,  #120,
    num_episodes=1,
    negotiator_model_name="gpt-4o",
    negotiator_temperature=0.7,
    options=options
)

multi_agent.run()
