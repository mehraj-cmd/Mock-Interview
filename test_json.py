import time
from ai_client import generate_ai_completion
start = time.time()
res = generate_ai_completion('Generate 3 python questions. Return STRICTLY as JSON object: {"questions": ["q1", "q2"]}', json_mode=True)
print(f'Time: {time.time()-start:.2f}s')
print('Result:', str(res)[:100])
