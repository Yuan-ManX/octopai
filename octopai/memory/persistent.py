import os
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
import asyncio


@dataclass
class MemoryFact:
    id: str
    content: str
    category: str
    confidence: float
    source: str
    timestamp: float
    tags: List[str] = field(default_factory=list)
    access_count: int = 0
    last_accessed: Optional[float] = None


@dataclass
class UserPreference:
    key: str
    value: Any
    category: str
    description: str
    timestamp: float
    strength: float = 1.0
    examples: List[str] = field(default_factory=list)


@dataclass
class ConversationSummary:
    id: str
    title: str
    summary: str
    started_at: float
    ended_at: float
    key_topics: List[str] = field(default_factory=list)
    skills_used: List[str] = field(default_factory=list)
    artifacts_generated: List[str] = field(default_factory=list)


@dataclass
class UserProfile:
    user_id: str
    created_at: float
    last_active: float
    preferences: Dict[str, UserPreference] = field(default_factory=dict)
    facts: List[MemoryFact] = field(default_factory=list)
    conversation_history: List[ConversationSummary] = field(default_factory=list)
    skill_usage_stats: Dict[str, int] = field(default_factory=dict)
    writing_style: Optional[Dict[str, Any]] = None
    technical_stack: List[str] = field(default_factory=list)


