#!/usr/bin/env python3
"""Gera o blog do Gestor Dental PRO a partir de _automacao/blog/posts/*.json.
Cada post: {"slug","titulo","descricao","data":"AAAA-MM-DD","palavra_chave","corpo_md","cta":"mercado|diagnostico|demo"}
Uso: python3 _automacao/blog.py   (recria blog/<slug>/index.html, blog/index.html, sitemap.xml e robots.txt)"""
import json, re, html, glob, os, datetime, urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE='https://dental.aastecnologiaeditorial.com.br'
WA='5519989522187'
MESES=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
def dataBR(d):
    y,m,dd=map(int,d.split('-'));return f'{dd} de {MESES[m-1]} de {y}'
def inline(t):
    t=html.escape(t,quote=False)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    t=re.sub(r'\[(.+?)\]\((https?://[^)\s]+|/[^)\s]*)\)',r'<a href="\2">\1</a>',t)
    return t
def md(src):
    out=[];lista=None;par=[]
    def fecha():
        nonlocal lista,par
        if par: out.append('<p>'+inline(' '.join(par))+'</p>');par=[]
        if lista: out.append(f'</{lista}>');lista=None
    for ln in src.splitlines():
        s=ln.strip()
        if not s: fecha();continue
        m=re.match(r'^(#{2,3})\s+(.*)',s)
        if m: fecha();n=len(m.group(1));out.append(f'<h{n}>{inline(m.group(2))}</h{n}>');continue
        m=re.match(r'^(?:[-*]|(\d+)[.)])\s+(.*)',s)
        if m:
            if par: out.append('<p>'+inline(' '.join(par))+'</p>');par=[]
            tipo='ol' if m.group(1) else 'ul'
            if lista!=tipo:
                if lista: out.append(f'</{lista}>')
                out.append(f'<{tipo}>');lista=tipo
            out.append('<li>'+inline(m.group(2))+'</li>');continue
        if s.startswith('>'): fecha();out.append('<blockquote>'+inline(s.lstrip('> '))+'</blockquote>');continue
        if lista: out.append(f'</{lista}>');lista=None
        par.append(s)
    fecha();return '\n'.join(out)
