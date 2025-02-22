from .requirement_definition_phase import RequirementDefinitionPhase
import json
import os


def main():
    with open(os.path.join(os.path.dirname(__file__), "basic_role_define.json"), "r") as f:
        basic_role_define_dict = json.load(f)

    requirement_phase = RequirementDefinitionPhase(basic_role_define=basic_role_define_dict)
    crew = requirement_phase.crew()
    crew.kickoff()


if __name__ == "__main__":
    main()
