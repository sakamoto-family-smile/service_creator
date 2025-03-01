from crewai import Agent, Crew, Task, Process, LLM
from service_creator_agents import (
    product_manager,
    engineer_manager,
    infrastructure_engineer
)
from service_creator_tools import (
    google_search_tool,
    HumanFeedbackTool
)
import os
import pandas as pd
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)


class RequirementDefinitionPhase:
    def __init__(self, ui_type: str = "web") -> None:
        self.__llm_instance = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY")
        )  # TODO : 各Agentごとにllmを設定したい

        self.__human_feedback_tool = HumanFeedbackTool(ui_type=ui_type).get_human_feedback_tool()

    def before_kickoff(self, inputs):
        csv_path = inputs["request_list_path"]
        df = pd.read_csv(csv_path).set_index("No")
        return {"request_table": df.to_string()}

    def product_manager(self) -> Agent:
        goal = """
・主体的に要求から機能要件と非機能要件をcsvフォーマットで構築する。Product Managerと協力すること。
・SLO/SLAの設定をEngineer Managerと協力して、構築する
・Engineer Managerと協力して、開発項目一覧を作成すること
・Engineer Managerと協力して、抽象化したコンポーネント図を作成すること
        """
        return product_manager(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool(), self.__human_feedback_tool]
        )

    def engineer_manager(self) -> Agent:
        goal = """
・Product Managerと協力して、機能要件・非機能要件を構築すること
・主体的にSLO/SLAの構築を行い、csvフォーマットで出力すること。Product ManagerやInfrastructure Engineerと協力すること。
・主体的に開発項目一覧の作成を行い、csvフォーマットで出力すること。Product ManagerやInfrastructure Engineerと協力すること。
・主体的にサービス全体の抽象化したコンポーネント図を作成し、drawioのフォーマットで出力すること。Product ManagerやInfrastructure Engineerと協力すること。
        """
        return engineer_manager(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool(), self.__human_feedback_tool]
        )

    def infrastructure_engineer(self) -> Agent:
        goal = """
・Engineer Managerと協力して、SLO/SLAの構築を実施すること
・Engineer Managerと協力して、開発項目一覧を作成すること
・Engineer Managerと協力して、抽象化したコンポーネント図を作成すること
        """
        return infrastructure_engineer(
            goal=goal,
            llm=self.__llm_instance,
            tools=[google_search_tool(), self.__human_feedback_tool]
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
・作成した成果物は、他のエージェントにレビュー依頼を出し、確認してもらってください
・成果物が完成したら、必ずユーザーにレビュー依頼を出すようにしてください

✴️要求一覧の表
{request_table}
            """,
            expected_output="""
要求から機能要件と非機能要件をcsvフォーマットで構築する
            """,
            agent=self.product_manager(),
            output_file="requirements.csv",
            human_input=False
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
・作成した成果物は、他のエージェントにレビュー依頼を出し、確認してもらってください
・成果物が完成したら、必ずユーザーにレビュー依頼を出すようにしてください

✴️要求一覧の表
{request_table}
            """,
            expected_output="""
要求や要件から、SLO/SLAをcsvフォーマットで構築する
            """,
            agent=self.engineer_manager(),
            output_file="slo_sla.csv",
            context=[self.task_of_creating_requirement_list()],
            human_input=False
        )

    # TODO : 工程情報や観点についてはcsvに記載して、テーブルデータとして渡す方がメンテナンスがしやすそう
    def task_of_creating_development_task_list(self) -> Task:
        return Task(
            description="""
下記の条件を守って、開発項目一覧を作成する。

★条件
・要件一覧はcsvデータとして入力される
・SLO/SLA一覧はcsvデータとして入力される
・開発項目一覧のフォーマットはCSVとすること
・開発項目を作る際の観点は後述の「開発項目に関する観点」を遵守すること
・作成した成果物は、他のエージェントにレビュー依頼を出し、確認してもらってください
・成果物が完成したら、必ずユーザーにレビュー依頼を出すようにしてください

★開発項目に関する観点
・バックエンド、フロントエンド、全体のタスクとして分類が可能であること
・作業概要、作業詳細、工程、主担当の情報が開発項目ごとに明記されていること
・担当は各エージェントに割り振ること
・工程については、後述する「工程情報」から選択すること

★工程情報
・要件定義フェーズ: 要求から要件を抽出するフェーズ。抽象的なインフラ設計、開発項目作成、非機能要求整理（SLA/SLO）も実施する。
・設計フェーズ: 要件から、具体的なインフラ設計やデータベース設計、クラス図、シーケンス図の作成を行い、次の実装フェーズに繋げる。
・実装フェーズ: 設計フェーズで構築した情報を元に、プログラミング言語を用いて、バックエンド・フロントエンドごとに実装を行う。
・単体テスト実装フェーズ: 実装フェーズで実装したコードに関して、要件通りに動作するかを検証するためにUnitTestを実装する。プログラミング言語ごとに実装する。
・単体テスト実行フェーズ: 単体テスト実装フェーズで実装したUnitTestを実行し、期待通りに動作していないコードについて改修を行う。
・QAテスト設計フェーズ: 要件から、第三者試験（フロントエンドとバックエンドを結合した試験）を行うためのQAテスト項目を設計、作成する
・QAテスト実装フェーズ: QAテスト設計フェーズで構築したQAテスト項目を使って、テストを実装する
・QAテスト実行フェーズ: QAテスト実装フェーズで構築したQAテストを使って、テストを実行する

★チームに関する情報
            """,
            expected_output="""
            """,
            agent=self.engineer_manager(),
            output_file="development_task_list.csv",
            context=[self.task_of_creating_slo_sla_list()],
            human_input=False
        )

    # TODO : implement
    def task_of_creating_abstract_architecture_diagram_of_service(self):
        return Task(
            description="""
            """,
            expected_output="""
            """,
            agent=self.engineer_manager(),
            output_file="abstract_architecture_diagram_of_service.csv",
            context=[self.task_of_creating_development_task_list()],
            human_input=False
        )

    # TODO : タスクごとの成果物をユーザーが取得できるように修正する
    # UI関連の関数は外からもらうようにしたい
    def task_completion_callback(self, task_result):
        logging.info(f"task result is {task_result}")

    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.product_manager(),
                self.engineer_manager(),
                self.infrastructure_engineer()
            ],
            tasks=[
                self.task_of_creating_requirement_list(),
                self.task_of_creating_slo_sla_list(),
                self.task_of_creating_development_task_list()
            ],
            process=Process.sequential,
            before_kickoff_callbacks=[self.before_kickoff],
            planning=True,
            planning_llm=self.__llm_instance,
            share_crew=True,
            task_callback=self.task_completion_callback,
            verbose=True
        )
