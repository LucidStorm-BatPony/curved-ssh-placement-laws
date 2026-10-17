import numpy as np
# Reciprocal verification: (1) test THEIR shift placement law
# K_bb = -|psi0(b)|^2 / t2_bridged^2 inside MY convention (t1*t2=1),
# (2) close their convention ledger item exactly using both codebases.

Nc=100; ns=2*Nc+1
def build(sigma=0.5, r=0.5, warr=None):
    H=np.zeros((ns,ns),complex); N2=ns-1; tb=np.zeros(ns-1)
    for i in range(ns-1):
        t0=np.sqrt(r) if i%2==0 else 1/np.sqrt(r)
        tb[i]=t0*(((i+1)/N2)**sigma if sigma>0 else 1.0)
        H[i,i+1]=tb[i]; H[i+1,i]=tb[i]
    if warr is not None:
        for i in range(ns-2):
            H[i,i+2]+=1j*warr[i]; H[i+2,i]-=1j*warr[i]
    return H, tb

def ldos(H, eta=1e-3):
    A=(1j*eta)*np.eye(ns)-H
    e=np.zeros(ns,complex); e[0]=1
    return -np.linalg.solve(A,e)[0].imag/np.pi

for SIG,label in [(0.5,"WARPED"),(0.0,"FLAT")]:
    H0,tb=build(SIG); base=np.log(ldos(H0))
    E,V=np.linalg.eigh(H0); k=np.argmin(np.abs(E)); p=np.abs(V[:,k])**2
    eps=0.01
    print(f"== {label} chain, MY convention (t1*t2=1) ==")
    print(f"{'b(site)':>8} {'K_bb measured':>14} {'-p_b/t2br^2':>13} {'ratio':>8}")
    for b in [0,2,4,8,12,20]:
        w=np.zeros(ns-2); w[b]=eps
        K=(np.log(ldos(build(SIG,warr=w)[0]))-base)/eps**2
        law=-p[b]/tb[b+1]**2          # bridged inter-type bond = tb[b+1] for even b
        print(f"{b:>8} {K:14.4e} {law:13.4e} {K/law:8.4f}")

# convention closure: uniform-w responsivity ratio, mine vs theirs, vs (t2_theirs/t2_mine)^-2
print("\n-- convention item closure --")
w0=0.01
H0,_=build(0.5); Hw,_=build(0.5,warr=np.full(ns-2,w0))
mine=(np.log(ldos(Hw))-np.log(ldos(H0)))/w0   # ~ d ln rho/dw at w0 (one-sided, matches earlier defn)
print(f"my uniform-w response at w=0.01 (warped): {mine:+.3f}   their measured: -1.80")
print(f"predicted ratio from law's 1/t2^2 with t2_mine=sqrt2, t2_theirs=1:  {np.sqrt(2)**2:.1f}x  -> {mine*2:+.3f} vs -1.80")
