import datetime

class Planner:

    def __init__(self, calendar, reminder):
        self.calendar = calendar
        self.reminder = reminder

    def generate_day_plan(self, goals):
        """
        goals = [
            {"task": "Study DBMS", "duration": 2},
            {"task": "Gym", "duration": 1},
        ]
        """

        now = datetime.datetime.now()
        current_hour = max(now.hour + 1, 8)

        plan = []

        for g in goals:
            start = datetime.datetime.combine(
                now.date(),
                datetime.time(current_hour, 0)
            )

            end = start + datetime.timedelta(hours=g["duration"])

            plan.append({
                "task": g["task"],
                "start": start,
                "end": end
            })

            current_hour += g["duration"]

        return plan


    def apply_plan(self, plan):
        for p in plan:
            self.calendar.add_event(
                p["task"],
                p["start"].isoformat(),
                p["end"].isoformat()
            )