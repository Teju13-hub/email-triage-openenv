#!/usr/bin/env bash
# Pre-submission validation script
# Usage: bash validate.sh

set -e
echo "=== Email AI Project Validator ==="

# 1. Check required files
echo ""
echo "[1/5] Checking required files..."
REQUIRED=(inference.py app.py Dockerfile openenv.yaml requirements.txt env/models.py env/email_env.py env/reward.py env/tasks.py)
for f in "${REQUIRED[@]}"; do
  if [ -f "$f" ]; then
    echo "  ✅  $f"
  else
    echo "  ❌  MISSING: $f"
    exit 1
  fi
done

# 2. Check env vars
echo ""
echo "[2/5] Checking environment variables..."
for var in HF_TOKEN API_BASE_URL MODEL_NAME; do
  if [ -n "${!var}" ]; then
    echo "  ✅  $var is set"
  else
    echo "  ⚠️   $var is NOT set (export it before running inference.py)"
  fi
done

# 3. Python syntax check
echo ""
echo "[3/5] Python syntax check..."
for pyfile in inference.py app.py env/models.py env/email_env.py env/reward.py env/tasks.py; do
  python3 -m py_compile "$pyfile" && echo "  ✅  $pyfile" || { echo "  ❌  Syntax error in $pyfile"; exit 1; }
done

# 4. Import check
echo ""
echo "[4/5] Import check..."
python3 -c "
from env.models import Observation, Action, Email, Reward
from env.email_env import EmailEnv
from env.reward import compute_reward
from env.tasks import grade_easy, grade_medium, grade_hard
env = EmailEnv()
obs = env.reset()
assert hasattr(obs, 'inbox')
assert len(obs.inbox) == 10
print('  ✅  All imports OK, env reset works')
"

# 5. Grader smoke test
echo ""
echo "[5/5] Grader smoke test..."
python3 -c "
from env.tasks import grade_easy, grade_medium, grade_hard

sample = [
  {'type': 'classify', 'email_id': 1, 'label': 'urgent',  'response': ''},
  {'type': 'classify', 'email_id': 2, 'label': 'spam',    'response': ''},
  {'type': 'classify', 'email_id': 3, 'label': 'normal',  'response': ''},
]

easy   = grade_easy(sample)
medium = grade_medium(sample)
hard   = grade_hard(sample)

assert 0.0 <= easy   <= 1.0, f'grade_easy out of range: {easy}'
assert 0.0 <= medium <= 1.0, f'grade_medium out of range: {medium}'
assert 0.0 <= hard   <= 1.0, f'grade_hard out of range: {hard}'

print(f'  ✅  grade_easy={easy:.2f}  grade_medium={medium:.2f}  grade_hard={hard:.2f}')
"

echo ""
echo "=== All checks passed! Ready to submit. ==="
