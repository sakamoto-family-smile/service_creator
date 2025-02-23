from crewai import Agent, Crew, Task, Process, LLM
from service_creator_agents import (
    product_manager,
    engineer_manager,
    infrastructure_engineer
)
from service_creator_tools import google_search_tool, human_feedback_tool
import os
import pandas as pd


class RequirementDefinitionPhase1:
    def __init__(self) -> None:
        self.__llm_instance = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY")
        )  # TODO : 各Agentごとにllmを設定したい

    def before_kickoff(self, inputs):
        csv_path = inputs["request_list_path"]
        df = pd.read_csv(csv_path)
        return {"request_table": df.to_string()}

    def product_manager(self) -> Agent:
        goal = """
・主体的に要求から機能要件と非機能要件をcsvフォーマットで構築する。Product Managerと協力すること。
・SLO/SLAの設定をEngineer Managerと協力して、構築する
        """
        return product_manager(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool(), human_feedback_tool()]
        )

    def engineer_manager(self) -> Agent:
        goal = """
・Product Managerと協力して、機能要件・非機能要件を構築すること
・主体的にSLO/SLAの構築を行い、csvフォーマットで出力すること。Product ManagerやInfrastructure Engineerと協力すること。
        """
        return engineer_manager(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool(), human_feedback_tool()]
        )

    def infrastructure_engineer(self) -> Agent:
        goal = """
・Engineer Managerと協力して、SLO/SLAの構築を実施すること
        """
        return infrastructure_engineer(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool(), human_feedback_tool()]
        )

    def task_of_creating_requirement_list(self) -> Task:
        return Task(
            description="""
下記の要件を守って、要求から要件一覧を作成する。

★条件
・要求一覧は表データとして入力される（要求一覧の表を参照）
・要求一覧から機能要件と非機能要件と分類できるように生成すること
・要件一覧のフォーマットはcsvとすること
・要求一覧の優先度に沿って、要件一覧に優先度をつけること
・要求内容から、ユーザーの作りたいものを想定し、必要に応じて要求の追加や削除をユーザー（human）に確認すること
・非機能要件を構築する際に、サービスを構築する上で現実的な非機能要件か？を、検索処理もしくはEngineer Managerと協議をし、確認すること。
・また非現実的な非機能要件になった場合は、要求の調整をするようにユーザー（human）と調整すること
・各エージェントは日本語でやり取りをしてください


✴️要求一覧の表
{request_table}
            """,
            expected_output="""
要求から機能要件と非機能要件をcsvフォーマットで構築する
            """,
            agent=self.product_manager(),
            output_file="requirements.csv",
            human_input=True
        )

    def task_of_creating_slo_sla_list(self) -> Task:
        return Task(
            description="""
下記の要件を守って、SLO/SLAの一覧を作成する。

✴️条件
・要求一覧は表データとして入力される（要求一覧の表を参照）
・前のタスクで構築した機能要件の一覧と要求一覧を利用して、SLO/SLAの一覧を作成する
・SLO/SLAの一覧のフォーマットはCSVとすること
・SLO/SLAは、一般的なWebサービスを構築する際のSLO/SLAを参考にし、検討すべきメトリクスを設定すること
・SLO/SLAを設定する際に、Infrastructure Engineerと協議し、決めていくこと
・Webサービスを構築する上で、非現実的なSLO/SLAになりそうな場合は、ユーザー（human）やProduct Managerに対し、要求や要件を調整し、SLO/SLAを再設定すること
・各エージェントは日本語でやり取りをしてください

✴️要求一覧の表
{request_table}
            """,
            expected_output="""
要求や要件から、SLO/SLAをcsvフォーマットで構築する
            """,
            agent=self.engineer_manager(),
            output_file="slo_sla.csv",
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
            before_kickoff_callbacks=[self.before_kickoff],
            planning=True,
            planning_llm=self.__llm_instance,
            share_crew=True,
            verbose=True
        )
