from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
from scipy import stats
import numpy as np
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['POST'], allow_headers=['*'],
                    allow_credentials = True,)


@app.get("/")
async def root():
    return {"message": "Hello World"}

class MeanProblem(BaseModel):
    values : List[int]
    tails: float

def jknife(xs):
    means = []
    means.append(np.mean(xs[1:]))
    for i in range(1,len(xs)):
        ys = xs[:i] + xs[i+1:]
        means.append(np.mean(ys))
    return means

def discrete_mode(ys,bins=20):
    try:
        m, M = np.min(ys), np.max(ys)
        xs = np.linspace(m,M,bins)
        p = zip(xs,stats.gaussian_kde(ys).evaluate(xs))
        return max(p, key = lambda x: x[1])[0]
    except: return np.nan

@app.post("/jackknife")
async def jack(prob: MeanProblem):
    '''The jacknife: provides confidence intervals for the true population mean of a sample'''
    values, tails = prob.values, prob.tails
    print(values, tails)
    partial_means = jknife(values)
    mode = discrete_mode(partial_means)
    left = (1 - tails)/2
    results = {
            'mean': np.mean(partial_means),
            'median': np.median(partial_means),
            'lower': np.quantile(partial_means, left),
            'higher': np.quantile(partial_means, 1-left),
            'mode': mode,
            'big_sigma': sum(values),
            'big_modal_sigma': mode * len(values)
    }

    print(results)
    return results

@app.post("/test")
async def test(lst: List, fl : float):
    return {'hey': lst, 'now': fl}
