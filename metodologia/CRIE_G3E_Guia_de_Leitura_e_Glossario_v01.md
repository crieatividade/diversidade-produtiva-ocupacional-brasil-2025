# Guia de leitura e glossário do estudo de diversidade produtiva e ocupacional, Brasil 2025

**Material educativo complementar ao artigo de pesquisa e ao Atlas Territorial do Crieatividade.org.** Preparado em 1º de novembro de 2026. Guia complementar preparado para disponibilização pública, sujeito a revisão editorial e científica.

## 1. O que este estudo procura compreender?

A pergunta central é: **territórios que distribuem seus empregos entre mais atividades econômicas, e de modo menos concentrado, também apresentam uma distribuição mais diversa de ocupações?**

- **Atividade econômica:** o que um estabelecimento faz. Exemplo: fabricação de roupas, serviços de informática ou comércio de alimentos.
- **Ocupação:** que tipo de trabalho uma pessoa exerce. Exemplo: costureiro, programador, vendedor ou auxiliar administrativo.
- **Por que comparar?** Uma única atividade pode empregar várias ocupações; a mesma ocupação pode existir em muitas atividades. As duas distribuições não são equivalentes.

A análise é uma fotografia do **emprego formal em 2025**, segundo os agregados territoriais identificados como RAIS 2025 no Crie. Ela não acompanha a trajetória das pessoas, não contempla todo o trabalho informal e não mede diretamente habilidades ou conhecimento individual.

## 2. Siglas, nomes e classificações

| Termo | Significado | Para que serve neste estudo? |
|---|---|---|
| RAIS | **Relação Anual de Informações Sociais**. Registro administrativo brasileiro do mercado de trabalho formal, gerido pelo Ministério do Trabalho e Emprego. | Fonte de vínculos de emprego formal. |
| MTE | **Ministério do Trabalho e Emprego**. | Órgão responsável pela fonte administrativa RAIS e suas divulgações. |
| IBGE | **Instituto Brasileiro de Geografia e Estatística**. | Padrão de códigos e identificação das unidades territoriais. |
| UF | **Unidade da Federação**, incluindo estados e Distrito Federal. | Permite controlar diferenças médias estaduais. |
| CNAE | **Classificação Nacional de Atividades Econômicas**. | Agrupa vínculos pelo ramo da atividade do estabelecimento; a análise usa o nível **divisão**. |
| CBO | **Classificação Brasileira de Ocupações**. | Agrupa vínculos pelo tipo de trabalho exercido; a análise usa o **subgrupo principal**. |
| ISIC | **International Standard Industrial Classification**, classificação internacional de atividades econômicas, coordenada pelas Nações Unidas. | Referência futura para harmonização entre países. |
| ISCO | **International Standard Classification of Occupations**, classificação internacional de ocupações, coordenada pela OIT. | Referência futura para harmonização entre países. |
| QL | **Quociente locacional**, medida de especialização relativa a uma área de comparação. | Pertence ao conjunto mais amplo de análises do Atlas, mas não é o objeto central deste artigo. |
| HHI | **Herfindahl-Hirschman Index**, índice de concentração. | Mede quanto o emprego está concentrado em categorias. |
| CSV | Arquivo de valores separados por delimitadores. | Forma simples de disponibilizar a tabela de entrada para outros pesquisadores. |
| SQL | **Structured Query Language**, linguagem de consultas a bancos de dados. | Usada para recalcular os índices armazenados diretamente das contagens de empregos classificados. |
| Python | Linguagem de programação. | Usada para reproduzir os cálculos, modelos e figuras fora do Crie. |
| SHA-256 | Algoritmo que produz uma assinatura digital de 256 bits para determinado arquivo. | Ajuda a detectar se o arquivo analisado foi modificado; não valida, sozinho, a fonte de origem. |
| Release | Versão identificada de um conjunto de dados. | Distingue a base nacional utilizada de outras importações ou revisões. |

**Atenção:** vínculo de emprego não equivale necessariamente a trabalhador único. Uma mesma pessoa pode ter mais de um vínculo. E dados de trabalho formal não descrevem todo o mercado de trabalho.

## 3. Como calculamos a participação de cada categoria?

Para um território com 100 empregos **classificados** entre duas atividades:

- Atividade A: 50 empregos. Participação = 50/100 = **0,50**, ou 50%.
- Atividade B: 50 empregos. Participação = 50/100 = **0,50**, ou 50%.

