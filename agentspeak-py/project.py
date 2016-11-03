#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import imp
from environment import *
from mas import *
from parser_agent import *

class Project(Mas):
    def __init__(self, file):
        project_file = open(file, 'r');
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
        if agents_name:
            # Remove os espaços em branco
            agents_name = re.sub(' ', '', agents_name[0])
            # Cria um array com o nome dos agentes
            agents_name = re.split(',', agents_name)

            for agent_name in agents_name:
                position_hashtag = agent_name.find('#')
                if position_hashtag >= 0:
                    number_instances = int(agent_name[position_hashtag+1:])
                    agent_name = agent_name[:position_hashtag]
                    agent_file = '%s/%s.asl' % (file_path, agent_name)
                                    
                    for i in range(1, number_instances+1):
                        instance_name = '%s%s' % (agent_name, i)
                        parser = ParserAgent(instance_name, agent_file)
                        self.agents.append(parser.agent)
                else:
                    agent_file = '%s/%s.asl' % (file_path, agent_name)
                    parser = ParserAgent(agent_name, agent_file)
                    self.agents.append(parser.agent)

            # Ordena os agentes
            self.sort(self.agents)

        # Encontra o ambiente
        self.environment = Environment()

        regex_environment = '\s*environment\s*=\s*(\w*)'
        environment_content = re.findall(regex_environment, project_content)
        if environment_content:
            environment_content = environment_content[0]
            # Carrega o ambiente personalizado
            environment_file = '%s/%s.py' % (file_path, environment_content)
            module = imp.load_source(environment_content, environment_file)
            EnvironmentClass = getattr(module, environment_content)
            self.environment = EnvironmentClass()    

