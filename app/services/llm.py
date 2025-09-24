from typing import Optional, List
from app.config import settings

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.enabled = bool(self.api_key and OpenAI is not None)
        self._client = OpenAI(api_key=self.api_key) if self.enabled else None

    def explain_plan(self, sequence: List[str], context: str | None = None) -> Optional[str]:
        if not self.enabled or not self._client:
            return None
        prompt = (
            "你是教育领域的路径规划解释助手。基于先修关系和学生薄弱点，为下面的知识点顺序生成简洁、可读的解释。\n"
            f"路径: {' -> '.join(sequence)}\n"
            f"上下文: {context or '无'}\n"
            "请用简短中文要点说明为什么按此顺序最合适，突出先修与认知负荷平衡。"
        )
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content if resp and resp.choices else None

    def explain_resources(self, kp_id: str, resource_types: List[str], style: Optional[str]) -> Optional[str]:
        if not self.enabled or not self._client:
            return None
        prompt = (
            "你是学习资源匹配助手。根据学习风格偏好，对给定知识点的资源类型给出一句话推荐理由。\n"
            f"知识点: {kp_id}\n资源类型: {', '.join(resource_types)}\n学习风格: {style or '未指定'}\n"
            "输出简洁中文，强调风格契合与效率。"
        )
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content if resp and resp.choices else None

    def validate_prereq(self, prerequisite: str, target: str) -> Optional[str]:
        if not self.enabled or not self._client:
            return None
        prompt = (
            "你是先修关系校验助手。判断两个知识点的先修关系是否合理，给出一句话理由。\n"
            f"先修: {prerequisite} -> 目标: {target}\n"
            "仅输出简短中文判断与理由。"
        )
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return resp.choices[0].message.content if resp and resp.choices else None


llm_service = LLMService()