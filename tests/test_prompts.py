from syncom.prompts.agent import AgentTemplate


def test_agent_prompt():
    data = {
        "instructions": "Instructions",
        "examples": [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ],
        "question": "Main-Q",
        "tool_results": {"result": "data"},
    }
    template = AgentTemplate(**data)
    result = template.render()
    expected = (
        '\n# Instructions\nInstructions\n\n'
        '# Examples\n\n'
        '## Example 1\n### Question\nQ1\n### Answer\nA1\n\n'
        '## Example 2\n### Question\nQ2\n### Answer\nA2\n\n\n\n'
        '# Tool Results\n{&#x27;result&#x27;: &#x27;data&#x27;}\n\n\n'
        '# Question\nMain-Q\n'
    )
    assert result == expected
