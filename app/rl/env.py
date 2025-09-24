from typing import Dict, List, Tuple

class LearningPathEnv:
    def __init__(self, knowledge_points: List[str]):
        self.knowledge_points = knowledge_points
        self.state: Dict[str, float] = {kp: 0.0 for kp in knowledge_points}

    def reset(self) -> Dict[str, float]:
        self.state = {kp: 0.0 for kp in self.knowledge_points}
        return self.state

    def step(self, action_kp: str) -> Tuple[Dict[str, float], float, bool, Dict]:
        # Simplified: improve mastery a bit and give reward
        prev = self.state.get(action_kp, 0.0)
        new = min(1.0, prev + 0.1)
        self.state[action_kp] = new
        reward = new - prev
        done = all(v >= 1.0 for v in self.state.values())
        return self.state, reward, done, {}