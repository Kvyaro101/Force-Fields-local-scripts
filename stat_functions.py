def stat_sigma(values:list, square:bool) -> float:
    mean = sum(values)/len(values)
    sigma_value = sum((i-mean)**2 for i in values) / len(values)
    if square:
        return sigma_value
    else:
        return sigma_value**(1/2)

def get_analysis_for_ff(qm_e:list[int], mm_e:list[int]):
    deviations = [mm_e[i] - qm_e[i] for i in range(len(mm_e))]
    mean_dev = sum(deviations) / len(deviations)
    sqrt_dev = ( sum(i**2 for i in deviations) / len(deviations) ) ** (1/2)
    covariation_dev = (
        sum(i*j for i,j in zip(qm_e, mm_e)) / len(qm_e) - (sum(qm_e)/len(qm_e))*
        (sum(mm_e)/len(mm_e))
    )
    qm_sig, mm_sig = stat_sigma(qm_e, False), stat_sigma(mm_e, False)
    correlation_dev = covariation_dev/(qm_sig * mm_sig)
    return Stat_characteristic(mean_dev, sqrt_dev, (qm_sig, mm_sig),covariation_dev, correlation_dev)
    


class Stat_characteristic:
    def __init__(self, mean, sqrt, sigmas, cov, corr):
        self.mean = mean
        self.sqrt = sqrt
        self.sigmas = sigmas
        self.cov = cov
        self.corr = corr

if __name__ == "__main__":
    res = get_analysis_for_ff([3, 4, 6, 2, 9, 6, 8, 7, 5, 8], [2, 3, 6, 1, 7, 4, 9, 6, 8, 5])
    print(res.cov, res.corr) # 4.1200000000000045 0.7652178521673068
