from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import FileReadTool, SerperDevTool
from models.models import JobResults
import json

from dotenv import load_dotenv

load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

resume_file_read_tool = FileReadTool(file_path="data/sample_resume.txt")
jobs_file_read_tool = FileReadTool(file_path="data/sample_jobs.json")
search_tool = SerperDevTool(n_results=5)

@CrewBase
class AutomatedJobSearch():
    """AutomatedJobSearch crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, query: str):
        self.query = query
        self.response_schema = json.dumps(JobResults.model_json_schema(), indent=2)

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def job_search_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_search_expert_agent'],
            tools=[jobs_file_read_tool], 
            verbose=True
        )

    @agent
    def job_rating_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_rating_expert_agent'],
            tools=[resume_file_read_tool],
            verbose=True
        )

    @agent
    def company_rating_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['company_rating_expert_agent'],
            tools=[search_tool], 
            verbose=True
        )

    @agent
    def summarization_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarization_expert_agent'],
            tools=None,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def job_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_search_task'], # type: ignore[index]
            input={"query": self.query}
        )

    @task
    def job_rating_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_rating_task'], # type: ignore[index]
        )

    @task
    def evaluate_company_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_company_task'], # type: ignore[index]
            output_schema=self.response_schema
        )

    @task
    def structure_results_task(self) -> Task:
        return Task(
            config=self.tasks_config['structure_results_task'], # type: ignore[index]
            output_schema=self.response_schema
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AutomatedJobSearch crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
