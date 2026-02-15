import uuid
import statistics


class AssessmentEngine:

    def __init__(self):
        self.sessions = {}

        # 12 structured questions mapped to psychological axes
        self.questions = [
            {"text": "When criticized, you usually:", "axis": "reflection"},
            {"text": "In conflict, you tend to:", "axis": "assertion"},
            {"text": "When overwhelmed, you:", "axis": "regulation"},
            {"text": "You prefer decisions that are:", "axis": "control"},
            {"text": "When misunderstood, you:", "axis": "assertion"},
            {"text": "Your emotions are:", "axis": "regulation"},
            {"text": "You trust:", "axis": "control"},
            {"text": "Silence makes you feel:", "axis": "reflection"},
            {"text": "When pressured, you:", "axis": "regulation"},
            {"text": "Structure feels:", "axis": "control"},
            {"text": "You process pain by:", "axis": "reflection"},
            {"text": "Power, to you, is:", "axis": "assertion"},
        ]

    # ------------------------
    # SESSION START
    # ------------------------

    def start_session(self):
        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "current_index": 0,
            "scores": {
                "reflection": [],
                "assertion": [],
                "regulation": [],
                "control": []
            }
        }

        return {
            "session_id": session_id,
            "question": self.questions[0]["text"],
            "progress": 0
        }

    # ------------------------
    # ANSWER HANDLER
    # ------------------------

    def submit_answer(self, session_id, answer_value):
        session = self.sessions.get(session_id)

        if not session:
            return {"error": "Invalid session."}

        index = session["current_index"]
        axis = self.questions[index]["axis"]

        # Score should be 1–5 from frontend
        session["scores"][axis].append(answer_value)

        session["current_index"] += 1

        if session["current_index"] >= len(self.questions):
            result = self.generate_result(session["scores"])
            del self.sessions[session_id]
            return {"complete": True, "result": result}

        next_question = self.questions[session["current_index"]]["text"]

        progress = int((session["current_index"] / len(self.questions)) * 100)

        return {
            "complete": False,
            "question": next_question,
            "progress": progress
        }

    # ------------------------
    # RESULT INTELLIGENCE
    # ------------------------

    def generate_result(self, scores):

        averages = {}
        for axis in scores:
            if scores[axis]:
                averages[axis] = round(sum(scores[axis]) / len(scores[axis]), 2)
            else:
                averages[axis] = 0

        dominant = max(averages, key=averages.get)
        lowest = min(averages, key=averages.get)

        stability = round(
            100 - (statistics.pstdev(list(averages.values())) * 20), 2
        )

        return self.build_narrative(dominant, lowest, stability, averages)

    # ------------------------
    # NARRATIVE BUILDER
    # ------------------------

    def build_narrative(self, dominant, lowest, stability, averages):

        lines = []

        # Opening
        lines.append("You are more internally structured than you appear.")

        # Dominant trait exposure
        if dominant == "reflection":
            lines.append("You analyze before you act. You rarely move without internal alignment.")
        elif dominant == "assertion":
            lines.append("You hold strong positions. Even when silent, you are not passive.")
        elif dominant == "regulation":
            lines.append("You contain more than you reveal. Control is your emotional language.")
        elif dominant == "control":
            lines.append("You prefer structure. Chaos unsettles you more than you admit.")

        # Shadow tension
        if lowest == "reflection":
            lines.append("You may avoid sitting too long with your own uncertainty.")
        elif lowest == "assertion":
            lines.append("You sometimes retreat instead of claiming space.")
        elif lowest == "regulation":
            lines.append("Emotion can leak out when pressure builds.")
        elif lowest == "control":
            lines.append("Letting go is harder for you than you show.")

        # Stability Insight
        if stability > 80:
            lines.append("Your psychological structure is stable. You are consistent under pressure.")
        elif stability > 60:
            lines.append("There is balance within you, but tension exists between parts.")
        else:
            lines.append("Your internal forces compete. Growth will require conscious integration.")

        # Closing exposure line
        lines.append("Your shadow is not weakness. It is the part of you that waits to be acknowledged.")

        return "\n\n".join(lines)


# Create global engine instance
engine = AssessmentEngine()