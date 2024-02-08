

BASIC_PROMPT = """
# Instructions
{{ instructions }}
"""

CHAIN_OF_THOUGHT_PROMPT = """
# Instructions
{{ instructions }}

# Examples
{{ examples }}

# Question
{{ question }}
"""

AGENT_PROMPT = """
# Instructions
{{ instructions }}

# Examples
{{ examples }}

# Question
{{ question }}

# Tool Results
{{ tool_results }}
"""
