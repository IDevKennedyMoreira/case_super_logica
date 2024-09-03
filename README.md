🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰

Pipeline de dados do case de projeto para a empresa CondoManage

Atenção: Respostas das questões de encontram abaixo do manual de instalação desse mesmo arquivo!

Para a correta execução desse projeto devemos nos atentar a instalação de dependências:

OBS! Todo o projeto foi criado usando sitema operacional MAC a depender do seu sistema operacional
diferentes passos devem ser tomados para a devida instalação do projeto, aqui estarei disponibilizando
apenas o passo a passo para o MAC e sistemas similares baseados em unix exceto pelo gerenciador de pacotes
que estou utilizando o brew

1. Garantir a instalação do java

   brew install openjdk@11

2. Garantir instalação do spark

   brew install apache-spark

3. Instalar python

   brew install python3

   Neste projeto foi usada a versão Python 3.10.11 usar essa ou maior

4. Instalar o virtualenv na máquina local

   pip install virtualenv

5. Abrir projeto e iniciar o ambiente virtual

   source env/bin/activate

6. Instalar requirements

   pip install -r requirements.txt

7. Definir variável de ambiente do airflow

   export AIRFLOW_HOME=~/Desktop/case_super_logica

8. Para executar o projeto em modo local sem airflow via terminal

   cd dags;python3 superlogica_data_pipeline_local.py

   OBS! o motivo de rodar a partir da pasta de dags é que no início do projeto
   não pensei que teria problemas em rodar a pipe com o airflow com scripts de
   execução paralela em modo local, porém após consultar a documentação vi essa restrição
   mas o projeto já estava todo montado a partir desse ponto de montagem

9. Para executar o projeto em modo local usando o airflow

   airflow standalone logue com admin e senha presente no arquivo
   standalone_admin_password

   OBS! você não conseguirá rodar scripts em paralelo como o presente em nossa DAG
   sem instalar um banco de dados local e alterar o airflow.cgf para sua configuração
   de banco escolhida devido a esse trabalho recomendo fortemente o uso da execução via
   terminal presente no passo 8

-> RESPOSTAS

Questão 1.

A arquitetura de datalake escolhida para a criação dessa projeto foi a medalhão
aqui temos:

camada landing apenas recebendo os arquivos csv para processamento

camada raw apenas transforma os arquivos da camada landing em formato parquet

camada refined aplica regras de negócio e gera a OBT (One Big Table) modalagem escolhida
por mim para este projeto

camada trusted é uma cópia da camada refined com dados prontos para análise

Questão 2.

A ingestão de dados desse projeto foi criada a partir de uma simulação da criação de
arquivos csv a classe responsavel por isso é a DataGenerator presente no arquivo
dags/models/datagenerator.py ela é orquestrada a partir de dags/landing_read_data_from_external.py
e por sua vez os dados entram na camada raw através de dags/raw_read_data_from_landing.py
a explicação de como cada arquivo funciona está em seus comentários internos.

Questão 3.

Questão 4.

Vide comentários internos do arquivo dags/raw_streaming_read_data_from_landing_townhouse.py
lá é feita a primeira parte da ingestão usando streaming a pipelie exposta na DAG e no arquivo
dags/superlogica_data_pipeline_local.py é do tipo batching

Questão 5.

Para definicão de documentação usaria um repositório de documentação como o confluence e também
geraria comentário seguindo a PEP8 e com a ferramenta mkdocs conseguiria fazer a documentação automática
a partir dos cometários nos jobs.
