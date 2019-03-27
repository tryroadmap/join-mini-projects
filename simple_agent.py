from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

import time

import logging

# Functions
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_BARRACKS = 21
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_NOT_QUEUED = [0]
_QUEUED = [1]

class SimpleAgent(base_agent.BaseAgent):
    def __init__(self):
        super(SimpleAgent, self).__init__()

        self.attack_coordinates = None
        self.supply_depot_built = None
        self.barracks_built = None
        self.scv_selected = None
        self.base_top_left = None
        self.commandcenter_selected = None


    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
            obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
            obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]

    def step(self, obs):
        super(SimpleAgent, self).step(obs)

        time.sleep(0.25)

        if obs.first():
            player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                                features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()

            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
            else:
                self.attack_coordinates = (12, 16)


        if not self.supply_depot_built:
            if not self.scv_selected:
                unit_type_scv = self.get_units_by_type(obs, units.Terran.SCV)
                #logging.warning(unit_type_scv)
                if len(unit_type_scv) > 0:
                    if self.unit_type_is_selected(obs, units.Terran.SCV):
                        if (actions.FUNCTIONS.Build_SupplyDepot_screen.id in
                        obs.observation.available_actions):
                            x = random.randint(0, 83)
                            y = random.randint(0, 83)

                            logging.warning("unit type selected scv buidling supply depot" )
                            #self.supply_depot_built = True #flag
                            #self.scv_selected = True #flag
                            return(actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x , y)))


        if not self.commandcenter_selected:
            if self.can_do(obs, actions.FUNCTIONS.Train_SCV_quick.id):
                return(actions.FUNCTIONS.Train_SCV_quick("now"))



        if not self.barracks_built: #TODO add condition count  > 3
            if not self.scv_selected:
                unit_type_scv = self.get_units_by_type(obs, units.Terran.SCV)
                if len(unit_type_scv) > 0:
                    logging.warning("barracks point 1" )
                    if self.unit_type_is_selected(obs, units.Terran.SCV):
                        if (actions.FUNCTIONS.Build_Barracks_screen.id in
                        obs.observation.available_actions):
                            logging.warning("barracks point 2" )
                            x = random.randint(0, 83)
                            y = random.randint(0, 83)
                            return(actions.FUNCTIONS.Build_Barracks_screen("now", (x , y)))






        return actions.FUNCTIONS.no_op()





def main(unused_argv):
  logging.basicConfig(filename='pysc2.log',level=logging.DEBUG , format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
  agent = SimpleAgent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.terran),
                   sc2_env.Bot(sc2_env.Race.random,
                               sc2_env.Difficulty.very_easy)],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=16,
          game_steps_per_episode=0,
          visualize=True) as env:

        agent.setup(env.observation_spec(), env.action_spec())

        timesteps = env.reset()
        agent.reset()

        while True:
          step_actions = [agent.step(timesteps[0])]
          if timesteps[0].last():
            break
          timesteps = env.step(step_actions)

  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
    app.run(main)
