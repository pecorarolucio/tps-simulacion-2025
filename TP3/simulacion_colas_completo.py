# -------------------  simulacion_colas_completo.py  -------------------
import simpy, random, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from matplotlib.backends.backend_pdf import PdfPages

# ---------- parámetros globales ----------
mu = 1.0
cargas   = [0.25, 0.5, 0.75, 1.0, 1.25]
lambdas  = [c * mu for c in cargas]
colas    = [float('inf'), 0, 2, 5, 10, 50]
num_rep        = 30
num_clientes   = 1000
n_target       = 3           # ← queremos P(n = 3 en cola)
# -----------------------------------------

# ---------- fórmulas teóricas ----------
def p_den_mm1k(lmbda, mu, K):
    ρ = lmbda / mu
    if abs(ρ-1) < 1e-12:
        return 1 / (K+1)
    return ((1-ρ)*ρ**K) / (1-ρ**(K+1))

def prob_n_cola_mm1(lmbda, mu, n):
    ρ = lmbda / mu
    return (1-ρ) * ρ**(n+1)

def prob_n_cola_mm1k(lmbda, mu, K, n):
    ρ = lmbda / mu
    P0 = 1/(K+1) if abs(ρ-1)<1e-12 else (1-ρ)/(1-ρ**(K+1))
    return ρ**(n+1) * P0 if n < K else 0

def teoria_mm1(lmbda, mu):
    ρ = lmbda / mu
    if abs(ρ-1) < 1e-12:
        return [np.nan]*5          # diverge
    L  = ρ/(1-ρ)
    Lq = ρ**2/(1-ρ)
    W  = 1/(mu-lmbda)
    Wq = lmbda/(mu*(mu-lmbda))
    return L, Lq, W, Wq, ρ

def teoria_mm1k(lmbda, mu, K):
    ρ    = lmbda / mu
    Pden = p_den_mm1k(lmbda, mu, K)

    if Pden >= 1-1e-12:            # todo se rechaza
        return [np.nan]*5
    if abs(ρ-1) < 1e-12:           # ρ = 1, K finito
        L  = K/2
        Lq = (K-1)/2
        W  = L  / (lmbda*(1-Pden))
        Wq = Lq / (lmbda*(1-Pden))
        return L, Lq, W, Wq, ρ

    L  = ρ*(1-(K+1)*ρ**K + K*ρ**(K+1)) / ((1-ρ)*(1-ρ**(K+1)))
    Lq = L - ρ*(1-ρ**K)/(1-ρ**(K+1))
    W  = L  / (lmbda*(1-Pden))
    Wq = W - 1/mu
    return L, Lq, W, Wq, ρ
# ---------------------------------------------------------------------

# ---------- simulador discreto ----------
def sim_mm1(lmbda, mu, K=np.inf):
    env   = simpy.Environment()
    serv  = simpy.Resource(env, capacity=1)
    q_lim = None if K==float('inf') else K
    t_sys, t_que, rechaz = [], [], 0
    count_n = 0   # ← llegadas que encuentran n_target en cola

    def cliente():
        nonlocal rechaz, count_n
        t0 = env.now
        # rechazo si cola llena
        if q_lim is not None and len(serv.queue) >= q_lim:
            rechaz += 1
            return
        # cuenta llegadas con n_target clientes esperando
        if len(serv.queue) == n_target:
            count_n += 1
        with serv.request() as req:
            yield req
            t_que.append(env.now - t0)
            yield env.timeout(random.expovariate(mu))
            t_sys.append(env.now - t0)

    def generador():
        for _ in range(num_clientes):
            env.process(cliente())
            yield env.timeout(random.expovariate(lmbda))

    env.process(generador()); env.run()

    atend  = len(t_sys)
    p_den  = rechaz / num_clientes
    L  = np.mean(t_sys)*lmbda*(1-p_den) if atend else 0
    Lq = np.mean(t_que)*lmbda*(1-p_den) if atend else 0
    W  = np.mean(t_sys) if atend else 0
    Wq = np.mean(t_que) if atend else 0
    ρ  = L
    Pn = count_n / num_clientes         # ← prob. simulada de n_target en cola
    return L, Lq, W, Wq, ρ, p_den, Pn