Chamamos essa participação de **p**. Todos os *p* da mesma distribuição somam 1 (100%). O denominador é o total de vínculos classificados naquele domínio e nível, que pode ser ligeiramente menor do que o estoque geral de empregos do território.

## 4. O que é o índice de Shannon?

A **entropia de Shannon** resume a distribuição das participações entre as categorias. Sua fórmula é:

**H = −Σ pᵢ × ln(pᵢ)**

- **H:** índice de Shannon do território naquela classificação.
- **Σ:** somatório, isto é, somar o resultado calculado para todas as categorias presentes.
- **pᵢ:** participação do emprego na categoria *i*.
- **ln:** logaritmo natural, uma transformação matemática das proporções.
- **i:** identificação de cada categoria (atividade CNAE ou ocupação CBO).

Com **duas atividades** igualmente distribuídas, 50%/50%:

H = −[0,50 × ln(0,50) + 0,50 × ln(0,50)] ≈ **0,693**.

Com as mesmas duas atividades, mas 90%/10%:

H = −[0,90 × ln(0,90) + 0,10 × ln(0,10)] ≈ **0,325**.

**Como interpretar:** para um mesmo número de categorias, uma distribuição mais equilibrada gera Shannon maior. Shannon também depende do número de categorias existentes. Seu mínimo é 0, quando todo o emprego está em uma única categoria, e seu máximo é ln(K), quando as K categorias presentes têm participações iguais.

**O que não significa:** Shannon elevado não prova que um município é mais rico, mais inovador, que seus trabalhadores têm melhores habilidades ou que possui maior complexidade econômica.

## 5. O que é o HHI?

O **Índice de Herfindahl-Hirschman** mede concentração. Sua fórmula, usando participações entre 0 e 1, é:

**HHI = Σ pᵢ²**

- **HHI:** concentração do emprego entre categorias no território.
- **pᵢ²:** a participação da categoria *i* multiplicada por ela mesma.
- **Σ:** soma desses quadrados para todas as categorias.

Nas duas situações anteriores:

- **50%/50%:** HHI = 0,50² + 0,50² = **0,50**.
- **90%/10%:** HHI = 0,90² + 0,10² = **0,82**.

**Como interpretar:** quanto maior o HHI, mais concentrado é o emprego. O valor máximo é 1; o mínimo, com K categorias igualmente distribuídas, é 1/K. O HHI é definido para cada classificação separadamente. Em outros usos econômicos, o índice pode ser apresentado numa escala de 0 a 10.000; este estudo usa proporções de 0 a 1.

**Shannon e HHI não se contradizem:** no município 90%/10%, Shannon diminui (menor diversidade) e HHI aumenta (maior concentração). São formas diferentes de resumir a distribuição.

## 6. E o número de atividades e ocupações?

A **variedade** é simplesmente quantas categorias aparecem com pelo menos um emprego. Por exemplo, dez divisões CNAE presentes significam variedade produtiva 10. Porém, dez atividades com distribuição 10%/10%/.../10% são diferentes de dez atividades com 91% do emprego em uma única atividade. Por isso, variedade e equilíbrio precisam ser distinguidos.

A **equitabilidade** usada no artigo é **H / ln(K)**, para K maior que 1. Essa medida varia de 0 a 1 e responde quanto a distribuição se aproxima do equilíbrio **entre as categorias que estão presentes**. Não é a mesma medida de Shannon bruto, nem resolve todas as diferenças de classificação entre países.

A transformação **exp(H)** representa o número de categorias igualmente frequentes que produziria a mesma entropia observada. É útil para interpretação dentro da mesma classificação e mesmo universo, não para equiparar diretamente o significado de divisões CNAE e subgrupos CBO.

## 7. Como ler os resultados estatísticos?

