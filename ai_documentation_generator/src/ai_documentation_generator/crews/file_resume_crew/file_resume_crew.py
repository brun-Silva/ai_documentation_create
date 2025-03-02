from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


from dotenv import load_dotenv
import os

load_dotenv()

#acessar as variáveis de ambiente

model = os.getenv("MODEL")
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL_LINK")


llm = LLM(
    model=model,
    temperature=0.7,            # Para saídas mais criativas
    timeout=120,                # Tempo máximo de espera (em segundos)
    max_tokens=1000,            # Tamanho máximo da resposta
    top_p=0.9,                  # Parâmetro de amostragem nucleus
    frequency_penalty=0.1,      # Reduz a repetição
    presence_penalty=0.1,       # Estimula diversidade nos tópicos
    seed=42,                    # Garante reprodutibilidade
    # Observe que adicionamos "/v1" ao base_url para utilizar o endpoint correto
    base_url=base_url,
    api_key=api_key          # Valor dummy para satisfazer a exigência do parâmetro api_key
)


@CrewBase
class FileResumeCrew:
    """Poem Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def code_architect_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["code_architect_agent"],
            llm=llm
        )
    @agent
    def doc_integrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["doc_integrator_agent"],
            llm=llm
        )
    @agent
    def cross_validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cross_validation_agent"],
            llm=llm
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def code_architect_task(self) -> Task:
        return Task(
            config=self.tasks_config["code_architect_task"],
        )
    @task
    def doc_integrator_task(self) -> Task:
        return Task(
            config=self.tasks_config["doc_integrator_task"],
        )
    @task
    def cross_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config["cross_validation_task"],
        )
    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
