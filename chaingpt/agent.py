from collections import deque
from typing import Dict, Optional, Any

from pydantic import BaseModel, Field
from .chains import TaskCreationChain, TaskPrioritizationChain, ExecutionChain
from .tasks import (
    get_next_task,
)
from langchain.llms import BaseLLM  # Add the missing import


class ChainGPT(BaseModel):
    task_list: deque = Field(default_factory=deque)
    task_creation_chain: TaskCreationChain = Field(...)
    task_prioritization_chain: TaskPrioritizationChain = Field(...)
    execution_chain: ExecutionChain = Field(...)
    task_id_counter: int = Field(1)
    max_iterations: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True

    def add_task(self, task: Dict):
        self.task_list.append(task)

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        iteration = 0
        while self.task_list and (
            self.max_iterations is None or iteration < self.max_iterations
        ):
            iteration += 1

            # Create tasks
            new_tasks = self.task_creation_chain(inputs)
            for task in new_tasks:
                task["task_id"] = self.task_id_counter
                self.task_id_counter += 1
                self.add_task(task)

            # Prioritize tasks
            self.task_list = self.task_prioritization_chain(self.task_list)

            # Get and execute next task
            next_task = get_next_task(self.task_list)
            if next_task:
                result = self.execution_chain(next_task, inputs)
                inputs.update(result)
                self.task_list.remove(next_task)

        return inputs

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = False, **kwargs) -> "ChainGPT":
        task_creation_chain = TaskCreationChain.from_llm(llm, verbose=verbose)
        task_prioritization_chain = TaskPrioritizationChain.from_llm(
            llm, verbose=verbose
        )
        execution_chain = ExecutionChain.from_llm(llm, verbose=verbose)
        return cls(
            task_creation_chain=task_creation_chain,
            task_prioritization_chain=task_prioritization_chain,
            execution_chain=execution_chain,
            **kwargs,
        )