# ---------------------------------------------------------------------

# ---------- experimentos ----------
rows = []
for K, lmb in product(colas, lambdas):
    for _ in range(num_rep):
        Ls, Lqs, Ws, Wqs, ρs, Ps, Pn_s = sim_mm1(lmb, mu, K)
        if K == float('inf'):
            Lt, Lqt, Wt, Wqt, ρt = teoria_mm1(lmb, mu)
            Pt   = 0
            Pn_t = prob_n_cola_mm1(lmb, mu, n_target)
        else:
            Lt, Lqt, Wt, Wqt, ρt = teoria_mm1k(lmb, mu, int(K))
            Pt   = p_den_mm1k(lmb, mu, int(K))
            Pn_t = prob_n_cola_mm1k(lmb, mu, int(K), n_target)

        rows.append({
            "K": "∞" if K == float('inf') else K,
            "ρ": round(lmb / mu, 2),
            "L_sim": Ls,  "L_teo": Lt,
            "Lq_sim": Lqs, "Lq_teo": Lqt,
            "W_sim": Ws,   "W_teo": Wt,
            "Wq_sim": Wqs, "Wq_teo": Wqt,
            "ρ_sim": ρs,   "ρ_teo": ρt,
            "Pden_sim": Ps, "Pden_teo": Pt,
            "P3_sim": Pn_s, "P3_teo": Pn_t
        })

df = pd.DataFrame(rows)
df.to_csv("mm1_resultados_completos.csv", index=False)
print(">>> CSV guardado como mm1_resultados_completos.csv")

# ---------- función de gráficos ----------
def graficar_subset(sub, titulo=""):
    fig, axs = plt.subplots(3, 3, figsize=(15, 12))
    metricas = [
        ("L",   "Prom. nº en sistema (L)"),
        ("Lq",  "Prom. nº en cola (Lq)"),
        ("ρ",   "Utilización (ρ)"),
        ("W",   "Prom. tiempo en sistema (W)"),
        ("Wq",  "Prom. tiempo en cola (Wq)"),
        ("Pden","Prob. de denegación"),
        ("P3",  f"Prob. n={n_target} en cola")
    ]
    for i, (m, ttl) in enumerate(metricas):
        ax = axs[i // 3][i % 3]
        sim = sub[f"{m}_sim"]
        teo = sub[f"{m}_teo"].iloc[0]
        ax.plot(sim.values, label="Simulado")
        ax.axhline(teo, color="r", ls="--", label="Teórico")
        ax.axhline(sim.mean(), color="g", ls="-.", label="Prom. sim.")
        ax.set_title(ttl); ax.grid(True); ax.legend()
    plt.suptitle(titulo, fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig
# ---------------------------------------------------------------------

# ---------- PDF multipágina ----------
with PdfPages("mm1_todas_las_figuras.pdf") as pdf:
    for K in df["K"].unique():
        for r in df["ρ"].unique():
            sub = df[(df["K"] == K) & (df["ρ"] == r)]
            if sub.empty:
                continue
            fig = graficar_subset(sub, f"K = {K}  |  ρ = {r}")
            pdf.savefig(fig)
            plt.close(fig)
print(">>> PDF generado: mm1_todas_las_figuras.pdf")

# ---------- Gráfico de ejemplo (ρ = 0.75, K = ∞) ----------
sub = df[(df["K"] == "∞") & (df["ρ"] == 0.75)]
graficar_subset(sub, "Ejemplo: K = ∞  |  ρ = 0.75")
plt.show()
# ----------------------------------------------------------------------
