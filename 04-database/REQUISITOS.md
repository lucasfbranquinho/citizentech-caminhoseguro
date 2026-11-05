# Database Design

Modelo Relacional/Lógico (tabelas, atributos, PKs, FKs, relacionamentos) e implementação física.

## Entregáveis (pontos)
1. Apresentação (10): capa com integrantes em **ordem alfabética**, RM, nome da equipe e nome da
   solução; sumário; objetivo e escopo; breve descrição das funcionalidades.
2. Diagrama do Modelo Lógico no **Oracle Data Modeler** (20): todas as tabelas, atributos, PKs, FKs,
   relacionamentos e cardinalidades.
3. Script DDL (20): CREATE TABLE / ALTER TABLE, completo com todas as constraints.
4. Script DML (20): INSERTs com **no mínimo 5 linhas por tabela** (exceção só se justificada).
5. Script DQL (30), três consultas:
   - 10: duas tabelas com INNER JOIN
   - 10: duas tabelas com INNER JOIN + função de grupo + GROUP BY
   - 10: duas tabelas com LEFT OUTER JOIN + WHERE + ORDER BY

## Formato
Itens 1 e 2 no PDF. Itens 3 a 5 em arquivos texto `.sql`. **Não incluir links para diagramas em nuvem.**

## Ligação com DDD Java
As mesmas tabelas servem para a API do 05-ddd-java (banco Oracle da FIAP). Modelar pensando nas duas.
