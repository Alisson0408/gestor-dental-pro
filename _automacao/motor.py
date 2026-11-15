#!/usr/bin/env python3
"""Motor de criativos do Gestor Dental PRO (@gestordentalpro).

Uso:
  python3 motor.py reel      roteiro.json  saida.mp4
  python3 motor.py carrossel roteiro.json  pasta_saida/

O roteiro é uma lista de cenas/slides. Tipos:
  hook     {"tag","texto","destaque"}            frase de impacto (destaque = trecho em dourado)
  painel   {"titulo","valor","itens":[[rot,val],..]}  painel "dinheiro escapando" com contador
  lista    {"tag","titulo","itens":[..],"cor":"red|gold|green"}
  numero   {"tag","numero","texto","nota"}       número grande
  barras   {"tag","titulo","barras":[[rot,txt,pct,cor],..],"nota"}
  checks   {"tag","titulo","itens":[..]}
  acoes    {"tag","titulo","itens":[[icone,texto,botao],..]}
  cta      {"titulo","sub"}
Cada cena de reel aceita "dur" (segundos, padrão 3.2).
"""
import os, json, sys, subprocess, pathlib, math, wave, struct, random

BASE = pathlib.Path(__file__).resolve().parent
F = (BASE / 'fonts').as_uri()
TOOTH = '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 5.2C10.4 3.6 8 3 6.3 3.6 3.8 4.5 3 7.2 3.6 10c.5 2.1 1.4 3.5 1.9 5.6.5 2.2.6 5.4 2.3 5.4 1.6 0 1.7-3 2.2-4.6.4-1.2 1-1.9 2-1.9s1.6.7 2 1.9c.5 1.6.6 4.6 2.2 4.6 1.7 0 1.8-3.2 2.3-5.4.5-2.1 1.4-3.5 1.9-5.6.6-2.8-.2-5.5-2.7-6.4C16 3 13.6 3.6 12 5.2Z" fill="{c}"/></svg>'

CSS = """
@font-face{font-family:J;src:url(F/plus-jakarta-sans-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:J;src:url(F/plus-jakarta-sans-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:J;src:url(F/plus-jakarta-sans-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:J;src:url(F/plus-jakarta-sans-latin-800-normal.woff2);font-weight:800}
*{box-sizing:border-box;margin:0}
html,body{width:WWpx;height:HHpx;overflow:hidden;font-family:J,sans-serif;color:#fff;-webkit-font-smoothing:antialiased;background:#072a30}
.bg{position:absolute;inset:0;background:radial-gradient(900px 800px at 90% -5%,rgba(230,197,122,.28),transparent 60%),radial-gradient(900px 800px at -10% 105%,rgba(19,112,122,.65),transparent 60%),linear-gradient(160deg,#0a3d44,#072a30 70%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(circle at 50% 40%,#000,transparent 75%)}
.scene{position:absolute;inset:0;padding:PADT 80px PADB;display:flex;flex-direction:column;opacity:0}
.top{display:flex;align-items:center;gap:16px}
.logo{width:68px;height:68px;border-radius:19px;background:linear-gradient(135deg,#f0d38c,#c79a3b);display:grid;place-items:center;box-shadow:0 10px 30px rgba(199,154,59,.35)}
.brand b{font-size:30px;font-weight:800;letter-spacing:-.5px;display:block}.brand small{font-size:16px;letter-spacing:4px;color:#e6c57a;font-weight:800}
.tag{display:inline-block;align-self:flex-start;background:rgba(230,197,122,.14);border:2px solid rgba(230,197,122,.42);color:#e6c57a;border-radius:40px;padding:12px 26px;font-weight:800;font-size:26px;letter-spacing:.5px}
h1{font-weight:800;letter-spacing:-3px;line-height:1.03}
em{font-style:normal;background:linear-gradient(135deg,#f6e1a6,#c79a3b);-webkit-background-clip:text;color:transparent}
.sub{font-size:38px;line-height:1.35;color:#cfe4e7;font-weight:600}
.sp{flex:1}
.card{background:#f6f8f9;color:#0f1f2a;border-radius:36px;padding:34px;box-shadow:0 40px 90px rgba(0,0,0,.45)}
.panel{background:linear-gradient(135deg,#0a3d44,#0e5a63 60%,#13707a);border-radius:28px;padding:34px;color:#fff}
.panel .l{font-size:22px;letter-spacing:1.5px;text-transform:uppercase;color:#bfe0e3;font-weight:700}
.panel .v{font-size:96px;font-weight:800;color:#e6c57a;letter-spacing:-3px;margin:8px 0 22px}
.leak{display:grid;grid-template-columns:1fr 1fr;gap:16px}.leak div{background:rgba(255,255,255,.1);border-radius:18px;padding:18px 20px}.leak span{display:block;font-size:22px;color:#bfe0e3}.leak b{font-size:36px}
.li{display:flex;align-items:center;gap:24px;font-size:44px;font-weight:700;padding:22px 0;border-bottom:2px solid rgba(255,255,255,.08)}
.li i{flex:none;width:58px;height:58px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-weight:800;font-size:30px}
.big{font-weight:800;letter-spacing:-8px;line-height:.9}
.bar{height:30px;border-radius:15px;background:rgba(255,255,255,.1);overflow:hidden}.bar i{display:block;height:100%;border-radius:15px}
.row{display:flex;justify-content:space-between;align-items:baseline;font-size:34px;font-weight:700;margin:30px 0 14px}
.todo{background:#fff;color:#0f1f2a;border-radius:30px;padding:10px 30px;box-shadow:0 40px 90px rgba(0,0,0,.4)}
.todo div{display:flex;align-items:center;gap:18px;padding:26px 0;border-bottom:2px solid #e2e8ec;font-size:32px;font-weight:600}.todo div:last-child{border:0}
.todo em{font-style:normal;color:#fff;-webkit-text-fill-color:#fff;background:#1fae5b;margin-left:auto;border-radius:12px;padding:8px 16px;font-weight:800;font-size:24px;white-space:nowrap}
.cta{display:inline-flex;align-items:center;gap:12px;background:linear-gradient(135deg,#f0d38c,#c79a3b);color:#2b1d02;font-weight:800;font-size:44px;padding:32px 52px;border-radius:26px;box-shadow:0 20px 60px rgba(199,154,59,.45)}
.foot{display:flex;justify-content:space-between;font-size:26px;color:#a9cdd1;font-weight:600;border-top:1px solid rgba(255,255,255,.12);padding-top:28px}
.a{opacity:0}
.prog{position:absolute;left:80px;right:80px;bottom:70px;height:6px;border-radius:3px;background:rgba(255,255,255,.12)}.prog i{display:block;height:100%;background:#e6c57a;border-radius:3px}
"""

