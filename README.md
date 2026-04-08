# Email AI — OpenEnv Submission

An AI agent that classifies and replies to emails across three difficulty tiers using a Qwen 72B model via Hugging Face Inference Router.

---

## Project Structure

```
email_ai_project/
├── app.py              ← Flask HTTP server (HF Spaces entry point)
├── inference.py        ← Chain-of-thought agent runner
├── openenv.yaml        ← Environment metadata
├── Dockerfile
├── requirements.txt
├── .env.example
├── validate.sh         ← Pre-submission validator
├── env/
│   ├── __init__.py
│   ├── models.py       ← Pydantic typed models
│   ├── email_env.py    ← OpenEnv environment (reset / step / state)
│   ├── reward.py       ← Reward shaping logic
│   └── tasks.py        ← Easy / Medium / Hard graders
└── dashboard/
    └── index.html      ← Web dashboard
```

---

## Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export HF_TOKEN=your_huggingface_token
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

# 3. Run pre-submission validator
bash validate.sh

# 4. Run the agent
python inference.py

# 5. OR start the Flask API server
python app.py
```

---

## Docker

```bash
# Build
docker build -t email-ai .

# Run Flask server (default)
docker run -p 7860:7860 \
  -e HF_TOKEN=your_token \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  email-ai

# Run inference instead
docker run \
  -e HF_TOKEN=your_token \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  email-ai python inference.py
```

---

## HTTP API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check (returns 200) |
| POST | `/reset` | Reset environment, returns initial observation |
| POST | `/step` | Take an action, returns obs/reward/done/info |
| GET | `/state` | Current score and step count |
| POST | `/grade` | Run all three graders on a list of actions |

### Example `/step` request body

```json
{
  "type": "classify",
  "email_id": 1,
  "label": "urgent",
  "response": ""
}
```

---

## Graders

| Grader | Scoring |
|--------|---------|
| `grade_easy()` | 1.0 if any email labelled urgent, else 0.0 |
| `grade_medium()` | Fraction of spam/normal correctly labelled (out of 6) |
| `grade_hard()` | Classification accuracy (10 emails) + reply quality bonus |

---

## Deploy to Hugging Face Spaces

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose **Docker** as the SDK
3. Upload all project files
4. Add Secrets under **Settings → Variables and Secrets**:
   - `HF_TOKEN`
   - `API_BASE_URL`
   - `MODEL_NAME`
5. The Space will start and serve on port 7860
6. Verify: `curl https://your-space.hf.space/` should return `{"status": "ok", ...}`

---

## Log Format

```
[START] task=email-winning env=email-env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action={"type":"classify","email_id":1,"label":"urgent",...} reward=0.50 done=false error=null
[END] success=true steps=12 score=0.85 rewards=0.50,0.40,...
```
