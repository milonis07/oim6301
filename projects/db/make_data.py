"""Writes one CSV file per table for the BabsonAI Labs database, into
projects/db/data/. Uses a fixed random seed so it writes the same files
every time it runs.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

random.seed(42)
fake = Faker()
Faker.seed(42)

AS_OF = date(2026, 11, 8)
WINDOW_START = AS_OF - timedelta(days=365)

NUM_PEOPLE = 25
NUM_PROJECTS = 14
TARGET_TASKS = 300
TARGET_EXPENSES = 220

PROJECT_CATEGORIES = ["LLM app", "data pipeline", "internal tool"]
PROJECT_STATUSES = ["planned", "active", "paused", "done"]
EXPENSE_CATEGORIES = ["GPU cloud", "data labeling", "software", "travel"]
ASSIGNMENT_ROLES = ["Contributor", "Lead", "Reviewer", "Advisor"]

FOUNDER_TITLES = ["Co-Founder & CEO", "Co-Founder & CTO"]
LEAD_TITLES = [
    "Engineering Lead",
    "Data Science Lead",
    "Product Lead",
    "Operations Lead",
]
IC_TITLES = [
    "Machine Learning Engineer",
    "Data Analyst",
    "Software Engineer",
    "Project Manager",
    "Business Analyst",
    "Product Designer",
    "QA Engineer",
    "Data Engineer",
]

TASK_DESCRIPTIONS = [
    "Set up the data pipeline",
    "Fix a bug in the chatbot",
    "Write a client report",
    "Review model outputs",
    "Label a batch of training data",
    "Deploy a change to staging",
    "Update the project plan",
    "Meet with the client",
    "Clean the dataset",
    "Write unit tests",
    "Prepare slides for the demo",
    "Tune the model's parameters",
    "Set up monitoring and alerts",
    "Document the API",
    "Review a teammate's code",
]

EXPENSE_NOTES = {
    "GPU cloud": [
        "Cloud GPU hours for training",
        "Inference serving costs",
        "Spot instance cluster",
    ],
    "data labeling": [
        "Labeling batch for training set",
        "QA pass on labels",
        "Annotation vendor invoice",
    ],
    "software": [
        "Subscription renewal",
        "New developer tool license",
        "API credits",
    ],
    "travel": [
        "Client site visit",
        "Conference travel",
        "Team offsite",
    ],
}


def clamp_date(a_date, earliest, latest):
    if a_date < earliest:
        return earliest
    if a_date > latest:
        return latest
    return a_date


def make_work_email(first_name, last_name, used_emails):
    base = (first_name + "." + last_name).lower()
    email = base + "@babsonailabs.com"
    suffix = 2
    while email in used_emails:
        email = base + str(suffix) + "@babsonailabs.com"
        suffix += 1
    used_emails.add(email)
    return email


def generate_people():
    people = []
    used_emails = set()
    person_id = 1

    founder_ids = []
    for title in FOUNDER_TITLES:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = make_work_email(first_name, last_name, used_emails)
        start_date = AS_OF - timedelta(days=random.randint(900, 1100))
        people.append(
            {
                "person_id": person_id,
                "first_name": first_name,
                "last_name": last_name,
                "work_email": email,
                "title": title,
                "start_date": start_date,
                "manager_id": None,
            }
        )
        founder_ids.append(person_id)
        person_id += 1

    lead_ids = []
    for title in LEAD_TITLES:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = make_work_email(first_name, last_name, used_emails)
        start_date = AS_OF - timedelta(days=random.randint(500, 850))
        manager_id = random.choice(founder_ids)
        people.append(
            {
                "person_id": person_id,
                "first_name": first_name,
                "last_name": last_name,
                "work_email": email,
                "title": title,
                "start_date": start_date,
                "manager_id": manager_id,
            }
        )
        lead_ids.append(person_id)
        person_id += 1

    while len(people) < NUM_PEOPLE:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = make_work_email(first_name, last_name, used_emails)
        start_date = AS_OF - timedelta(days=random.randint(20, 900))
        manager_id = random.choice(lead_ids)
        title = random.choice(IC_TITLES)
        people.append(
            {
                "person_id": person_id,
                "first_name": first_name,
                "last_name": last_name,
                "work_email": email,
                "title": title,
                "start_date": start_date,
                "manager_id": manager_id,
            }
        )
        person_id += 1

    return people


def generate_projects():
    projects = []
    project_id = 1
    for _ in range(NUM_PROJECTS):
        category = random.choice(PROJECT_CATEGORIES)
        status = random.choices(
            PROJECT_STATUSES, weights=[2, 5, 2, 3], k=1
        )[0]
        if random.random() < 0.65:
            client_name = fake.company()
        else:
            client_name = None
        budget = round(random.uniform(20000, 500000), 2)
        start_date = AS_OF - timedelta(days=random.randint(30, 480))
        name = fake.catch_phrase()
        projects.append(
            {
                "project_id": project_id,
                "name": name,
                "client_name": client_name,
                "category": category,
                "budget": budget,
                "start_date": start_date,
                "status": status,
            }
        )
        project_id += 1
    return projects


def generate_assignments(people, projects):
    assignments = []
    assignments_by_project = {}
    for project in projects:
        team_size = random.randint(2, 6)
        team = random.sample(people, team_size)
        team_person_ids = []
        for person in team:
            earliest = person["start_date"]
            if project["start_date"] > earliest:
                earliest = project["start_date"]
            if earliest > AS_OF:
                earliest = AS_OF
            days_available = (AS_OF - earliest).days
            if days_available < 0:
                days_available = 0
            joined_date = earliest + timedelta(
                days=random.randint(0, days_available)
            )
            role = random.choice(ASSIGNMENT_ROLES)
            hours_per_week = random.randint(1, 40)
            assignments.append(
                {
                    "person_id": person["person_id"],
                    "project_id": project["project_id"],
                    "role": role,
                    "hours_per_week": hours_per_week,
                    "joined_date": joined_date,
                }
            )
            team_person_ids.append(person["person_id"])
        assignments_by_project[project["project_id"]] = team_person_ids
    return assignments, assignments_by_project


def generate_tasks(people, projects, assignments_by_project):
    person_start_by_id = {}
    for person in people:
        person_start_by_id[person["person_id"]] = person["start_date"]
    all_person_ids = []
    for person in people:
        all_person_ids.append(person["person_id"])

    tasks = []
    task_id = 1
    tasks_per_project = TARGET_TASKS // NUM_PROJECTS

    for project in projects:
        team = assignments_by_project[project["project_id"]]
        earliest = project["start_date"]
        if earliest < WINDOW_START:
            earliest = WINDOW_START
        for _ in range(tasks_per_project):
            days_available = (AS_OF - earliest).days
            if days_available < 0:
                days_available = 0
            created_date = earliest + timedelta(
                days=random.randint(0, days_available)
            )
            # A real business opens tasks on business days, so pull weekend
            # dates back to the Friday before.
            if created_date.weekday() == 5:
                created_date = created_date - timedelta(days=1)
            elif created_date.weekday() == 6:
                created_date = created_date - timedelta(days=2)
            due_date = created_date + timedelta(days=random.randint(3, 30))

            # Only somebody already at the company by created_date is
            # eligible, so the rule checked in Q7 holds for every task
            # except the two broken on purpose below.
            eligible = []
            for person_id in team:
                if person_start_by_id[person_id] <= created_date:
                    eligible.append(person_id)

            assigned_to = None
            if eligible and random.random() > 0.15:
                assigned_to = random.choice(eligible)

            completed_date = None
            if assigned_to is not None and random.random() < 0.6:
                completed_date = created_date + timedelta(
                    days=random.randint(1, 25)
                )
                completed_date = clamp_date(completed_date, created_date, AS_OF)

            tasks.append(
                {
                    "task_id": task_id,
                    "project_id": project["project_id"],
                    "description": random.choice(TASK_DESCRIPTIONS),
                    "created_date": created_date,
                    "assigned_to": assigned_to,
                    "due_date": due_date,
                    "completed_date": completed_date,
                }
            )
            task_id += 1

    # On purpose: break "a task is assigned only to somebody who works on
    # its project, and never before that person's start date" in exactly
    # two rows, so the question that checks this rule has something to find.
    broken_task_ids = []

    first_project = projects[0]
    first_team = assignments_by_project[first_project["project_id"]]
    outsider_id = None
    for person_id in all_person_ids:
        if person_id not in first_team:
            outsider_id = person_id
            break
    tasks[0]["project_id"] = first_project["project_id"]
    tasks[0]["assigned_to"] = outsider_id
    broken_task_ids.append(tasks[0]["task_id"])

    latest_hire_id = first_team[0]
    for person_id in first_team:
        if person_start_by_id[person_id] > person_start_by_id[latest_hire_id]:
            latest_hire_id = person_id
    tasks[1]["project_id"] = first_project["project_id"]
    tasks[1]["assigned_to"] = latest_hire_id
    tasks[1]["created_date"] = person_start_by_id[latest_hire_id] - timedelta(days=10)
    tasks[1]["due_date"] = tasks[1]["created_date"] + timedelta(days=14)
    tasks[1]["completed_date"] = None
    broken_task_ids.append(tasks[1]["task_id"])

    return tasks, broken_task_ids


def generate_expenses(projects, no_expense_project_ids):
    expenses = []
    expense_id = 1
    projects_with_expenses = []
    for project in projects:
        if project["project_id"] not in no_expense_project_ids:
            projects_with_expenses.append(project)

    expenses_per_project = TARGET_EXPENSES // len(projects_with_expenses)

    for project in projects_with_expenses:
        earliest = project["start_date"]
        if earliest < WINDOW_START:
            earliest = WINDOW_START
        days_available = (AS_OF - earliest).days
        if days_available < 0:
            days_available = 0
        for _ in range(expenses_per_project):
            category = random.choice(EXPENSE_CATEGORIES)
            amount = round(random.uniform(50, 8000), 2)
            expense_date = earliest + timedelta(
                days=random.randint(0, days_available)
            )
            note = random.choice(EXPENSE_NOTES[category])
            expenses.append(
                {
                    "expense_id": expense_id,
                    "project_id": project["project_id"],
                    "expense_date": expense_date,
                    "amount": amount,
                    "category": category,
                    "note": note,
                }
            )
            expense_id += 1

    return expenses


def write_csv(rows, fieldnames, file_path):
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    people = generate_people()
    projects = generate_projects()
    assignments, assignments_by_project = generate_assignments(people, projects)
    tasks, broken_task_ids = generate_tasks(people, projects, assignments_by_project)

    no_expense_project_ids = []
    for project in projects:
        if project["status"] == "planned":
            no_expense_project_ids.append(project["project_id"])
    while len(no_expense_project_ids) < 2:
        candidate = projects[len(no_expense_project_ids)]["project_id"]
        if candidate not in no_expense_project_ids:
            no_expense_project_ids.append(candidate)
    no_expense_project_ids = no_expense_project_ids[:2]

    expenses = generate_expenses(projects, no_expense_project_ids)

    write_csv(
        people,
        ["person_id", "first_name", "last_name", "work_email", "title", "start_date", "manager_id"],
        data_dir / "people.csv",
    )
    write_csv(
        projects,
        ["project_id", "name", "client_name", "category", "budget", "start_date", "status"],
        data_dir / "projects.csv",
    )
    write_csv(
        assignments,
        ["person_id", "project_id", "role", "hours_per_week", "joined_date"],
        data_dir / "assignments.csv",
    )
    write_csv(
        tasks,
        ["task_id", "project_id", "description", "created_date", "assigned_to", "due_date", "completed_date"],
        data_dir / "tasks.csv",
    )
    write_csv(
        expenses,
        ["expense_id", "project_id", "expense_date", "amount", "category", "note"],
        data_dir / "expenses.csv",
    )

    print("people:", len(people))
    print("projects:", len(projects))
    print("assignments:", len(assignments))
    print("tasks:", len(tasks))
    print("expenses:", len(expenses))
    print("projects with no expenses on purpose:", no_expense_project_ids)
    print("tasks that break the assignee rule on purpose:", broken_task_ids)


if __name__ == "__main__":
    main()
