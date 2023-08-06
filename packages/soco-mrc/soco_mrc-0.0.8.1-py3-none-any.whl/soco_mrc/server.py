import asyncio
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import os
from soco_mrc.mrc_model import MRCModel, MRCYesNoNoAnsModel
from soco_mrc.config import EnvVars

class MRCBase(object):
    model = MRCModel(EnvVars.region, EnvVars.use_gpu, EnvVars.max_ans_len)
    yn_model = MRCYesNoNoAnsModel(EnvVars.region, EnvVars.use_gpu, EnvVars.max_ans_len)

    @classmethod
    def batch_predict(cls, model_id, data, n_best, ans_type='auto'):
        if 'cls' in model_id:
            return cls.yn_model.batch_predict(model_id, data, n_best, ans_type)
        else:
            return cls.model.batch_predict(model_id, data, n_best)

path = os.path.dirname(__file__)

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])

model = MRCBase()

loop = asyncio.get_event_loop()
loop.close()


@app.route('/v1/ping', methods=['GET'])
async def ping(request):
    return JSONResponse({'result': 'pong'})


@app.route('/v1/query', methods=['POST'])
async def analyze(request):
    body = await request.json()
    data = body['data']
    model_id = body['model_id']
    params = body.get('params', {})
    n_best = params.get('n_best', 1)
    ans_type = params.get("ans_type", 'auto')
    results = model.batch_predict(model_id, data, n_best, ans_type)
    print(results[0:5])
    return JSONResponse({'result': results})

