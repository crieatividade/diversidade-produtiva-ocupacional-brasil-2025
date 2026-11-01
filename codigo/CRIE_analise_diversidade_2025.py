#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CRIE | RAIS 2025 | Exploratory, reproducible cross-sectional diversity analysis.

Run: python CRIE_analise_diversidade_2025.py --input m.csv --output resultados_crie_2025
Dependencies: numpy, scipy, statsmodels, matplotlib. CSV is handled with Python stdlib.
Analysis is descriptive, not causal. Index-producing system is external and must be audited.
"""
import argparse, csv, hashlib, json, math
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import pearsonr, spearmanr
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

NUM = ('empregos_formais','remuneracao_media','divisoes_produtivas','subgrupos_ocupacionais','productive_hhi','productive_shannon','occupational_hhi','occupational_shannon')
REGIONS={'AC':'Norte','AP':'Norte','AM':'Norte','PA':'Norte','RO':'Norte','RR':'Norte','TO':'Norte',
         'AL':'Nordeste','BA':'Nordeste','CE':'Nordeste','MA':'Nordeste','PB':'Nordeste','PE':'Nordeste','PI':'Nordeste','RN':'Nordeste','SE':'Nordeste',
         'DF':'Centro-Oeste','GO':'Centro-Oeste','MS':'Centro-Oeste','MT':'Centro-Oeste',
         'ES':'Sudeste','MG':'Sudeste','RJ':'Sudeste','SP':'Sudeste',
         'PR':'Sul','RS':'Sul','SC':'Sul'}
def asfloat(v):
    return float(v) if v not in ('NULL','','null','None',None) else float('nan')
def scalar(v):
    if isinstance(v,(np.floating,np.integer)): return v.item()
    if isinstance(v,np.ndarray): return v.tolist()
    return v

def write_csv(path, rows, cols):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',default='m.csv'); p.add_argument('--output',default='resultados_crie_2025'); a=p.parse_args()
    file=Path(a.input); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    rawbytes=file.read_bytes(); sha=hashlib.sha256(rawbytes).hexdigest()
    with open(file,newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    for r in rows:
        for k in NUM: r[k]=asfloat(r[k])
        r['estabelecimentos']=asfloat(r['estabelecimentos'])
        r['regiao']=REGIONS[r['uf']]
        r['ln_empregos']=math.log(r['empregos_formais']) if r['empregos_formais']>0 else float('nan')
        r['equiv_divisoes']=math.exp(r['productive_shannon'])
        r['equiv_ocupacoes']=math.exp(r['occupational_shannon'])
        r['norm_shannon_prod']=r['productive_shannon']/math.log(r['divisoes_produtivas']) if r['divisoes_produtivas']>1 else float('nan')
        r['norm_shannon_ocup']=r['occupational_shannon']/math.log(r['subgrupos_ocupacionais']) if r['subgrupos_ocupacionais']>1 else float('nan')
    n=len(rows)
    def vec(name, subset=rows): return np.array([r[name] for r in subset],dtype=float)
    X=vec('productive_shannon'); Y=vec('occupational_shannon'); size=vec('ln_empregos'); jobs=vec('empregos_formais')
    states=sorted(set(r['uf'] for r in rows)); dummies=np.array([[1. if r['uf']==u else 0. for u in states[1:]] for r in rows])
    controls=sm.add_constant(np.column_stack([size,dummies]))
    rx=sm.OLS(X,controls).fit().resid; ry=sm.OLS(Y,controls).fit().resid
    extended=sm.add_constant(np.column_stack([X,size,size**2,dummies]))
    model=sm.OLS(Y,extended).fit(cov_type='HC3')
    clusters=sm.OLS(Y,extended).fit(cov_type='cluster',cov_kwds={'groups':np.array([r['uf'] for r in rows])})
    simplemodel=sm.OLS(Y,sm.add_constant(np.column_stack([X,size,dummies]))).fit(cov_type='HC3')
    resids=Y-model.predict(extended); sdev=float(np.std(resids,ddof=int(model.df_model)+1))
    pear=pearsonr(X,Y); spear=spearmanr(X,Y)
    pcorr=pearsonr(rx,ry)
    # Correlation-based sensitivity by sample size and alternative indicators.
    def corr_on(sel, fx='productive_shannon', fy='occupational_shannon'):
        subset=[r for r in rows if sel(r)]
        if len(subset)<3: return {'n':len(subset),'pearson':None,'spearman':None}
        ax=np.array([r[fx] for r in subset]); ay=np.array([r[fy] for r in subset]); mask=np.isfinite(ax)&np.isfinite(ay)
        if mask.sum()<3: return {'n':int(mask.sum()),'pearson':None,'spearman':None}
        return {'n':int(mask.sum()),'pearson':float(pearsonr(ax[mask],ay[mask]).statistic),'spearman':float(spearmanr(ax[mask],ay[mask]).statistic)}
    checks={
        'missing':{col:sum(not math.isfinite(r[col]) for r in rows) for col in NUM+('estabelecimentos',)},
        'duplicates':n-len(set(r['ibge_code'] for r in rows)),
        'years':sorted(set(r['reference_year'] for r in rows)),
        'uf_count':len(states),
        'hhi_bounds':{k:sum(not (0<=r[k]<=1) for r in rows) for k in ('productive_hhi','occupational_hhi')},
        'shannon_bounds':{k:sum(r[h] < -1e-8 or r[h] > math.log(r[c])+1e-7 for r in rows) for h,c,k in [('productive_shannon','divisoes_produtivas','productive'),('occupational_shannon','subgrupos_ocupacionais','occupational')]},
        'hhi_min_possible':{k:sum(r[h]+1e-8 < 1./r[c] for r in rows) for h,c,k in [('productive_hhi','divisoes_produtivas','productive'),('occupational_hhi','subgrupos_ocupacionais','occupational')]},
        'zero_or_negative_employment':sum(r['empregos_formais']<=0 for r in rows),
        'remuneracao_lt_500':sum(r['remuneracao_media']<500 for r in rows),
    }
    stat={
       'n':n,'raw_sha256':sha,'jobs_total':int(jobs.sum()),'jobs_min':int(jobs.min()),'jobs_max':int(jobs.max()),
       'divisoes_minmax':[int(vec('divisoes_produtivas').min()),int(vec('divisoes_produtivas').max())],
       'ocupacoes_minmax':[int(vec('subgrupos_ocupacionais').min()),int(vec('subgrupos_ocupacionais').max())],
       'medians':{k:float(np.median(vec(k))) for k in ('empregos_formais','divisoes_produtivas','subgrupos_ocupacionais','productive_shannon','occupational_shannon','productive_hhi','occupational_hhi','equiv_divisoes','equiv_ocupacoes')},
       'means':{k:float(np.mean(vec(k))) for k in ('productive_shannon','occupational_shannon','productive_hhi','occupational_hhi')},
       'correlations':{
          'pearson_raw':float(pear.statistic),'pearson_p':float(pear.pvalue),
          'spearman_raw':float(spear.statistic),'spearman_p':float(spear.pvalue),
          'pearson_partial_logjobs_UF':float(pcorr.statistic),
          'pearson_with_logjobs_prod':float(pearsonr(X,size).statistic),
          'pearson_with_logjobs_ocup':float(pearsonr(Y,size).statistic),
          'pearson_hhi':float(pearsonr(vec('productive_hhi'),vec('occupational_hhi')).statistic),
       },
       'regression':{
           'spec':'Shannon_occ ~ Shannon_prod + ln(empregos) + ln(empregos)^2 + UF fixed effects',
           'beta_prod':float(model.params[1]),'se_HC3':float(model.bse[1]),'p_HC3':float(model.pvalues[1]),
           'ci_HC3':model.conf_int()[1].tolist(),'se_cluster_UF':float(clusters.bse[1]),'p_cluster_UF':float(clusters.pvalues[1]),
           'ci_cluster_UF':clusters.conf_int()[1].tolist(),
           'r_squared':float(model.rsquared),'rmse':sdev,
           'beta_prod_linear_logjobs_UF':float(simplemodel.params[1]),'se_linear_HC3':float(simplemodel.bse[1]),
       },
       'checks':checks,
       'robustness':{
         'thresholds':{str(t):corr_on(lambda r,t=t:r['empregos_formais']>=t) for t in (0,1000,5000,10000,20000)},
         'hhi':corr_on(lambda r:True,'productive_hhi','occupational_hhi'),
         'entropy_normalized':corr_on(lambda r:True,'norm_shannon_prod','norm_shannon_ocup'),
         'regions':{re:corr_on(lambda r,re=re:r['regiao']==re) for re in sorted(set(REGIONS.values()))},
         'ufs':{uf:corr_on(lambda r,uf=uf:r['uf']==uf) for uf in states},
       }
    }
    # Anomaly list: approximate standardized residuals, avoid extremes only in tiny labor markets.
    selected=[(r,float(resids[i])) for i,r in enumerate(rows) if r['empregos_formais']>=5000]
    selected.sort(key=lambda v:v[1])
    stat['positive_residuals_5000plus']=[{'ibge':r['ibge_code'],'municipio':r['municipio'],'uf':r['uf'],'empregos':int(r['empregos_formais']),'residual':round(e,4)} for r,e in selected[-8:][::-1]]
    stat['negative_residuals_5000plus']=[{'ibge':r['ibge_code'],'municipio':r['municipio'],'uf':r['uf'],'empregos':int(r['empregos_formais']),'residual':round(e,4)} for r,e in selected[:8]]
    # Regions: unweighted mean municipal Shannon, plus weighted mean by formal jobs (not a regional diversity index).
    stat['regions']={}
    for reg in sorted(set(REGIONS.values())):
        arows=[r for r in rows if r['regiao']==reg]; w=vec('empregos_formais',arows)
        stat['regions'][reg]={'n':len(arows),'jobs':int(sum(w)),
          'avg_prod':float(np.mean(vec('productive_shannon',arows))),
          'avg_ocup':float(np.mean(vec('occupational_shannon',arows))),
          'weighted_prod':float(np.average(vec('productive_shannon',arows),weights=w)),
          'weighted_ocup':float(np.average(vec('occupational_shannon',arows),weights=w)),
        }
    # Raw cleaned and derived numeric analysis file.
    analysiscols=['ibge_code','municipio','uf','regiao','reference_year','empregos_formais','divisoes_produtivas','subgrupos_ocupacionais','productive_shannon','occupational_shannon','productive_hhi','occupational_hhi','equiv_divisoes','equiv_ocupacoes','norm_shannon_prod','norm_shannon_ocup','ln_empregos','modelo_residuo_ocup']
    ar=[]
    for i,r in enumerate(rows):
        rec={k:(r[k] if not isinstance(r[k],float) or math.isfinite(r[k]) else '') for k in analysiscols if k!='modelo_residuo_ocup'};rec['modelo_residuo_ocup']=float(resids[i]); ar.append(rec)
    write_csv(out/'base_analitica_2025.csv',ar,analysiscols)
    # Figure 1
    plt.figure(figsize=(8.5,6.2)); plt.scatter(X,Y,s=6,alpha=.26,rasterized=True)
    coefs=np.polyfit(X,Y,1); xx=np.linspace(X.min(),X.max(),150);plt.plot(xx,np.polyval(coefs,xx),linewidth=1.5)
    plt.xlabel('Diversidade produtiva (Shannon, divisões CNAE)')
    plt.ylabel('Diversidade ocupacional (Shannon, subgrupos CBO)')
    plt.title('Diversidade produtiva e ocupacional | Brasil, 2025')
    plt.text(.02,.04,f'{n:,} unidades | Pearson r = {pear.statistic:.3f}',transform=plt.gca().transAxes,fontsize=9)
    plt.grid(alpha=.15);plt.tight_layout();plt.savefig(out/'figura1_diversidade_nacional.png',dpi=190);plt.close()
    # Figure 2 residual versus productive, with zero reference
    plt.figure(figsize=(8.5,6.2));plt.scatter(X,resids,s=6,alpha=.25,rasterized=True);plt.axhline(0,linestyle='--',linewidth=1)
    plt.xlabel('Diversidade produtiva (Shannon, divisões CNAE)')
    plt.ylabel('Resíduo da diversidade ocupacional')
    plt.title('Diferenças municipais após controlar porte e UF | Brasil, 2025')
    plt.text(.02,.04,'Resíduo do modelo com ln(empregos), seu quadrado e efeitos fixos de UF',transform=plt.gca().transAxes,fontsize=8)
    plt.grid(alpha=.15);plt.tight_layout();plt.savefig(out/'figura2_residuos_condicionais.png',dpi=190);plt.close()
    # Figure 3 region means
    names=list(stat['regions']); ix=np.arange(len(names));ww=.34
    plt.figure(figsize=(8.5,5.5));plt.bar(ix-ww/2,[stat['regions'][k]['avg_prod'] for k in names],width=ww,label='Produtiva')
    plt.bar(ix+ww/2,[stat['regions'][k]['avg_ocup'] for k in names],width=ww,label='Ocupacional')
    plt.xticks(ix,names);plt.ylabel('Shannon médio por município (sem ponderação)');plt.title('Diversidade observada por macrorregião | Brasil, 2025')
    plt.legend();plt.tight_layout();plt.savefig(out/'figura3_macrorregioes.png',dpi=190);plt.close()
    (out/'resultados.json').write_text(json.dumps(stat,ensure_ascii=False,indent=2,default=scalar),encoding='utf8')
    print(json.dumps({k:stat[k] for k in ('n','jobs_total','correlations','regression','checks','robustness','regions','positive_residuals_5000plus','negative_residuals_5000plus')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
