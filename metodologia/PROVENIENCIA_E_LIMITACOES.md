# Proveniência e status de validação | G3A

**Data do registro:** 01/11/2026. **Release:** 2. **Ano de referência:** 2025.

| Critério | Evidência | Estado |
| --- | --- | --- |
| Identificação da fonte | Registro `geoeco_dataset_release` indica RAIS/MTE 2025; fonte URL genérica | Identificado internamente |
| Versão técnica | `rais_2025_br_aggregate_v1`; `CRIE.RAIS.NATIONAL.04A` | Registrado |
| Contrato canônico | `CRIE.RAIS.NATIONAL.04A2.GUARD.V2`, `canonical_contract_checked = true` | Verificado internamente |
| Política de não identificados | `excluded_from_municipal_matrices` | Registrada |
| Estoque do CSV | 60.688.704 | Conciliado com registro interno |
| Totais de atividades CNAE | 60.684.209 (5 níveis iguais) | Conciliado internamente |
| Totais de ocupações CBO | 60.631.703 (5 níveis iguais) | Conciliado internamente |
| Reprodução matemática | 5.571 CNAE + 5.571 CBO; índices HHI/Shannon | Aprovado, 0 divergências na tolerância 1e-5 |
| Fonte oficial MTE | 59.970.945 vínculos em 31/12/2025 | **Diferença 717.759 não explicada** |
| Arquivo original oficial, filtros e revisões | Não integra este pacote | Pendente de reconciliação |
| Validação internacional | Nenhuma aplicação externa | Não realizada |

A auditoria SQL sobre células CNAE/CBO ocorreu no banco do Crie e foi comunicada com resultados agregados. As células originais **não foram exportadas para este repositório**. Assim, usuários externos podem reproduzir as estatísticas do CSV, mas não refazer a reconciliação do importador com microdados oficiais nem a auditoria de cada célula com os arquivos aqui presentes.

Referência oficial do MTE: *Sumário Executivo RAIS 2025* (maio de 2026), https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais/rais-2025/SumrioExecutivo_RAIS20251.pdf .
