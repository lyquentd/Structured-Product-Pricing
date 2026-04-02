import numpy as np

# Let's test standard ZC continuous formula if Taux is discrete ZC rate
rate_6y = 0.0460
T = 6.0

def test1():
    # What if Taux IS the ZC discret rate? Then DF = 1 / (1+rate)^T
    df = 1 / (1 + rate_6y)**T
    zc_cont = -np.log(df) / T
    print(f"Test 1 (Taux is ZC discret): DF={df:.5f}, ZC={zc_cont:.5f}")

def test2():
    # What if Taux is continuous ZC?
    df = np.exp(-rate_6y * T)
    zc_cont = -np.log(df) / T
    print(f"Test 2 (Taux is ZC cont): DF={df:.5f}, ZC={zc_cont:.5f}")

# Bootstrapping swap rates (annual)
rates = [0.0332, 0.0384, 0.0413, 0.0433, 0.0448, 0.0460]
def test3():
    dfs = []
    for i, r in enumerate(rates):
        t = i + 1
        if t == 1:
            dfs.append(1 / (1 + r))
        else:
            prev_sum = sum(dfs)
            dfs.append((1 - r * prev_sum) / (1 + r))
    df_6 = dfs[-1]
    zc_cont = -np.log(df_6) / 6
    print(f"Test 3 (My Bootstrap): DF={df_6:.5f}, ZC={zc_cont:.5f} -> wait my previous gave df=0.76118")

def test4():
    # User's exact screenshot values:
    # 4.5% ZC cont -> DF = exp(-0.045*6) = 0.763379
    # User screenshot says ZF=76.33%
    # This matches ZC cont = 4.50%.
    # But how did they get DF=76.33%?
    pass

test1()
test2()
test3()
test4()