COR = {'red': ('rgba(207,63,63,.2)', '#f08a8a', '✕'), 'gold': ('rgba(230,197,122,.18)', '#e6c57a', '!'), 'green': ('rgba(29,132,90,.25)', '#7fe0b0', '✓')}

def top():
    return f'<div class="top a" data-in="0"><span class="logo">{TOOTH.format(s=38,c="#2b1d02")}</span><span class="brand"><b>Gestor Dental</b><small>PRO</small></span></div>'

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def h1(texto, destaque, size):
    t = esc(texto)
    if destaque:
        d = esc(destaque); t = t.replace(d, f'<em>{d}</em>', 1)
    return f'<h1 class="a" data-in=".25" style="font-size:{size}px;margin-top:36px">{t}</h1>'

def scene_html(s, reel):
    k = s['tipo']; o = top() + '<div class="sp"></div>'
    big = 1.0 if reel else 0.86
    if s.get('tag'): o += f'<div class="tag a" data-in=".1" style="margin-top:0">{esc(s["tag"])}</div>'
    if k == 'hook':
        o += h1(s['texto'], s.get('destaque'), int(118*big))
        if s.get('sub'): o += f'<p class="sub a" data-in=".9" style="margin-top:40px">{esc(s["sub"])}</p>'
    elif k == 'painel':
        o += h1(s.get('titulo',''), s.get('destaque'), int(84*big)) if s.get('titulo') else ''
        it = ''.join(f'<div class="a" data-in="{1.0+i*.25:.2f}"><span>{esc(a)}</span><b>{esc(b)}</b></div>' for i,(a,b) in enumerate(s['itens']))
        o += f'<div class="card a" data-in=".45" style="margin-top:60px"><div class="panel"><div class="l">{esc(s.get("rotulo","Dinheiro escapando da clínica agora"))}</div><div class="v" data-count="{s["valor"]}">R$ {s["valor"]}</div><div class="leak">{it}</div></div></div>'
    elif k == 'lista':
        bg, fg, ic = COR[s.get('cor','red')]
        o += h1(s['titulo'], s.get('destaque'), int(88*big))
        o += '<div style="margin-top:50px">' + ''.join(f'<div class="li a" data-in="{.7+i*.32:.2f}"><i style="background:{bg};color:{fg}">{ic}</i>{esc(x)}</div>' for i,x in enumerate(s['itens'])) + '</div>'
    elif k == 'numero':
        fs = int(min(230, 880 / max(1, len(str(s["numero"])) * 0.6)) * big)
        o += f'<div class="big a" data-in=".3" style="font-size:{fs}px;margin-top:60px;white-space:nowrap"><em>{esc(s["numero"])}</em></div>'
        o += f'<p class="sub a" data-in=".8" style="margin-top:36px;color:#fff;font-size:46px;font-weight:700">{esc(s["texto"])}</p>'
        if s.get('nota'): o += f'<p class="sub a" data-in="1.4" style="margin-top:34px">{esc(s["nota"])}</p>'
    elif k == 'barras':
        o += h1(s['titulo'], s.get('destaque'), int(84*big))
        cols = {'green':'#1d845a,#7fe0b0','gold':'#a96b12,#e6c57a','red':'#cf3f3f,#f08a8a'}
        b = ''
        for i,(rot,txt,pct,cor) in enumerate(s['barras']):
            d = .7+i*.45
            b += f'<div class="row a" data-in="{d:.2f}"><span>{esc(rot)}</span><span style="color:{cols[cor].split(",")[1]}">{esc(txt)}</span></div><div class="bar a" data-in="{d:.2f}"><i data-grow="{pct}" data-in="{d+.15:.2f}" style="width:{pct}%;background:linear-gradient(90deg,{cols[cor]})"></i></div>'
        o += f'<div style="margin-top:40px">{b}</div>'
        if s.get('nota'): o += f'<p class="a" data-in="2.0" style="font-size:26px;color:#a9cdd1;margin-top:24px">{esc(s["nota"])}</p>'
    elif k == 'checks':
        o += h1(s['titulo'], s.get('destaque'), int(90*big))
        o += '<div style="margin-top:50px">' + ''.join(f'<div class="li a" data-in="{.7+i*.32:.2f}" style="font-size:40px"><i style="background:rgba(230,197,122,.18);color:#e6c57a">✓</i>{esc(x)}</div>' for i,x in enumerate(s['itens'])) + '</div>'
    elif k == 'acoes':
        o += h1(s['titulo'], s.get('destaque'), int(84*big))
        o += '<div class="todo a" data-in=".6" style="margin-top:56px">' + ''.join(f'<div class="a" data-in="{.9+i*.35:.2f}">{esc(ic)} {esc(tx)}<em>{esc(bt)}</em></div>' for i,(ic,tx,bt) in enumerate(s['itens'])) + '</div>'
    elif k == 'cta':
        o += f'<div class="a" data-in=".1" style="margin:0 auto;width:{300 if reel else 240}px;height:{300 if reel else 240}px;border-radius:80px;background:linear-gradient(135deg,#f6e1a6,#c79a3b);display:grid;place-items:center;box-shadow:0 40px 100px rgba(199,154,59,.45)">{TOOTH.format(s=180 if reel else 140,c="#0a3d44")}</div>'
        o += f'<h1 class="a" data-in=".4" style="font-size:{int(96*big)}px;margin-top:70px;text-align:center">{esc(s["titulo"])}</h1>'
        if s.get('sub'): o += f'<p class="sub a" data-in=".8" style="margin-top:30px;text-align:center">{esc(s["sub"])}</p>'
        o += f'<div class="a" data-in="1.1" style="text-align:center;margin-top:60px"><span class="cta">{esc(s.get("botao","Teste grátis por 7 dias"))}</span></div>'
    o += '<div class="sp"></div>'
    if not reel:
        o += f'<div class="foot"><span>@gestordentalpro</span><span>{esc(s.get("rodape","Teste grátis por 7 dias →"))}</span></div>'
    return o

