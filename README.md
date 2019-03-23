# pysc2-ai
inspired by skjb work on pysc2-tutorial


### Setup

```
pip3 install -r requirements.txt
```
### To run:
```
python -m pysc2.bin.agent --map Simple64 --agent simple_agent.SimpleAgent --agent_race terran
```

You can find your accountid and serverid as directory names under ```~/Library/Application Support/Blizzard/StarCraft II/Accounts```.

Now you can open the replays using the Starcraft UI: they can be found in Replays.


###References:
[environment var obs official repo](https://github.com/deepmind/pysc2/blob/master/docs/environment.md#minimap)
[training smart agents jan 2018] http://chris-chris.ai/2017/11/06/pysc2-tutorial2/
