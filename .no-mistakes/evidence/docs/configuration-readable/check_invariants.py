import re, sys, collections, subprocess, pathlib
base = open(sys.argv[1]).read(); new = open(sys.argv[2]).read()
def slug(h):
    s = h.strip().lower()
    s = re.sub(r'[^\w\- ]', '', s)
    return s.replace(' ', '-')
def headings(t):
    out=[]; infence=False
    for l in t.splitlines():
        if l.startswith('```'): infence = not infence; continue
        m = re.match(r'^(#{1,6})\s+(.*)$', l)
        if m and not infence: out.append(slug(m.group(2)))
    return out
def fences(t): return re.findall(r'^```.*?^```', t, re.M|re.S)
def strip_fences(t): return re.sub(r'^```.*?^```', '', t, flags=re.M|re.S)
def codes(t): return collections.Counter(re.findall(r'`([^`\n]+)`', strip_fences(t)))
def links(t): return set(re.findall(r'\]\(([^)\s]+)\)', t))
def nums(t): return set(re.findall(r'\b\d+(?:\.\d+)?\b', strip_fences(t)))
bh, nh = headings(base), headings(new)
missing_anchors = [h for h in bh if h not in nh]
print("base headings:", len(bh), "new headings:", len(nh))
print("original anchors missing in new:", missing_anchors)
bf, nf = fences(base), fences(new)
print("fenced blocks base/new:", len(bf), len(nf), "byte-identical:", bf == nf)
bc, nc = codes(base), codes(new)
lost = {k:v-nc.get(k,0) for k,v in bc.items() if nc.get(k,0) < v}
print("inline-code occurrences lost:", lost)
bl, nl = links(base), links(new)
print("link targets lost:", sorted(bl-nl))
bn, nn = nums(base), nums(new)
print("numeric literals lost:", sorted(bn-nn))
# external anchors into configuration.md
repo = pathlib.Path('.')
refs = subprocess.run(['git','grep','-ohE',r'configuration\.md#[A-Za-z0-9_-]+'],capture_output=True,text=True).stdout.split()
bad = sorted({r for r in refs if r.split('#')[1] not in nh})
print("repo-wide configuration.md# refs:", len(set(refs)), "unresolved:", bad)
# self anchors
selfrefs = set(re.findall(r'\]\(#([^)]+)\)', new))
print("in-doc #anchor links:", len(selfrefs), "unresolved:", sorted(a for a in selfrefs if a not in nh))
# sentence-per-line heuristic: prose lines with more than one sentence break
