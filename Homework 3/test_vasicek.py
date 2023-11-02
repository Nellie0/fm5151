from vasicek import vasicek_rt_mean, vasicek_rt_var, vasicek_sz, vasicek_d1, vasicek_d2, vasicek_zcb_call, vasicek_zcb_put

a = 0.1
b = 0.08
sigma = 0.015
r0 = 0.05
TO = 1
TB = 3
K = 0.87

def test_vasicek_rt_mean():
    assert vasicek_rt_mean(a, b, r0, 5) == 0.06180408020862101

def test_vasicek_rt_var():
    assert vasicek_rt_var(a, sigma, 5) == 0.0007111356286821273

def test_vasicek_sz():
    assert vasicek_sz(a, sigma, TO, TB) == 0.02588585159177525

def test_vasicek_d1():
    assert vasicek_d1(a, b, sigma, r0, K, TO, TB) == 1.142766967386068

def test_vasicek_d2():
    assert vasicek_d2(a, b, sigma, r0, K, TO, TB) == 1.1168811157942928

def test_vasicek_zcb_call():
    assert vasicek_zcb_call(a, b, sigma, r0, K, TO, TB) == 0.025929830615982197

def test_vasicek_zcb_put():
    assert vasicek_zcb_put(a, b, sigma, r0, K, TO, TB) == 0.001403706405088287