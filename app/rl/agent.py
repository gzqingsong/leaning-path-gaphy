from typing import Dict

class SimpleAgent:
    def select_action(self, state: Dict[str, float]) -> str:
        # Choose the lowest-mastery kp
        return min(state.items(), key=lambda kv: kv[1])[0]