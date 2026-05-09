"""
graph.py — State Definition + Graph Assembly
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from nodes.collect_input import collect_input
from nodes.agent1_research import agent1_research
from nodes.agent2_coach import agent2_coach
from nodes.generate_report import generate_report


class InterviewPrepState(TypedDict):
    # Inputs
    company_name: str
    role_name: str
    job_description: str
    resume_text: str
    experience_level: str

    # Agent 1 outputs
    company_info: dict
    key_facts: List[str]           # Broader than "news" — any useful info
    culture_signals: dict
    salary_data: dict
    jd_keywords: List[str]
    red_flags: List[str]
    competitor_companies: List[str]
    interview_process: dict

    # Agent 2 outputs (Groq — includes questions now)
    company_brief: str
    resume_deep_review: dict
    how_to_prepare: dict
    interview_questions: List[str]  # Moved to Agent 2 (Groq is faster)
    salary_strategy: str
    confidence_score: int
    confidence_reasoning: str

    # Control
    errors: List[str]
    current_step: str
    final_report: str


def build_graph():
    """Build and compile the LangGraph workflow (for teaching)."""
    graph = StateGraph(InterviewPrepState)
    graph.add_node("collect_input", collect_input)
    graph.add_node("agent1_research", agent1_research)
    graph.add_node("agent2_coach", agent2_coach)
    graph.add_node("generate_report", generate_report)
    graph.set_entry_point("collect_input")
    graph.add_edge("collect_input", "agent1_research")
    graph.add_edge("agent1_research", "agent2_coach")
    graph.add_edge("agent2_coach", "generate_report")
    graph.add_edge("generate_report", END)
    return graph.compile()