class PersistentMemory:
    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or os.path.join(os.getcwd(), "memory")
        self._ensure_storage_dir()
        self.profiles: Dict[str, UserProfile] = {}
        self._load_profiles()
        
    def _ensure_storage_dir(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def _get_profile_path(self, user_id: str) -> str:
        safe_user_id = hashlib.md5(user_id.encode()).hexdigest()
        return os.path.join(self.storage_dir, f"{safe_user_id}.json")
        
    def _load_profiles(self):
        if not os.path.exists(self.storage_dir):
            return
            
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.storage_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    profile = self._dict_to_profile(data)
                    self.profiles[profile.user_id] = profile
                except Exception as e:
                    print(f"Failed to load profile {filename}: {e}")
                    
    def _save_profile(self, profile: UserProfile):
        filepath = self._get_profile_path(profile.user_id)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._profile_to_dict(profile), f, ensure_ascii=False, indent=2)
            
    def _profile_to_dict(self, profile: UserProfile) -> Dict[str, Any]:
        return {
            "user_id": profile.user_id,
            "created_at": profile.created_at,
            "last_active": profile.last_active,
            "preferences": {k: asdict(v) for k, v in profile.preferences.items()},
            "facts": [asdict(f) for f in profile.facts],
            "conversation_history": [asdict(s) for s in profile.conversation_history],
            "skill_usage_stats": profile.skill_usage_stats,
            "writing_style": profile.writing_style,
            "technical_stack": profile.technical_stack
        }
        
    def _dict_to_profile(self, data: Dict[str, Any]) -> UserProfile:
        profile = UserProfile(
            user_id=data["user_id"],
            created_at=data["created_at"],
            last_active=data["last_active"],
            skill_usage_stats=data.get("skill_usage_stats", {}),
            writing_style=data.get("writing_style"),
            technical_stack=data.get("technical_stack", [])
        )
        
        profile.preferences = {
            k: UserPreference(**v) 
            for k, v in data.get("preferences", {}).items()
        }
        
        profile.facts = [MemoryFact(**f) for f in data.get("facts", [])]
        profile.conversation_history = [
            ConversationSummary(**s) 
            for s in data.get("conversation_history", [])
        ]
        
        return profile
        
    def get_or_create_profile(self, user_id: str) -> UserProfile:
        if user_id not in self.profiles:
            profile = UserProfile(
                user_id=user_id,
                created_at=time.time(),
                last_active=time.time()
            )
            self.profiles[user_id] = profile
            self._save_profile(profile)
        else:
            profile = self.profiles[user_id]
            profile.last_active = time.time()
            self._save_profile(profile)
        return profile
        
    def add_fact(
        self,
        user_id: str,
        content: str,
        category: str,
        source: str,
        confidence: float = 0.8,
        tags: Optional[List[str]] = None
    ) -> MemoryFact:
        profile = self.get_or_create_profile(user_id)
        
        existing_fact = self._find_existing_fact(profile, content, category)
        if existing_fact:
            existing_fact.confidence = max(existing_fact.confidence, confidence)
            existing_fact.timestamp = time.time()
            if tags:
                existing_fact.tags = list(set(existing_fact.tags + tags))
            self._save_profile(profile)
            return existing_fact
            
        fact_id = hashlib.md5(f"{user_id}:{content}:{time.time()}".encode()).hexdigest()[:16]
        fact = MemoryFact(
            id=fact_id,
            content=content,
            category=category,
            confidence=confidence,
            source=source,
            timestamp=time.time(),
            tags=tags or []
        )
        
        profile.facts.append(fact)
        self._save_profile(profile)
        return fact
        
    def _find_existing_fact(
        self,
        profile: UserProfile,
        content: str,
        category: str
    ) -> Optional[MemoryFact]:
        normalized_content = content.lower().strip()
        for fact in profile.facts:
            if fact.category == category and fact.content.lower().strip() == normalized_content:
                return fact
        return None
        
    def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        limit: int = 100
    ) -> List[MemoryFact]:
        profile = self.get_or_create_profile(user_id)
        
        facts = profile.facts.copy()
        
        if category:
            facts = [f for f in facts if f.category == category]
            
        if tags:
            facts = [f for f in facts if any(tag in f.tags for tag in tags)]
            
        if min_confidence > 0:
            facts = [f for f in facts if f.confidence >= min_confidence]
            
        facts.sort(key=lambda x: (-x.confidence, -x.timestamp))
        
        for fact in facts[:limit]:
            fact.access_count += 1
            fact.last_accessed = time.time()
            
        self._save_profile(profile)
        return facts[:limit]
        
    def delete_fact(self, user_id: str, fact_id: str) -> bool:
        profile = self.get_or_create_profile(user_id)
        initial_len = len(profile.facts)
        profile.facts = [f for f in profile.facts if f.id != fact_id]
        
        if len(profile.facts) < initial_len:
            self._save_profile(profile)
            return True
        return False
        
    def set_preference(
        self,
        user_id: str,
        key: str,
        value: Any,
        category: str,
        description: str,
        strength: float = 1.0,
        example: Optional[str] = None
    ) -> UserPreference:
        profile = self.get_or_create_profile(user_id)
        
        if key in profile.preferences:
            pref = profile.preferences[key]
            pref.value = value
            pref.timestamp = time.time()
            pref.strength = max(pref.strength, strength)
            if example and example not in pref.examples:
                pref.examples.append(example)
        else:
            pref = UserPreference(
                key=key,
                value=value,
                category=category,
                description=description,
                timestamp=time.time(),
                strength=strength,
                examples=[example] if example else []
            )
            profile.preferences[key] = pref
            
        self._save_profile(profile)
        return pref
        
    def get_preference(
        self,
        user_id: str,
        key: str,
        default: Any = None
    ) -> Any:
        profile = self.get_or_create_profile(user_id)
        pref = profile.preferences.get(key)
        return pref.value if pref else default
        
    def get_all_preferences(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> Dict[str, UserPreference]:
        profile = self.get_or_create_profile(user_id)
        
        if category:
            return {k: v for k, v in profile.preferences.items() if v.category == category}
        return profile.preferences.copy()
        
    def add_conversation_summary(
        self,
        user_id: str,
        conversation_id: str,
        title: str,
        summary: str,
        started_at: float,
        ended_at: float,
        key_topics: Optional[List[str]] = None,
        skills_used: Optional[List[str]] = None,
        artifacts_generated: Optional[List[str]] = None
    ) -> ConversationSummary:
        profile = self.get_or_create_profile(user_id)
        
        conv_summary = ConversationSummary(
            id=conversation_id,
            title=title,
            summary=summary,
            started_at=started_at,
            ended_at=ended_at,
            key_topics=key_topics or [],
            skills_used=skills_used or [],
            artifacts_generated=artifacts_generated or []
        )
        
        profile.conversation_history.append(conv_summary)
        
        for skill in skills_used or []:
            profile.skill_usage_stats[skill] = profile.skill_usage_stats.get(skill, 0) + 1
            
        profile.conversation_history.sort(key=lambda x: -x.started_at)
        
        if len(profile.conversation_history) > 100:
            profile.conversation_history = profile.conversation_history[:100]
            
        self._save_profile(profile)
        return conv_summary
        
    def get_conversation_history(
        self,
        user_id: str,
        limit: int = 20,
        topic: Optional[str] = None
    ) -> List[ConversationSummary]:
        profile = self.get_or_create_profile(user_id)
        
        history = profile.conversation_history.copy()
        
        if topic:
            topic_lower = topic.lower()
            history = [
                h for h in history 
                if topic_lower in h.title.lower() 
                or topic_lower in h.summary.lower()
                or any(topic_lower in t.lower() for t in h.key_topics)
            ]
            
        return history[:limit]
        
    async def extract_and_store(
        self,
        user_id: str,
        conversation_text: str,
        source: str = "conversation"
    ):
        from octopai.skills.factory import SkillFactory
        
        profile = self.get_or_create_profile(user_id)
        
        extraction_prompt = f"""
        从以下对话中提取关键信息、用户偏好和事实：

        对话内容：
        {conversation_text}

        请返回JSON格式的结果，包含：
        {{
            "facts": [
                {{
                    "content": "事实内容",
                    "category": "类别（如personal, professional, technical等）",
                    "tags": ["标签1", "标签2"],
                    "confidence": 0.9
                }}
            ],
            "preferences": [
                {{
                    "key": "偏好键名",
                    "value": "偏好值",
                    "category": "类别",
                    "description": "描述"
                }}
            ],
            "topics": ["主题1", "主题2"]
        }}
        """
        
        try:
            factory = SkillFactory()
            skill = factory.create_skill(
                name="memory_extraction",
                description="从对话中提取记忆",
                prompt=extraction_prompt,
                inputs={"conversation": conversation_text},
                outputs={"facts": List[Dict], "preferences": List[Dict], "topics": List[str]}
            )
            
            result = await skill.execute()
            
            for fact_data in result.get("facts", []):
                self.add_fact(
                    user_id=user_id,
                    content=fact_data["content"],
                    category=fact_data["category"],
                    source=source,
                    confidence=fact_data.get("confidence", 0.8),
                    tags=fact_data.get("tags", [])
                )
                
            for pref_data in result.get("preferences", []):
                self.set_preference(
                    user_id=user_id,
                    key=pref_data["key"],
                    value=pref_data["value"],
                    category=pref_data["category"],
                    description=pref_data["description"]
                )
                
        except Exception as e:
            print(f"Failed to extract memory: {e}")
            
    def get_memory_context(
        self,
        user_id: str,
        current_task: Optional[str] = None,
        max_facts: int = 10,
        max_preferences: int = 10
    ) -> Dict[str, Any]:
        profile = self.get_or_create_profile(user_id)
        
        facts = self.get_facts(
            user_id=user_id,
            limit=max_facts
        )
        
        preferences = list(self.get_all_preferences(user_id).values())
        preferences.sort(key=lambda x: (-x.strength, -x.timestamp))
        preferences = preferences[:max_preferences]
        
        recent_conversations = self.get_conversation_history(user_id, limit=3)
        
        context = {
            "user_id": user_id,
            "facts": [
                {
                    "content": f.content,
                    "category": f.category,
                    "confidence": f.confidence,
                    "tags": f.tags
                }
                for f in facts
            ],
            "preferences": [
                {
                    "key": p.key,
                    "value": p.value,
                    "category": p.category,
                    "description": p.description
                }
                for p in preferences
            ],
            "recent_conversations": [
                {
                    "title": c.title,
                    "summary": c.summary,
                    "key_topics": c.key_topics
                }
                for c in recent_conversations
            ],
            "skill_usage_stats": profile.skill_usage_stats.copy(),
            "technical_stack": profile.technical_stack.copy()
        }
        
        if profile.writing_style:
            context["writing_style"] = profile.writing_style
            
        return context
        
    def update_writing_style(
        self,
        user_id: str,
        style_features: Dict[str, Any]
    ):
        profile = self.get_or_create_profile(user_id)
        
        if profile.writing_style is None:
            profile.writing_style = {}
            
        for key, value in style_features.items():
            profile.writing_style[key] = value
            
        self._save_profile(profile)
        
    def update_technical_stack(
        self,
        user_id: str,
        technologies: List[str]
    ):
        profile = self.get_or_create_profile(user_id)
        
        for tech in technologies:
            if tech not in profile.technical_stack:
                profile.technical_stack.append(tech)
                
        self._save_profile(profile)
