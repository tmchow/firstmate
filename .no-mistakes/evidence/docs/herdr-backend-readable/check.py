import re,sys,subprocess,os,collections
b=open(sys.argv[1]).read(); a=open(sys.argv[2]).read()
def blocks(t):
    out=[];cur=None;fence=None
    for l in t.split('\n'):
        m=re.match(r'^(\s*)(```+|~~~+)',l)
        if cur is None and m: cur=[l];fence=m.group(2);continue
        if cur is not None:
            cur.append(l)
            if l.strip().startswith(fence) and l.strip().strip(fence[0])=='' : out.append('\n'.join(cur));cur=None
    return out
def strip(t):
    return re.sub(r'(?ms)^\s*(```+|~~~+).*?^\s*\1\s*$','',t)
def heads(t): return [l for l in strip(t).split('\n') if re.match(r'^#{1,6} ',l)]
def slug(h):
    s=re.sub(r'^#+ ','',h).strip().lower(); s=re.sub(r'[^\w\- ]','',s); return s.replace(' ','-')
def links(t): return collections.Counter(re.findall(r'\]\(([^)\s]+)',strip(t)))
def html_anchors(t): return set(re.findall(r'<a (?:name|id)="([^"]+)"',t))
bb,ab=blocks(b),blocks(a)
print("code blocks before/after:",len(bb),len(ab))
missing=[x for x in bb if x not in ab]; print("code blocks missing/altered:",len(missing))
print("code blocks sequence identical:", bb==ab)
hb,ha=heads(b),heads(a)
lost=[h for h in hb if h not in ha]; print("headings before/after:",len(hb),len(ha)); print("original headings missing:",lost)
sb=set(map(slug,hb)); sa=set(map(slug,ha)); print("anchors lost:",sorted(sb-sa)); print("html anchors lost:",sorted(html_anchors(b)-html_anchors(a)))
lb,la=links(b),links(a); print("link targets dropped:",sorted(set(lb)-set(la))); print("link targets added:",sorted(set(la)-set(lb)))
# internal anchors in after resolve
bad=[l for l in la if l.startswith('#') and l[1:] not in sa|html_anchors(a)]; print("unresolved in-doc anchors:",bad)
# relative file links resolve
d=os.path.dirname(sys.argv[3])
badf=[l for l in la if not l.startswith(('#','http')) and not os.path.exists(os.path.normpath(os.path.join(d,l.split('#')[0])))]; print("unresolved relative file links:",badf)
# inbound references
r=subprocess.run(['git','grep','-hoE',r'herdr-backend\.md#[A-Za-z0-9_-]+'],capture_output=True,text=True).stdout.split()
inb=sorted(set(x.split('#')[1] for x in r)); badin=[x for x in inb if x not in sa|html_anchors(a)]
print("inbound anchor refs:",len(inb),"unresolved:",badin)
# one sentence per line (outside code/tables): lines with >1 sentence end
multi=[l for l in strip(a).split('\n') if not l.startswith('|') and len(re.findall(r'[a-z0-9`)\]]\. [A-Z`]',l))>0]
print("lines possibly holding >1 sentence:",len(multi))
for l in multi[:10]: print("  >",l[:160])