JS = """
const S=[...document.querySelectorAll('.scene')];const D=DURS;const T=D.reduce((a,b)=>a+b,0);
const ease=x=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
window.setT=function(t){let acc=0;S.forEach((s,i)=>{const l=t-acc;const d=D[i];acc+=d;
 const vis=l>=-0.0001&&l<d;const fin=Math.min(1,l/0.25),fout=i<S.length-1?Math.min(1,(d-l)/0.25):1;
 s.style.opacity=vis?Math.min(fin,fout):0;if(!vis)return;
 const z=1+0.03*(l/d);s.style.transform='scale('+z+')';
 s.querySelectorAll('.a').forEach(e=>{const p=ease((l-parseFloat(e.dataset.in||0))/0.5);e.style.opacity=p;e.style.transform='translateY('+(30*(1-p))+'px)'});
 s.querySelectorAll('[data-count]').forEach(e=>{const v=parseFloat(e.dataset.count.replace(/\\./g,'').replace(',','.'));const p=ease((l-0.6)/1.6);
  e.textContent='R$ '+(v*p).toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})});
 s.querySelectorAll('[data-grow]').forEach(e=>{const p=ease((l-parseFloat(e.dataset.in))/0.9);e.style.width=(parseFloat(e.dataset.grow)*p)+'%'});
});const pr=document.querySelector('.prog i');if(pr)pr.style.width=(100*t/T)+'%'};
window.showAll=function(){S.forEach(s=>{s.style.opacity=1;s.querySelectorAll('.a').forEach(e=>{e.style.opacity=1;e.style.transform='none'})})};
"""

