#!/usr/bin/env python
from random import randint

from pydantic import BaseModel
from crewai import LLM
from crewai.flow import Flow, listen, start
from crews.tree_generator_crew.tree_generator_crew import TreeGeneratorCrew
from crews.file_resume_crew.file_resume_crew import FileResumeCrew
from library_functions import listar_arquivos, extrair_conteudo_arquivo, append_to_resume
class TreeState(BaseModel):
    files: str = listar_arquivos('C:/Users/brunoesteves/PycharmProjects/CrewAi/herdade-gaviao-agentic-ai/herdade_gaviao', ['.venv', '.git','.idea','__pycache__'])[0]
    files_list : list = listar_arquivos('C:/Users/brunoesteves/PycharmProjects/CrewAi/herdade-gaviao-agentic-ai/herdade_gaviao', ['.venv', '.git','.idea','__pycache__'])[1]
    tree_structure : str = ""
    file_content : str = ""



class TreeFlow(Flow[TreeState]):

    @start()
    def generate_tree(self):
        print("Generating documentation")
        result = (
            TreeGeneratorCrew()
            .crew()
            .kickoff(inputs={"files": self.state.files})
        )
        self.state.tree_structure = str(result.raw)
        print("Tree generated \n", result.raw)


    @listen(generate_tree)
    def read_filex(self):
        for file in self.state.files_list:
            print("FILE PATH : ", file)
            try:
                content = extrair_conteudo_arquivo(file,[".db"])
                if(content == None):
                    print("CONTENT ",content)
                    pass
                else:
                    self.state.file_content = content
                    result = (
                        FileResumeCrew()
                        .crew()
                        .kickoff(inputs={"file_content": self.state.file_content,
                                         "tree_project": self.state.tree_structure,
                                         "file_path" : file})
                    )
                    append_to_resume(result.raw)
            except Exception as exp:
                print("ERROR, ", exp)




def kickoff():
    tree_flow = TreeFlow()
    tree_flow.kickoff()


if __name__ == "__main__":
    kickoff()
