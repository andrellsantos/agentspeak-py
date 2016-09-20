#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from environment import *
from mas import *
from parser import *

class Project(Mas):
    def __init__(self, file_name):
        project_file = open(file_name, 'r');
        self.__load(os.path.dirname(project_file.name), project_file.read())
        project_file.close()

    def __load(self, file_path, project_content): 
        # [FERRAMENTA] https://regex101.com/#python
        # Remove o que está entre /* e */
        regex_multiple_comments = '/\*.*\*/'
        project_content = re.sub(regex_multiple_comments, '', project_content, re.S)
        # Remove o que está após //
        regex_comments = '//.*'
        project_content = re.sub(regex_comments, '', project_content)

        # Encontra a lista dos agentes        
        self.agents = []
        
        regex_agents = '\s*agents\s*=\s*\[(.*)\]'
        agents_name = re.findall(regex_agents, project_content, re.S)
        if len(agents_name) > 0:
            # Remove os espaços em branco
            agents_name = re.sub(' ', '', agents_name[0])
            # Cria um array com o nome dos agentes
            agents_name = re.split(',', agents_name)

            for agent_name in agents_name:
                agent_file = '%s/%s.asl'%(file_path, agent_name)
                parser = Parser(agent_name, agent_file)
                self.agents.append(parser.agent)

            # Ordena os agentes
            self.sort(self.agents)

        # Encontra o ambiente
        self.environment = Environment()

        regex_environment = '\s*environment\s*=\s*(\w*)'
        environment_content = re.findall(regex_environment, project_content)
        if len(environment_content) > 0:
            environment_content = environment_content[0]
            # [TO-DO] Carrega o ambiente personalizado        