CTAS={
 'mercado':('Seu preço dá lucro de verdade?','O Gestor Dental PRO calcula o custo real de cada procedimento e compara com o preço praticado na sua região — em minutos.','/?demo#mercado','Ver a Análise de mercado (grátis)'),
 'diagnostico':('Quanto dinheiro está escapando do seu consultório?','Responda 5 perguntas e veja o diagnóstico na hora — faltas, orçamentos parados, inadimplência e glosas.','/comecar/','Fazer o diagnóstico grátis'),
 'demo':('Veja funcionando, sem cadastro','Abra a demonstração do Gestor Dental PRO com dados de exemplo e explore agenda, orçamentos, prontuário e financeiro.','/?demo','Abrir a demonstração'),
}
CSS='''*{box-sizing:border-box}body{margin:0;font-family:"Plus Jakarta Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#0f1f2a;background:#f6f8f9;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:#0e5a63}.top{background:linear-gradient(135deg,#072a30,#0e5a63);color:#fff;padding:14px 0}.w{max-width:760px;margin:0 auto;padding:0 20px}
.top .w{display:flex;justify-content:space-between;align-items:center;gap:12px}.logo{color:#fff;text-decoration:none;font-weight:800;font-size:17px}.logo b{color:#e6c57a}
.tb{background:linear-gradient(135deg,#e6c57a,#c79a3b);color:#2b1d02;text-decoration:none;font-weight:700;font-size:13.5px;padding:9px 14px;border-radius:10px;white-space:nowrap}
article{background:#fff;border:1px solid #e2e8ec;border-radius:18px;padding:30px 26px;margin:26px 0;box-shadow:0 10px 30px rgba(7,42,48,.06)}
h1{font-size:30px;line-height:1.25;margin:6px 0 10px;letter-spacing:-.4px}h2{font-size:21px;margin:30px 0 8px;color:#0a3d44}h3{font-size:17px;margin:22px 0 6px}
.meta{color:#5b6c78;font-size:13.5px}.lead{font-size:17px;color:#33454f}blockquote{margin:16px 0;padding:12px 16px;border-left:4px solid #c79a3b;background:#fbf6ea;border-radius:8px}
li{margin:4px 0}.cta{margin:30px 0 4px;padding:22px;border-radius:16px;background:linear-gradient(135deg,#072a30,#0e5a63);color:#fff}.cta h3{margin:0 0 6px;color:#e6c57a;font-size:19px}
.cta p{margin:0 0 14px;color:#d5e6e8}.cta .tb{display:inline-block;padding:12px 18px;font-size:15px}.wa{display:inline-block;margin-left:10px;color:#fff;font-size:14px}
.lista a{display:block;background:#fff;border:1px solid #e2e8ec;border-radius:14px;padding:18px 20px;margin:12px 0;text-decoration:none;color:#0f1f2a}.lista a:hover{border-color:#c79a3b}
.lista b{font-size:17.5px;display:block;margin-bottom:4px}.lista span{color:#5b6c78;font-size:14px}footer{color:#5b6c78;font-size:12.5px;text-align:center;padding:10px 0 34px}
@media(max-width:600px){h1{font-size:25px}article{padding:22px 18px}}'''
def head(titulo,desc,url,extra=''):
    return f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{html.escape(titulo)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="article"><meta property="og:url" content="{url}">
<meta name="author" content="Gestor Dental PRO · AAS Tecnologia Editorial">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>{extra}</head><body>
<div class="top"><div class="w"><a class="logo" href="/">🦷 Gestor Dental <b>PRO</b></a><a class="tb" href="/comecar/">Diagnóstico grátis</a></div></div>'''
FOOT='<footer>© {a} Gestor Dental PRO · AAS Tecnologia Editorial · <a href="/blog/">Blog</a> · <a href="/vendas/">Conheça o sistema</a></footer></body></html>'
def main():
    posts=[]
    for f in sorted(glob.glob(os.path.join(ROOT,'_automacao/blog/posts/*.json'))):
        p=json.load(open(f,encoding='utf-8'))
        for k in ('slug','titulo','descricao','data','corpo_md'): assert p.get(k),f'{f}: falta {k}'
        assert re.fullmatch(r'[a-z0-9-]+',p['slug']),f'slug inválido {p["slug"]}'
        posts.append(p)
    posts.sort(key=lambda p:p['data'],reverse=True)
    ano=datetime.date.today().year
    for p in posts:
        url=f'{SITE}/blog/{p["slug"]}/'
        ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":p['titulo'],"description":p['descricao'],"datePublished":p['data'],"author":{"@type":"Organization","name":"Gestor Dental PRO"},"publisher":{"@type":"Organization","name":"AAS Tecnologia Editorial"},"mainEntityOfPage":url},ensure_ascii=False)
        t,s,link,lab=CTAS.get(p.get('cta','diagnostico'),CTAS['diagnostico'])
        wa=f'https://wa.me/{WA}?text='+urllib.parse.quote('Olá! Li o artigo "'+p['titulo']+'" no blog e quero conhecer o Gestor Dental PRO.')
        rel=[q for q in posts if q is not p][:3]
        relh=''.join(f'<a href="/blog/{q["slug"]}/"><b>{html.escape(q["titulo"])}</b><span>{html.escape(q["descricao"])}</span></a>' for q in rel)
        corpo=f'''{head(p['titulo']+' | Gestor Dental PRO',p['descricao'],url,'<script type="application/ld+json">'+ld+'</script>')}
<div class="w"><article><div class="meta"><a href="/blog/">Blog do Gestor Dental PRO</a> · {dataBR(p['data'])}</div><h1>{html.escape(p['titulo'])}</h1><p class="lead">{html.escape(p['descricao'])}</p>
{md(p['corpo_md'])}
<div class="cta"><h3>{t}</h3><p>{s}</p><a class="tb" href="{link}">{lab}</a><a class="wa" href="{wa}">ou fale no WhatsApp →</a></div></article>
{('<h2 style="font-size:19px">Leia também</h2><div class="lista">'+relh+'</div>') if relh else ''}</div>{FOOT.format(a=ano)}'''
        d=os.path.join(ROOT,'blog',p['slug']);os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(corpo)
    lista=''.join(f'<a href="/blog/{p["slug"]}/"><b>{html.escape(p["titulo"])}</b><span>{dataBR(p["data"])} · {html.escape(p["descricao"])}</span></a>' for p in posts)
    idx=f'''{head('Blog do Gestor Dental PRO — gestão e finanças para dentistas','Artigos práticos para dentistas: precificação, faltas, orçamentos, inadimplência, convênios e gestão do consultório.',SITE+'/blog/')}
<div class="w"><h1 style="margin-top:26px">Gestão e finanças para dentistas</h1><p class="lead">Conteúdo prático para o consultório lucrar mais com os mesmos pacientes.</p><div class="lista">{lista}</div></div>{FOOT.format(a=ano)}'''
    os.makedirs(os.path.join(ROOT,'blog'),exist_ok=True);open(os.path.join(ROOT,'blog','index.html'),'w',encoding='utf-8').write(idx)
    urls=[('/', None),('/vendas/',None),('/comecar/',None),('/como-funciona/',None),('/blog/',posts[0]['data'] if posts else None)]+[(f'/blog/{p["slug"]}/',p['data']) for p in posts]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{SITE}{u}</loc>'+(f'<lastmod>{d}</lastmod>' if d else '')+'</url>\n' for u,d in urls)+'</urlset>\n'
    open(os.path.join(ROOT,'sitemap.xml'),'w',encoding='utf-8').write(sm)
    open(os.path.join(ROOT,'robots.txt'),'w',encoding='utf-8').write(f'User-agent: *\nAllow: /\nDisallow: /_automacao/\nSitemap: {SITE}/sitemap.xml\n')
    print(f'{len(posts)} artigo(s) gerado(s).')
if __name__=='__main__': main()
