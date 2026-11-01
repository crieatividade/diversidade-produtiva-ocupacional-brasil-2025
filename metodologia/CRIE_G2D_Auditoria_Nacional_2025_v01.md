# G2D — Auditoria matemática nacional dos índices de diversidade (RAIS 2025)

**Data da verificação:** 1º de novembro de 2026  
**Base:** `crieativ_rea`, release 2, `rais_2025_br_aggregate_v1`, `CRIE.RAIS.NATIONAL.04A`  
**Origem desta evidência:** resultados de consultas SQL de leitura executadas pelo autor no phpMyAdmin e compartilhadas na conversa. Esta ficha registra os resultados informados; não constitui acesso direto independente ao servidor.

## Escopo e método

Foram recalculados o índice Herfindahl-Hirschman, `HHI = Σ(pᵢ²)`, e o índice de Shannon, `H = −Σ(pᵢ ln pᵢ)`, a partir das células do emprego classificado de cada território, separadamente para **divisão CNAE** e **subgrupo principal CBO**. Cada proporção usa como denominador o total de vínculos **classificados naquela dimensão e naquele território**, armazenado em `geoeco_municipality_level_total`.

O recálculo foi comparado aos quatro indicadores persistidos em `geoeco_municipality_summary` com tolerância absoluta de `0,00001` para cada índice. Somaram-se também os empregos classificados por categoria e compararam-se aos totais persistidos no nível correspondente. Essas verificações não são independentes dos agregados carregados no Crie, mas verificam independentemente a fórmula aplicada aos mesmos agregados.

## Resultado nacional

| Tipo | Territórios | Totais reproduzidos | Divergências nos totais | Pares Shannon+HHI reproduzidos | Divergências nos índices | Maior desvio HHI | Maior desvio Shannon |
|---|---:|---:|---:|---:|---:|---:|---:|
| CNAE divisão | 5.571 | 5.571 | 0 | 5.571 | 0 | 0,0000000020 | 0,0000002597 |
| CBO subgrupo principal | 5.571 | 5.571 | 0 | 5.571 | 0 | 0,0000000018 | 0,0000001529 |
| **Total** | **11.142** | **11.142** | **0** | **11.142** | **0** |  |  |

Em termos de comparação individual, foram reproduzidos **22.284 valores de índices** (5.571 territórios × 2 domínios × 2 medidas) dentro da tolerância definida. Não houve discrepâncias nas 11.142 somas de empregos classificados.

## Cobertura interna do release

- Estoque total no sumário do Crie: **60.688.704 vínculos**.
- CNAE, níveis classificados: **60.684.209**; diferença para o estoque: **4.495** (cobertura de aproximadamente **99,9926%**).
- CBO, níveis classificados: **60.631.703**; diferença para o estoque: **57.001** (cobertura de aproximadamente **99,9061%**).
- O percentual de cobertura nacional **não substitui** a análise da cobertura municipal.

## Pendências e limites

1. **Conciliação externa:** o sumário executivo oficial do MTE registra **59.970.945** vínculos ativos em 2025; o release 2 do Crie, **60.688.704**. A diferença de **717.759** vínculos ainda requer esclarecimento de versão, universo, filtros ou agregação. Não atribuir uma causa sem evidência.
2. **Microdados de origem:** o procedimento acima audita as células agregadas presentes no banco, não reconstrói integralmente a base a partir dos microdados RAIS originais.
3. **Interpretação:** Shannon e HHI caracterizam a distribuição do emprego formal entre categorias, não medem automaticamente complexidade, qualidade do emprego, conhecimentos individuais ou capacidades coletivas.
4. **Disponibilidade:** o arquivo processado e o código Python precisam ser depositados em repositório acessível ao professor e identificados no artigo. Não publicar dados pessoais, credenciais ou dumps privados.
5. **Bibliografia:** verificar manualmente as referências citadas e manter a declaração de assistência de IA generativa.

## Recomendação para o Atlas

Exibir separadamente, em ficha metodológica consultável: fonte e versão, população coberta, classificação e granularidade, denominador, fórmula, taxa de cobertura, resultado da auditoria matemática interna e estado da conciliação externa. Não utilizar uma única etiqueta 'verificado' para representar todas essas condições.

**Status G2D:** concluído para consistência matemática interna nacional.  
**Status do release perante a fonte oficial:** reconciliação externa pendente.  
**Status de implantação no Atlas:** nenhuma alteração de código ou banco foi efetuada para esta auditoria.
