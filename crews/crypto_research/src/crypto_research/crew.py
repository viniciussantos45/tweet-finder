from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class CryptoResearch():
    """CryptoResearch crew"""

    # Path to YAML configuration files for agents and tasks
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Agents Definitions
    @agent
    def macro_economic_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['macro_economic_agent'],
            verbose=True
        )

    @agent
    def crypto_context_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['crypto_context_agent'],
            verbose=True
        )

    @agent
    def crypto_specific_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['crypto_specific_agent'],
            verbose=True
        )

    @agent
    def social_sentiment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['social_sentiment_agent'],
            verbose=True
        )

    @agent
    def regulatory_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['regulatory_agent'],
            verbose=True
        )

    @agent
    def technical_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_analysis_agent'],
            verbose=True
        )

    @agent
    def data_aggregator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_aggregator_agent'],
            verbose=True
        )

    # Tasks Definitions
    @task
    def macro_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['macro_research_task'],
        )

    @task
    def crypto_context_task(self) -> Task:
        return Task(
            config=self.tasks_config['crypto_context_task'],
        )

    @task
    def crypto_specific_task(self) -> Task:
        return Task(
            config=self.tasks_config['crypto_specific_task'],
        )

    @task
    def social_sentiment_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_sentiment_task'],
        )

    @task
    def regulatory_task(self) -> Task:
        return Task(
            config=self.tasks_config['regulatory_task'],
        )

    @task
    def technical_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_analysis_task'],
        )

    @task
    def data_aggregation_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_aggregation_task'],
            output_file='aggregated_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CryptoResearch crew"""
        return Crew(
            agents=self.agents,   # Agents automatically collected by the @agent decorators
            tasks=self.tasks,     # Tasks automatically collected by the @task decorators
            process=Process.sequential,
            verbose=True,
        )
