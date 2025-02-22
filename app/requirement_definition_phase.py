from crewai import Agent, Crew, Task, Process, LLM
from .service_creator_agents import (
    product_manager,
    engineer_manager,
    infrastructure_engineer
)
from .service_creator_tools import google_search_tool
import os


class RequirementDefinitionPhase:
    def __init__(self) -> None:
        self.__llm_instance = LLM(
            model="gemini-2.0-flash",
            api_key=os.environ.get("GEMINI_API_KEY")
        )  # TODO : 各Agentごとにllmを設定したい

    def product_manager(self) -> Agent:
        goal = """
あああ
        """
        return product_manager(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool()]
        )

    def engineer_manager(self) -> Agent:
        goal = """
あああ
        """
        return engineer_manager(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool()]
        )

    def infrastructure_engineer(self) -> Agent:
        goal = """
あああ
        """
        return infrastructure_engineer(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool()]
        )

    def task_of_creating_requirement_list(self) -> Task:
        return Task(
            description="""
要求から要件一覧を作成する。
            """,
            expected_output="""
            """,
            agent=self.product_manager(),
            output_file="",
            human_input=True
        )

    def task_of_creating_slo_sla_list(self) -> Task:
        return Task(
            description="""
            """,
            expected_output="""
            """,
            agent=self.engineer_manager(),
            output_file="",
            context=[self.task_of_creating_requirement_list()],
            human_input=True
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.product_manager(),
                self.engineer_manager(),
                self.infrastructure_engineer()
            ],
            tasks=[
                self.task_of_creating_requirement_list(),
                self.task_of_creating_slo_sla_list()
            ],
            process=Process.sequential,
            verbose=True
        )
