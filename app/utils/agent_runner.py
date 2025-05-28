def run_query_agent(question, columns):
    from app.agents.mistral_agent import load_mistral_agent
    agent = load_mistral_agent()
    return agent.run({"question": question, "columns": columns})

def run_insight_agent(question, result):
    from app.agents.insight_agent import load_insight_agent
    agent = load_insight_agent()
    return agent.run({"question": question, "result": result})

def run_chart_agent(question, result):
    from app.agents.chart_agent import load_chart_agent
    agent = load_chart_agent()
    return agent.run({"question": question, "result": result})
