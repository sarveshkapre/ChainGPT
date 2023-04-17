from typing import Dict, List
from langchain.llms import LLMChain


def get_next_task(
    task_creation_chain: LLMChain,
    result: Dict,
    task_description: str,
    task_list: List[str],
    objective: str,
) -> List[Dict]:
    inputs = {
        "result": result,
        "task_description": task_description,
        "task_list": task_list,
        "objective": objective,
    }
    tasks = task_creation_chain(inputs)
    return tasks


def prioritize_tasks(
    task_prioritization_chain: LLMChain,
    this_task_id: int,
    task_list: List[Dict],
    objective: str,
) -> List[Dict]:
    inputs = {
        "this_task_id": this_task_id,
        "task_list": task_list,
        "objective": objective,
    }
    prioritized_tasks = task_prioritization_chain(inputs)
    return prioritized_tasks


def execute_task(
    execution_chain: LLMChain, objective: str, task: str, k: int = 5
) -> str:
    inputs = {"objective": objective, "task": task}
    result = execution_chain(inputs)
    top_k_results = result["results"][:k]
    return top_k_results
