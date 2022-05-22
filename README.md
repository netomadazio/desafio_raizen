<h1 align="center"> Desafio Raízen </h1>

## Repositório destinado a construção do exercício proposto, como forma de avaliação da empresa Raízen

<h4 align="center"> 
	🚧  Raízen Project 🚀 Concluído com pontos de melhorias..  🚧
</h4>

## Índice 

* [Título](#Título)
* [Índice](#índice)
* [Descrição do Projeto](#descrição-do-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Resolução](#resolução)
* [Pontos de melhorias](#Pontos-de-melhorias)
* [Execução](#Execução)
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

## :hammer: Tecnologias utilizadas

- `Github`: Ferramenta utilizada para versionamento do projeto e repositório; 
- `Python`: Linguagem para manipulação dos arquivos e dados necessários;
- `Docker`: Responsável por criar a imagem necessária para processamento da aplicação;
- `Docker-compose`: Realiza a orquestração dos contêiners;
- `Airflow`: Organiza o fluxo de trabalho;

## Resolução

O primeiro desafio encontrado, foi como realizar a extração dos dados da "raw_data"(nossa base de dados brutos), visto que não era possível em seu formato encontrado. Através de algumas pesquisas pode-se descobrir que fazendo a conversão da tabela do formato "xls" para "xlsx" poderíamos enfim extrair as tabelas necessárias para posterior manipulação dos arquivos, sendo criado dois arquivos distintos xlsx, "oil_deritavite.xlsx" e "diesel.xlsx".
Fez-se então a leitura desses dois arquivos, adicionando-os em dataframe's para que fosse possível fazer as manipulações dos dados necessárias(ressaltando que o processo foi realizado em duas etapas, primeiro a leitura e processamento de um arquivo e posteriormente do outro). Após realizar-se as tratativas necessárias e os dados estarem no formato solicitado, verificou-se a consistência desses dados em relação a "raw_data", concluindo que o processo foi realizado de forma correta, então optou-se por gravar esses dados em formato de parquet, sendo particionado por "product" e "year_month", concluido dessa forma a primeira parte do desenvolvimento.

O segundo passo no desenvolvimento do projeto, foi em qual plataforma fazer o gereciamento do fluxo de trabalho e como isso seria realizado. Levantados esses pontos, optou-se pela utilização da ferramenta "Airflow", sendo utilizada através do docker-compose pela praticidade que isso traria ao desenvolvimento da solução, assim como também para execução. A plataforma do airflow foi iniciada através de uma imagem criada dentro de um arquivo .yaml do docker-compose, sendo também criado um Dockerfile para instalação das configurações necessárias para execução da aplicação conteinerizada. 
No ambiente de desenvolvimento, criou-se as DAG's para orquestração do fluxo de trabalho, sendo estas vistas no ambiente do airflow através do localhost da parta 8080.

## 📁 Execução do projeto 
