from env.models import Observation, Action, Email
from env.reward import compute_reward

class EmailEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.emails = [
            Email(id=1, subject="URGENT: Server Down", body="Fix immediately", sender="boss@company.com", priority_hint="urgent", deadline="today"),
            Email(id=2, subject="Win Prize!!!", body="Click link spam", sender="spam@fake.com", priority_hint="spam", deadline=None),
            Email(id=3, subject="Weekly Report", body="Submit by Friday", sender="manager@company.com", priority_hint="normal", deadline="Friday"),
            Email(id=4, subject="Meeting Reminder", body="Team sync at 4pm", sender="hr@company.com", priority_hint="normal", deadline=None),
            Email(id=5, subject="Project Deadline", body="Submit draft ASAP", sender="lead@company.com", priority_hint="urgent", deadline="tomorrow"),
            Email(id=6, subject="Social Event", body="Team outing next week", sender="hr@company.com", priority_hint="normal", deadline=None),
            Email(id=7, subject="Invoice", body="Please pay by Friday", sender="finance@company.com", priority_hint="normal", deadline="Friday"),
            Email(id=8, subject="Security Alert", body="Change password", sender="it@company.com", priority_hint="urgent", deadline="today"),
            Email(id=9, subject="Newsletter", body="Company news", sender="newsletter@company.com", priority_hint="normal", deadline=None),
            Email(id=10, subject="Spam Offer", body="Claim your prize", sender="spam@fake.com", priority_hint="spam", deadline=None),
        ]
        self.history = []
        self.score = 0.0
        self.steps = 0
        self.done = False
        self.last_error = None
        return Observation(inbox=self.emails, history=self.history, step_count=0)

    def step(self, action: Action):
        self.steps += 1
        try:
            reward, feedback = compute_reward(self.emails, action, self.history)
            self.last_error = None
        except Exception as e:
            reward = -1.0
            feedback = "error"
            self.last_error = str(e)

        self.score += reward
        self.history.append(str(action))

        if self.steps >= 12:
            self.done = True

        obs = Observation(
            inbox=self.emails,
            history=self.history,
            last_action_error=self.last_error,
            step_count=self.steps
        )
        return obs, reward, self.done, {"feedback": feedback}

    def state(self):
        return {"score": round(self.score, 2), "steps": self.steps}
