import re,sys
b=open(sys.argv[1]).read(); a=open(sys.argv[2]).read()
def fences(t): return re.findall(r'^```.*?^```', t, re.S|re.M)
def heads(t):
    t2=re.sub(r'^```.*?^```','',t,flags=re.S|re.M)
    return [l for l in t2.splitlines() if re.match(r'^#{1,6} ',l)]
def links(t): return sorted(set(re.findall(r'\]\(([^)]+)\)',t)))
def ticks(t):
    t2=re.sub(r'^```.*?^```','',t,flags=re.S|re.M)
    return set(re.findall(r'`([^`\n]+)`',t2))
def quotes(t): return set(re.findall(r'"([^"\n]{3,})"',re.sub(r'^```.*?^```','',t,flags=re.S|re.M)))
fb,fa=fences(b),fences(a)
print("fences before/after:",len(fb),len(fa),"identical-seq:",fb==fa, "missing:",[x[:60] for x in fb if x not in fa])
hb,ha=heads(b),heads(a)
print("headings before/after:",len(hb),len(ha)); print("missing headings:",[h for h in hb if h not in ha]); print("new headings:",[h for h in ha if h not in hb])
lb,la=links(b),links(a); print("missing link targets:",[x for x in lb if x not in la]); print("new link targets:",[x for x in la if x not in lb])
tb,ta=ticks(b),ticks(a); print("missing code identifiers:",sorted(tb-ta))
qb,qa=quotes(b),quotes(a); print("missing quoted strings:",sorted(qb-qa))
