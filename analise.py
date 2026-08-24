import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('')

# --análise 1: Filmes mais alugados

query_filmes = """
select f.film_id, f.title, count(r.rental_id) as quantidade_alugueis
from film f
join inventory i on f.film_id = i.film_id 
join rental r on i.inventory_id = r.inventory_id 
group by f.film_id, f.title 
order by quantidade_alugueis desc
limit 10;
"""

df_filmes = pd.read_sql(query_filmes, engine)

plt.figure(figsize=(10, 6))
barras = plt.bar(df_filmes['title'], df_filmes['quantidade_alugueis'])

# adiciona a quantidade exata de aluguéis acima da barra
for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, altura + 0.3, int(altura), ha='center', va='bottom')
    
plt.xlabel('Título do Filme')
plt.ylabel('Quantidade de Aluguéis')
plt.title('Top 10 Filmes Mais Alugados')
plt.xticks(rotation=45, ha='right')  
plt.tight_layout()      
plt.savefig('filmes_mais_alugados.png')
plt.show()

# --Análise 2: Gastos agregados por cliente 

query_gastos = """
select p.customer_id, c.first_name, c.last_name, SUM(amount) as total_gasto
from payment p
join customer c on p.customer_id = c.customer_id
group by p.customer_id, c.first_name, c.last_name
order by total_gasto desc
limit 10;
"""

df_gastos = pd.read_sql(query_gastos, engine)

df_gastos['nome_completo'] = df_gastos['first_name'] + ' ' + df_gastos['last_name']

plt.figure(figsize=(12, 8))
barras = plt.bar(df_gastos['nome_completo'], df_gastos['total_gasto'])

for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, altura + 0.3, round(altura, 2), ha='center', va='bottom')

plt.xlabel('Cliente')
plt.ylabel('Total Gasto (US$)')
plt.title('Top 10 Clientes com Maiores Gastos Agregados')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('gastos_agregados_por_cliente.png')
plt.show()

# -- Análise 3: Aluguéis por região 

query_regiao = """
select cy.country, count(r.rental_id) as qtd_alugueis_regiao
from rental r
join customer c on r.customer_id = c.customer_id
join address a on c.address_id = a.address_id
join city ct on a.city_id = ct.city_id 
join country cy on ct.country_id = cy.country_id 
group by cy.country
order by qtd_alugueis_regiao desc
limit 15;
"""

df_regiao = pd.read_sql(query_regiao, engine)

plt.figure(figsize=(12, 8))
barras = plt.bar(df_regiao['country'], df_regiao['qtd_alugueis_regiao'])

for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, altura + 0.3, int(altura), ha='center', va='bottom')

plt.xlabel('País')
plt.ylabel('Quantidade de Aluguéis')
plt.title('Top 15 Países com Mais Aluguéis')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('regiao_do_aluguel.png')
plt.show()

# --análise 4: Aluguéis por categoria do filme

query_categoria = """
select cg.name, count(r.rental_id) as qtd_alugueis_categoria
from category cg
join film_category fc on cg.category_id = fc.category_id 
join film f on fc.film_id = f.film_id
join inventory i on f.film_id = i.film_id 
join rental r on i.inventory_id = r.inventory_id
group by cg.name
order by qtd_alugueis_categoria desc;
"""

df_categoria = pd.read_sql(query_categoria, engine)

plt.figure(figsize=(12, 8))
barras = plt.bar(df_categoria['name'], df_categoria['qtd_alugueis_categoria'])

for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, altura + 0.3, int(altura), ha='center', va='bottom')

plt.xlabel('Categoria')
plt.ylabel('Quantidade de Aluguéis por Categoria')
plt.title('Categorias Mais Alugadas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('categoria_do_filme.png')
plt.show()

