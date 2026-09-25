import re,sys,glob,os
def slug(h):
    s=h.strip().lower(); s=re.sub(r'[^\w\- ]','',s); return s.replace(' ','-')
t=open('docs/remote-secondmates.md').read()
t2=re.sub(r'^```.*?^```','',t,flags=re.S|re.M)
slugs=set(); seen={}
for l in t2.splitlines():
    m=re.match(r'^#{1,6} (.*)',l)
    if m:
        s=slug(re.sub(r'`','',m.group(1))); n=seen.get(s,0); seen[s]=n+1
        slugs.add(s if n==0 else f"{s}-{n}")
bad=[]
for a in re.findall(r'\]\(#([^)]+)\)',t):
    if a not in slugs: bad.append(('self',a))
for f in glob.glob('**/*.md',recursive=True):
    if f.startswith('node_modules'): continue
    for a in re.findall(r'remote-secondmates\.md#([A-Za-z0-9_\-]+)',open(f,errors='ignore').read()):
        if a not in slugs: bad.append((f,a))
print("heading anchors:",len(slugs)); print("unresolved anchors:",bad or "none")
refs=[(f,a) for f in glob.glob('**/*',recursive=True) if os.path.isfile(f) and not f.startswith('.git') for a in re.findall(r'remote-secondmates\.md#([A-Za-z0-9_\-]+)',open(f,errors='ignore').read())]
print("inbound anchor refs checked:",len(refs))