def page(scenes, reel, w, h):
    durs = [float(s.get('dur', 3.2)) for s in scenes]
    css = CSS.replace('F/', F + '/').replace('WW', str(w)).replace('HH', str(h)).replace('PADT', '210px' if reel else '84px').replace('PADB', '300px' if reel else '84px')
    body = ''.join(f'<div class="scene">{scene_html(s, reel)}</div>' for s in scenes)
    prog = '<div class="prog"><i></i></div>' if reel else ''
    return f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="bg"></div><div class="grid"></div>{body}{prog}<script>{JS.replace("DURS", json.dumps(durs))}</script></body></html>', durs

def musica(path, dur, seed=7):
    """Trilha própria (livre de direitos): pad suave + pulso, gerada por síntese."""
    import numpy as np
    sr = 44100; n = int(sr*dur); t = np.arange(n)/sr
    rnd = random.Random(seed)
    prog = [[220.0,277.18,329.63],[196.0,246.94,329.63],[174.61,220.0,261.63],[196.0,246.94,293.66]]
    rnd.shuffle(prog)
    out = np.zeros(n)
    seg = 2.0
    for i in range(int(math.ceil(dur/seg))):
        a, b = int(i*seg*sr), min(n, int((i+1)*seg*sr+sr*0.3))
        tt = t[a:b]-i*seg; env = np.minimum(1, tt/0.25)*np.exp(-tt*0.35)
        for f in prog[i % 4]:
            out[a:b] += 0.08*env*(np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt))
    beat = 60/112
    for k in range(int(dur/beat)):
        a = int(k*beat*sr); b = min(n, a+int(0.18*sr)); tt = t[a:b]-k*beat
        out[a:b] += 0.32*np.exp(-tt*28)*np.sin(2*np.pi*(55+90*np.exp(-tt*40))*tt)
        if k % 2:
            hh = np.random.default_rng(k).standard_normal(b-a)*np.exp(-tt*90)*0.04; out[a:b] += hh
    fade = np.minimum(1, np.minimum(t/0.5, (dur-t)/1.0))
    out = np.tanh(out*fade*1.4)*0.8
    data = (out*32767).astype('<i2').tobytes()
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data)

def carregar(pg, html):
    """Abre o HTML a partir de um arquivo local (necessário para carregar as fontes)."""
    tmp = BASE / f'.render-{os.getpid()}.html'
    tmp.write_text(html, encoding='utf-8')
    pg.goto(tmp.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)

def reel(spec, out):
    from playwright.sync_api import sync_playwright
    scenes = spec['cenas'] if isinstance(spec, dict) else spec
    html, durs = page(scenes, True, 1080, 1920)
    total = sum(durs); fps = 30; nf = int(total*fps)
    out = pathlib.Path(out); tmp = out.with_name(out.stem + '.tmp.mp4'); silent = out.with_name(out.stem + '.v.mp4'); wav = out.with_suffix('.wav')
    ff = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r',str(fps),str(silent)], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
        carregar(pg, html)
        for i in range(nf):
            pg.evaluate(f'setT({i/fps})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        b.close()
    ff.stdin.close(); ff.wait()
    musica(wav, total, seed=spec.get('seed', 7) if isinstance(spec, dict) else 7)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(tmp)], check=True)
    tmp.rename(out); silent.unlink(); wav.unlink()
    print(out, f'{total:.1f}s')

def carrossel(spec, outdir):
    from playwright.sync_api import sync_playwright
    slides = spec['slides'] if isinstance(spec, dict) else spec
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350})
        for i, s in enumerate(slides, 1):
            html, _ = page([dict(s, dur=1)], False, 1080, 1350)
            carregar(pg, html)
            pg.evaluate('showAll(); setT(0.999); showAll(); document.querySelectorAll("[data-grow]").forEach(e=>e.style.width=e.dataset.grow+"%"); document.querySelectorAll("[data-count]").forEach(e=>e.textContent="R$ "+e.dataset.count); document.querySelector(".scene").style.transform="none"')
            pg.screenshot(path=str(outdir / f'{i:02d}.jpg'), type='jpeg', quality=92)
        b.close()
    print(outdir, len(slides), 'slides')

if __name__ == '__main__':
    modo, roteiro, saida = sys.argv[1:4]
    spec = json.load(open(roteiro, encoding='utf-8'))
    (reel if modo == 'reel' else carrossel)(spec, saida)
