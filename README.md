<h1 align="center"> Desafio Raízen </h1>

## Repositório destinado a construção do exercício proposto, como forma de avaliação da empresa Raízen

<h4 align="center"> 
	🚧  Raízen Project 🚀 Concluído com pontos de melhorias..  🚧
</h4>

## Índice 

* [Título](#título)
* [Índice](#índice)
* [Descrição do Projeto](#descrição-do-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Resolução](#resolução)
* [Pontos de melhorias](#pontos-de-melhorias)
* [Execução do projeto](#execução-do-projeto)
* [Conclusão](#conclusão)

## Descrição do Projeto

O projeto tem por objetivo, a resolução de um atividade proposta pela empresa Raízen, que consiste no desenvolvimento de uma pipeline ETL para extrair caches de pivô de relatórios consolidados, disponibilizados pela agência reguladora de petróleo/combustíveis do governo brasileiro, ANP(Agência Nacional de Petróleo, Gás Natural e Biocombustíveis).
O arquivo em questão possuem algumas pivot tables, onde é necessária a extração e manipulação de duas dessas tabelas:
- Vendas de combustíveis derivados de petróleo por UF e produto;
- Vendas de diesel por UF e tipo;

Os dados devem ser armazenados nos formatos a seguir

| Column       | Type        |
| ------------ | ----------- |
| `year_month` | `date`      |
| `uf`         | `string`    |
| `product`    | `string`    |
| `unit`       | `string`    |
| `volume`     | `double`    |
| `created_at` | `timestamp` |

Posteriormente definindo um schema de particionamento ou indexação.

Obs: (Parte da descrição retirada do próprio arquivo da atividade).

## Tecnologias utilizadas 
:hammer:

- `Github`: Ferramenta utilizada para versionamento do projeto e repositório; 
- `Python`: Linguagem para manipulação dos arquivos e dados necessários;
- `Docker`: Responsável por criar a imagem necessária para processamento da aplicação;
- `Docker-compose`: Realiza a orquestração dos contêiners;
- `Airflow`: Organiza o fluxo de trabalho;

## Resolução

O primeiro desafio encontrado, foi como realizar a extração dos dados da "raw_data"(base de dados brutos), visto que não era possível em seu formato encontrado. Através de algumas pesquisas, pode-se descobrir que fazendo a conversão da tabela do formato "xls" para "xlsx" poderia-se enfim extrair as tabelas necessárias para posterior manipulação dos arquivos, sendo assim criado dois arquivos distintos xlsx, "oil_deritavite.xlsx" e "diesel.xlsx".
Fez-se então a leitura desses arquivos, adicionando-os em dataframe's para que fosse possível fazer as manipulações dos dados necessárias(ressaltando que o processo foi realizado em duas etapas, primeiro a leitura e processamento de um arquivo e posteriormente do outro). Após realizar-se as tratativas necessárias e os dados estarem nos formatos solicitados, verificou-se a consistência desses dados em relação a "raw_data", concluindo que o processo foi realizado de forma correta, então optou-se por gravar esses dados em formato de parquet, sendo particionado por "product" e "year_month", concluido dessa forma a primeira parte do desenvolvimento.

O segundo passo no desenvolvimento do projeto, foi em qual plataforma fazer o gereciamento do fluxo de trabalho e como isso seria realizado. Levantados esses pontos, optou-se pela utilização da ferramenta "Airflow", sendo utilizada através do docker-compose pela praticidade que isso traria ao desenvolvimento da solução, assim como também para execução. A plataforma do airflow foi iniciada através de uma imagem criada dentro de um arquivo .yaml do docker-compose, sendo também criado um Dockerfile para instalação das configurações necessárias para execução da aplicação conteinerizada. 
No ambiente de desenvolvimento, criou-se as DAG's para orquestração do fluxo de trabalho, sendo estas vistas no ambiente do airflow através do localhost da porta 8080.
Com isso conclui-se a etapa de controle do fluxo de trabalho através de um ambiente conteinerizado.

## Pontos de melhorias

Existem alguns pontos que poderiam vir a ser melhorados no desenvolvimento do projeto, dentre eles podemos citar uma melhor performance no fluxo de trabalho, principalmete na etapa de extração dos dados das duas tabelas solicitadas, utilizou-se de "ferramentas" não tão performáticas no processo, sendo possível uma melhor pesquisa por outras formas de se processar essa tarefa.
Outro ponto que vale ressaltar, seria alocação desses dados processados em um banco de dados para consultas, sendo possível também um backup para evitar o reprocesso, como em um ambiente produtivo é default a replicação por três(3) no HDFS.

## Execução do projeto 
📁 

É possível realizar a execução do projeto de duas formas distintas, podendo elas serem realizadas no ambiente local ou em um ambiente conteinerizado.
- Para execução local, é necessário clonar o repositório através do comando:

	- git clone https://github.com/netomadazio/desafio_raizen.git

	Posteriormente entrar no diretório "local_excution" e executar o arquivo "ETL_Raizen_local.py":
	- cd local_excution
	- python ETL_Raizen_local.py

	Essa execução irá realizar todo a extração, manipulação e carregamento dos parquet's das tabelas solicitadas localmente.

- Para execução no ambiente conteinerizado deve-se clonar o repositório:

	- git clone https://github.com/netomadazio/desafio_raizen.git

	Subir o conteiner do airflow contendo as dependências do projeto: 
	- docker-compose up airflow-init
	- docker-compose up
	
	Acessar a porta no 8080 através do navegador web:
	- localhost:8080
	
	Então executar o fluxo de trabalho.

## Conclusão

Através do trabalho proposto pode-se desenvolver uma pipeline ETL, utilizando-se de algumas ferramentas disponíveis no mercado, ficando como observação a possibilidade de realizar melhorias nas etapas executadas, construindo um melhor desenvolvimento, execução e entrega.
Agradeço desde já pela oportunidade e sigo a disposição para quaisquer questionamentos.
Muito obrigado, Raízen.

Atenciosamente,

### Autor

Irineu Madazio Neto
Engenheiro de Controle e Automação 
apaixonado pela área de Engenharia de Dados.

[![Linkedin Badge](https://img.shields.io/badge/-Irineu-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/irineu-madazio-neto/)](https://www.linkedin.com/in/irineu-madazio-neto/) 




	



