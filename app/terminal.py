from requirement_definition_phase import RequirementDefinitionPhase
import os


def main():
    requirement_phase = RequirementDefinitionPhase()
    request_csv_path = os.path.join(os.path.dirname(__file__), "request_list.csv")
    crew = requirement_phase.crew()
    result = crew.kickoff(
        inputs={"request_list_path": request_csv_path}
    )
    print(result)


if __name__ == "__main__":
    main()