| Termo | Interpretação correta |
|---|---|
| Correlação de Pearson | Associação linear entre duas medidas. Vai de −1 (inversa perfeita) a +1 (direta perfeita), com 0 indicando ausência de associação linear. |
| Correlação de Spearman | Associação entre as posições ordenadas (ranks) das unidades, sem exigir relação linear direta. |
| Correlação parcial | Associação após retirar, por um procedimento estatístico, a variação linear associada às variáveis de controle. Não assegura ausência de fatores omitidos. |
| Regressão | Modelo estatístico que descreve como uma medida se associa a outras, condicionalmente aos controles especificados. |
| Variável de controle | Característica adicional considerada na análise, como tamanho do emprego formal e UF. |
| Efeito fixo de UF | Ajuste para diferenças médias entre as unidades federativas incluídas no modelo. Não elimina todas as diferenças entre municípios. |
| Logaritmo do emprego | Transformação matemática que reduz a escala de valores muito desiguais entre municípios. |
| Termo quadrático | Quadrado do logaritmo, permitindo que a relação estimada com o porte não seja uma reta simples. |
| Coeficiente β | Intensidade da associação estimada para a variável de interesse, conforme a equação e seus controles. |
| R² | Medida do ajuste conjunto do modelo aos valores observados; não indica causalidade nem contribuição exclusiva de um indicador. |
| Resíduo | Diferença entre o valor observado e o valor estimado pela regressão. Um resíduo elevado não é prova automática de sucesso ou problema territorial. |
| Erro-padrão/intervalo de confiança | Medidas de incerteza sob hipóteses do modelo; não provam que os registros de origem estão corretos. |
| Robustez | Verificação de como resultados variam diante de escolhas alternativas de indicadores, filtros ou especificações. |

**Resultados documentados no estudo:** Pearson entre Shannon produtivo e ocupacional ≈ **0,760**; Spearman ≈ **0,789**; correlação parcial por log do emprego e UF ≈ **0,565**; correlação entre equitabilidades ≈ **0,478**. Esses números **não são percentuais**, não representam aumento do emprego e não demonstram causa e efeito.

## 8. O que foi auditado e o que permanece pendente?

**Confirmado nos dados do Crie:**

1. A exportação utilizada contém 5.571 códigos territoriais distintos.
2. As somas de empregos classificados pelas duas distribuições coincidiram com seus totais de nível em 11.142 verificações.
3. Os índices Shannon e HHI armazenados coincidiram com seus recálculos a partir dos agregados, em 22.284 comparações numéricas, dentro da tolerância de 0,00001.
4. O programa Python reproduz os resultados estatísticos e figuras a partir da extração CSV disponibilizada.

**Não demonstrado:**

1. Reconstituição independente da importação a partir dos **arquivos oficiais exatos** que originaram os três agregados canônicos do Crie.
2. Reconciliação entre 60.688.704 vínculos do release interno e 59.970.945 vínculos informados no sumário executivo do MTE; a diferença de 717.759 permanece em investigação.
3. Comparabilidade internacional já validada, ou medida direta de conhecimentos, habilidades, mecanismos de aprendizagem e resultados distributivos.

A confirmação matemática não deve aparecer como “todos os dados validados” sem essas ressalvas.

## 9. Como o leitor pode reproduzir o exercício?

Com Python 3 instalado, a partir da raiz do repositório científico:

```bash
python -m pip install -r requirements.txt
python codigo/CRIE_analise_diversidade_2025.py --input dados/m.csv --output saida_reproduzida
python codigo/verificar_reproducao.py
```

O material externo permite refazer as análises a partir do CSV. A auditoria completa das células CNAE/CBO foi realizada no banco de origem; suas matrizes detalhadas não estão incluídas no pacote público preliminar.

## 10. Onde consultar as definições oficiais e os fundamentos científicos?

- MTE, **RAIS**: https://www.gov.br/pt-br/servicos/entregar-a-relacao-anual-de-informacoes-sociais
- IBGE/CONCLA, **CNAE 2.0**: https://cnae.ibge.gov.br/classificacoes/por-tema/atividades-economicas/classificacao-nacional-de-atividades-economicas.html
- MTE, **CBO**: https://www.gov.br/trabalho-e-emprego/pt-br/servicos/trabalhador/mais-acoes/classificacao-brasileira-de-ocupacoes
- Guevara, Hartmann e Mendoza (2016), **diverse: an R Package to Analyze Diversity in Complex Systems**: https://journal.r-project.org/articles/RJ-2016-033/
- Stirling (2007), **A general framework for analysing diversity in science, technology and society**: DOI 10.1098/rsif.2007.0213

**Uso responsável:** este guia oferece explicações simplificadas. Para replicação e citações acadêmicas, consulte também o artigo, os registros de método, o script, a documentação do release e as fontes oficiais. Não usar os índices como rankings automáticos de qualidade de pessoas, profissões ou municípios.
