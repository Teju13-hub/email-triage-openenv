from flask import Flask, request, jsonify
from env.email_env import EmailEnv

app = Flask(__name__)
env = EmailEnv()


@app.route("/", methods=["GET"])
def health():
    """Health check — must return 200 for the validator."""
    return jsonify({"status": "ok", "env": "email-env", "version": "1.0"})


@app.route("/reset", methods=["POST"])
def reset():
    obs = env.reset()
    return jsonify(obs.model_dump())


@app.route("/step", methods=["POST"])
def step():
    data = request.get_json(force=True)
    action_obj = type("Action", (), data)()
    obs, reward, done, info = env.step(action_obj)
    return jsonify({
        "obs": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info,
    })


@app.route("/state", methods=["GET"])
def state():
    return jsonify(env.state())


@app.route("/grade", methods=["POST"])
def grade():
    """Run all three graders against a list of actions."""
    from env.tasks import grade_easy, grade_medium, grade_hard
    actions = request.get_json(force=True)
    return jsonify({
        "easy":   grade_easy(actions),
        "medium": grade_medium(actions),
        "hard":   grade_hard(actions),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
