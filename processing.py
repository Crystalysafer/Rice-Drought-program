import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score


def heritability_calc(df:pd.DataFrame):
    # df.index: varieties, df.columns: repetition
    # return singleVal
    n, r = df.shape
    if (n <= 1) or (r <= 1):
        return np.nan
    
    meanVal_n = df.mean(axis=0)
    meanVal_r = df.mean(axis=1)
    meanVal = meanVal_n.mean()
                                            #                                       Degrees of Freedom
    SST = pow(df - meanVal, 2).sum().sum()  # Sum of Squares Total                  nr-1
    SSB = pow(meanVal_r - meanVal, 2).sum() * r  # Sum of Squares Between Groups    n-1
    SSW = pow(meanVal_n - meanVal, 2).sum() * n  # Sum of Squares Within Groups     r-1
    SSE = SST - SSW - SSB                   # Sum of Squares Error                  (r-1)(n-1)

    MSB = SSB / (n-1)
    MSE = SSE / ((r-1)*(n-1))

    if (MSB == 0) and (MSE==0):
        return 1

    heritability = (MSB-MSE) / (MSB+(r-1)*MSE)

    return heritability

def remove_outlier(series:pd.Series, n=3) -> pd.Series:
    mean = series.mean()
    std = series.std()
    upper = mean + n * std
    lower = mean - n * std
    series = series.map(lambda x: x if lower < x < upper else np.nan)

    return series

def stepwiseregression(X_train, Y_train, X_test, Y_test):

        X = pd.DataFrame(X_train)
        X.columns = map(str, X.columns)
        X.columns = "x" + X.columns
        Y = pd.DataFrame(Y_train, columns=["Y"])
        data = pd.concat([X, Y], axis=1)
        variables = set(X.columns)
        selected = []  # 最终自变量集
        current_score, best_new_score = float('inf'), float('inf')  # 设置分数的初始值为无穷大（因为aic/bic越小越好
        count = 0
        while variables:
            count += 1
            aic_with_variables = []  # 记录遍历过程的分数
            for candidate in variables:
                formula = "{}~{}".format(data.columns[-1], "+".join(selected + [candidate]))  # 组合
                model = smf.ols(formula=formula, data=data)
                aic = model.fit().aic
                aic_with_variables.append((aic, candidate))
            aic_with_variables.sort(reverse=True)  # 降序后, 取出当前最好模型分数
            best_new_score, best_candidate = aic_with_variables.pop()
            # print(count)
            if count > 100:
                break
            if current_score > best_new_score:
                variables.remove(best_candidate)
                selected.append(best_candidate)
                current_score = best_new_score
                if len(selected) > 20:
                    break
        formula = "{}~{}".format(data.columns[-1], "+".join(selected))
        model = smf.ols(formula=formula, data=data)
        params = model.fit().params

        X_test = pd.DataFrame(X_test)
        X_test.columns = X.columns
        y_test_pred = np.dot(X_test.loc[:, params.index[1:]], params[1:]) + params[0]
        r2 = r2_score(Y_test, y_test_pred)

        return r2



        
        