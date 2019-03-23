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
    q1 = np.quantile(partial_means, tails/2)
    qm = np.median(partial_means)
    mm = np.mean(partial_means)
    q2 = np.quantile(partial_means, 1-tails/2)
    mode = discrete_mode(partial_means)
    averages = {'mean':mm, 'median':qm, 'mode': mode}
    bounds = {'lower': q1, 'higher':q2}
    return {'averages':averages,'bounds':bounds}

@app.post("/test")
async def test(lst: List, fl : float):
    return {'hey': lst, 'now': fl}
