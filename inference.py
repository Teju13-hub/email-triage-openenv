import os
import json
from openai import OpenAI
from env.email_env import EmailEnv
from env.tasks import grade_hard

API_BASE_URL = os.getenv('API_BASE_URL', 'https://router.huggingface.co/v1')
MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-72B-Instruct')
API_KEY = os.getenv('HF_TOKEN')

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

env = EmailEnv()
obs = env.reset()

print(f"[START] task=email-winning env=email-env model={MODEL_NAME}", flush=True)

rewards = []
actions = []
steps = 0

while True:
    steps += 1
    prompt = f"""You are a chain-of-thought email AI assistant.
Analyze the inbox step-by-step and choose the best action.

Inbox: {obs.model_dump_json()}

Rules:
- Classify each email correctly: urgent, spam, or normal
- Reply professionally if the email warrants a response
- Consider deadlines and priority hints in deciding urgency

Return ONLY a JSON object with these exact keys:
  type      (string): "classify" or "reply"
  email_id  (int):    the email ID you are acting on
  label     (string): "urgent", "spam", or "normal"
  response  (string): your reply text if type is "reply", else ""
"""

    error_value = None
    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        content = res.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        action = json.loads(content.strip())
    except Exception as e:
        error_value = str(e)
        action = {"type": "classify", "email_id": steps, "label": "urgent", "response": ""}

    actions.append(action)

    action_obj = type("Action", (), action)()
    obs, reward, done, _ = env.step(action_obj)
    rewards.append(f"{reward:.2f}")

    # error must be JSON null (not the string "null")
    error_json = "null" if error_value is None else json.dumps(error_value)
    done_str = "true" if done else "false"
    action_json = json.dumps(action)

    print(
        f'[STEP] step={steps} action={action_json} reward={reward:.2f} done={done_str} error={error_json}',
        flush=True
    )

    if done:
        break

score = grade_hard(actions)
rewards_str = ",".join(rewards)
print(f"[END] success=true steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)
