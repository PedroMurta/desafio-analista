# Desafio Analista

##### Desafio proposto para Analista de dados 📈

> 1ª Etapa: Instanciar um banco de dados __PostgreSQL__  <img alt="SQL" width="26px" src="https://cdn.jsdelivr.net/npm/simple-icons@3.4.0/icons/postgresql.svg" /> e realizar nele a ingestão dos dados. `Fazer a normalização até a 3ª Forma Normal`
  
> 2ª Etapa: Criar uma consulta __*SQL*__ que retorne a aderência das contas à sua política de investimentos.


> 3ª Etapa: Criar um dashboard para disponibilizar as informações de aderência para o time operacional, e outras informações relevantes.


-----------------------------------------------------------

Sistema Operacional utilizado no desenvolvimento e ferramentas
- Arch Linux 
- Kernel: 6.2.8-arch1-1
- VSCode (Código do dashboard)
- Google Colab (Análise e tratamento dos dados)
- Railway (Deploy do dashboard e hospedagem do Banco de Dados PostgreSQL


------------------------

### Instruções de Instalação

```
- Clone o repositório 

git clone https://github.com/PedroMurta/desafio-analista.git

- Entre na pasta do repositório e crie um arquivo .env
python3 -m virtualenv .env

source .env/bin/activate

- Encontre o arquivo requirements.txt e instale as dependências
pip install -r requirements.txt 

- Execute o arquivo .py
python3 app.py

```



## Resolução: 


- 1ª Etapa:

```
Para instanciar um banco de dados a partir dos arquivos csv e xlsx que foram fornecidos e fazer a ingestão,
foi escolhido a plataforma Railway para hospedar o banco e também o projeto/repositório. os códigos estão 
neste notebook: 

Normalização: A Primeira Forma Normal (1FN) exige que cada atributo de uma tabela possua valores 
atômicos, ou seja, valores que não possam ser divididos em partes menores. Portanto, a tabela Position (arquivo csv)
já está na 1FN. 

Para a Segunda Forma Normal (2FN) e a Terceira Forma Normal é preciso que se remova todas as dependências transitivas
e criar novas tabelas se for necessário. É claro que existem várias formas de transformar as tabelas e a escolha final 
vai depender da necessidade e do contexto. 

> Como foi sugerido no desafio, aqui estão 2 exemplos de formas de 3FN feitos no dbdiagram.io:


```
![alt text](https://github.com/PedroMurta/desafio-analista/blob/main/normalizacao1.png?raw=true)
![alt text](https://github.com/PedroMurta/desafio-analista/blob/main/normalizacao2.png?raw=true)

- 2ª Etapa:

```
A criação da query no SQL para retornar a aderência das contas à política de investimentos também está no notebook: 


Porém, como forma de ter uma melhor visualização da transformação dos dados passo a passo, o foco da busca foi feita com 
python, pandas e streamlit. 

Se houver a preferência por consultas SQL, basta fazer a query equivalente aos comandos do pandas.

No contexto, é possível fazer as consultas com a biblioteca psycopg2 dentro das células do notebook.

```

 
Query SQL:
-   Query
        Select
         p.account_code, 
         p.asset_name, 
         p.asset_cnpj, 
        p.class_name, 
         ((p.position_value - pol.Conservador)^2 + 
        (p.position_value - pol."Moderado Conservador")^2 + 
        (p.position_value - pol.Moderado)^2 + 
        (p.position_value - pol."Moderado Agressivo")^2 + 
        (p.position_value - pol.Agressivo)^2)^0.5 AS aderencia
        FROM position p
        JOIN policy pol ON p.class_name = pol.Classe
        ORDER BY aderencia ASC; 
 


[Notebook](https://github.com/PedroMurta/desafio-analista/blob/main/Desafio_Analista.ipynb).


- 3ª Etapa:

```
- A Etapa de criação de dashboards teve a opção de ser desenvolvida em qualquer ferramenta, desde que fosse mostrado no 
documento do projeto.

- Por preferência pessoal, o dashboard desenvolvido com Python, plotly e streamlit está disponível neste link:
```


 [Dashboard com Streamlit](https://pedromurta-desafio-analista-streamlit-app-48ex30.streamlit.app/)
 
 
 [Dashboard com Datapane](https://cloud.datapane.com/reports/R70BGvA/an%C3%A1lises/)
 

 
Há diversas formas e aprimorar e melhorar estas análises e dashboards, podemos melhorar os gráficos com filtros,
melhorar o design da página e deixar os gráficos, aprimorar as análises com mais profundidade e com um melhor entendimento do negócio!

Agradeço a oportunidade de participar do processo e do desafio. 
