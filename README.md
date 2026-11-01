# Diversidade produtiva e ocupacional nos territórios brasileiros (2025)

**Material científico preliminar, não oficial.** Análise exploratória nacional preparada no contexto da pesquisa e do Atlas Territorial do [Crieatividade.org](https://crieatividade.org/). Versão de preparação G3B, 1º de novembro de 2026.

**Pergunta:** em que medida a diversidade de atividades econômicas está associada à diversidade ocupacional das unidades territoriais brasileiras, considerando porte do emprego formal e UF?

## Dados e escopo

- `dados/m.csv`: extração agregada municipal disponibilizada pelo autor, 5.571 unidades territoriais e 13 colunas, sem microdados de trabalhadores ou identificadores pessoais.
- `dados/base_analitica_2025.csv`: transformação da extração com variáveis derivadas; gerada pelo script de análise.
- Origem registrada no Crie: release `2`, `rais_2025_br_aggregate_v1`, metodologia `CRIE.RAIS.NATIONAL.04A`, contrato interno `CRIE.RAIS.NATIONAL.04A2.GUARD.V2`.
- Classificações: CNAE (divisões de atividades) e CBO (subgrupos principais de ocupações). Shannon e HHI medem a distribuição dos **vínculos formais classificados**.

**Ressalva crítica:** a extração do Crie soma 60.688.704 vínculos, mas o sumário executivo oficial do MTE registra 59.970.945 vínculos ativos em 31/12/2025. A diferença de 717.759 **não foi reconciliada**; os resultados não devem ser interpretados como validação externa do universo RAIS. Os arquivos oficiais de origem e o procedimento integral de importação não estão neste repositório.

## Como reproduzir

Pré-requisito: Python 3 com ambiente virtual.

```bash
python -m pip install -r requirements.txt
python codigo/CRIE_analise_diversidade_2025.py --input dados/m.csv --output saida_reproduzida
python codigo/verificar_reproducao.py
```

O script calcula estatísticas, regressões, figuras e `saida_reproduzida/base_analitica_2025.csv`. O verificador testa hashes e resultados de referência. **A verificação do pacote não implica reconciliação com microdados do MTE.**

## Resultados exploratórios

- Pearson entre Shannon produtivo e ocupacional: **0,760**; Spearman: **0,789**.
- Correlação parcial controlando log de emprego formal e UF: **0,565**.
- Pearson com entropias normalizadas pelo logaritmo das categorias presentes: **0,478** (n=5.570).
- Auditoria SQL dentro do banco: **11.142** combinações domínio × território, com Shannon e HHI reproduzidos dentro da tolerância `1e-5`. **Essa auditoria não é integralmente reproduzível a partir deste pacote**, porque as matrizes de células CNAE/CBO não foram incluídas; o resultado é documentado em `metodologia/CRIE_G2D_Auditoria_Nacional_2025_v01.md`.

As associações não são causais. Estes índices não medem diretamente competências ou capacidades individuais. O uso da RAIS não cobre o emprego informal.

## Organização

- `dados/`: extração original agregada e matriz processada.
- `codigo/`: script científico e verificação de reprodutibilidade.
- `figuras/`: três figuras.
- `resultados/`: resultados completos em JSON.
- `metodologia/`: auditoria nacional, proveniência, limitações e referências.
- `SHA256SUMS.json`: integridade dos principais arquivos.

## Fonte oficial e citação

Ministério do Trabalho e Emprego (MTE), **RAIS, ano-base 2025**. Página de divulgação: https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais/rais-2025 . A fonte oficial publica os dados para consulta estatística, mas a proveniência exata deste conjunto derivado e a possibilidade de redistribuição precisam ser verificadas pelo depositante.

Autor da análise e da extração do Crie: Thiago Santos da Silva. Foram utilizadas ferramentas de IA generativa para assistência na programação, redação e organização do protocolo, com revisão humana necessária antes de submissão.

## Direitos e status

**Não atribuir automaticamente uma licença ao conjunto de dados de terceiros.** Uma licença de código-fonte para este script original (por exemplo MIT) e uma licença de documentação (por exemplo CC BY 4.0) dependem da decisão do autor. A ausência de licença explícita restringe direitos de reutilização pelos terceiros; o código continua acessível para inspeção pública se o repositório for público. O material foi preparado, mas **não foi publicado automaticamente**.
