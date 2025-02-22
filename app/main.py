from .requirement_definition_phase import RequirementDefinitionPhase1


def main():
    requirement_phase = RequirementDefinitionPhase1()
    crew = requirement_phase.crew()
    result = crew.kickoff()
    print(result)


if __name__ == "__main__":
    main()
