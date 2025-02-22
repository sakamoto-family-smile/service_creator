from crewai import Agent, Crew, Task, Process, LLM
import os


class RquirementDefinitionPhase:
    def __init__(self, basic_role_define: dict) -> None:
        self.__basic_role_define = basic_role_define
        self.__backstory_key = "background"
        self.__llm_key = "llm"  # TODO : こちらを利用したい
        self.__llm_instance = LLM(
            model="gemini-2.0-flash",
            api_key=os.environ.get("GEMINI_API_KEY")
        )  # TODO : 各Agentごとにllmを設定したい

    def product_manager(self) -> Agent:
        role_name = "product_manager"
        return Agent(
            role="Product Manager",
            goal="",
            backstory=self.__basic_role_define[role_name][self.__backstory_key],
            llm=self.__llm_instance,
            verbose=True,
        )

    def engineer_manager(self) -> Agent:
        role_name = "engineer_manager"
        return Agent(
            role="Engineer Manager",
            goal="",
            backstory=self.__basic_role_define[role_name][self.__backstory_key],
            llm=self.__llm_instance,
            verbose=True,
        )

    def infrastructure_engineer(self) -> Agent:
        role_name = "infrastructure_engineer"
        return Agent(
            role="Infrastructure Engineer",
            goal="",
            backstory=self.__basic_role_define[role_name][self.__backstory_key],
            llm=self.__llm_instance,
            verbose=True,
        )

    def task_of_creating_requirement_list(self) -> Task:
        return Task(
            description="""
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
