#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from parser import *
from environment import *

class Project:

    def __init__(self, file_name):
        project_file = open(file_name, 'r');
        self.__load(os.path.dirname(project_file.name), project_file.read())
        project_file.close()

    def __load(self, file_path, project_content): 
        # [FERRAMENTA] https://regex101.com/#python
        # Remove o que está entre /* e */
        project_content = re.sub('/\*.*\*/', '', project_content, re.S)
        # Remove o que está após //
        project_content = re.sub('//.*', '', project_content)
        # Remove os espaços em branco
        # [FAIL] Não posso por causa das string dentro do .print ou .send
        # project_content = re.sub(' ', '', project_content)

        # Encontra a lista dos agentes        
        self.agents = []
        
        agents_content = re.findall('\s*agents\s*=\s*\[(.*)\]', project_content, re.S)
        if len(agents_content) > 0:
            # Remove os espaços em branco
            agents_content = re.sub(' ', '', agents_content[0])
            # Cria um array com o nome dos agentes
            agents_content = re.split(',', agents_content)

            for agent_content in agents_content:
                agent_content = '%s/%s.asl'%(file_path, agent_content)
                parser = Parser(agent_content)
                self.agents.append(parser.agent)

        # Encontra o ambiente
        self.environment = Environment()

        environment_content = re.findall('\s*environment\s*=\s*(\w*)', project_content)
        if len(environment_content) > 0:
            environment_content = environment_content[0]
            # Carrega o ambiente personalizado        
