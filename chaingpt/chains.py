from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM


class TaskCreationChain(LLMChain):
    def __init__(self, llm: BaseLLM, **kwargs):
        super().__init__(llm, **kwargs)
        self.prompt_template = PromptTemplate(
            "{input} {context} What tasks should be created and performed?"
        )

    def __call__(self, inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        prompt = self.prompt_template.render(input=inputs)
        response = self.llm(prompt)
        return response["tasks"]


class TaskPrioritizationChain(LLMChain):
    def __init__(self, llm: BaseLLM, **kwargs):
        super().__init__(llm, **kwargs)
        self.prompt_template = PromptTemplate(
            "{tasks} {context} How should these tasks be prioritized?"
        )

    def __call__(self, tasks: List[Dict[str, Any]]) -> deque:
        prompt = self.prompt_template.render(tasks=tasks)
        response = self.llm(prompt)
        return deque(response["prioritized_tasks"])


class ExecutionChain(LLMChain):
    def __init__(self, llm: BaseLLM, **kwargs):
        super().__init__(llm, **kwargs)
        self.prompt_template = PromptTemplate(
            "{task} {input} {context} Execute the task and provide the result."
        )

    def __call__(self, task: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self.prompt_template.render(task=task, input=inputs)
        response = self.llm(prompt)
        return response["result"]
