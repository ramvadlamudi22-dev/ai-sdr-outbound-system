from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RecordReview:
    company: str
    role: str
    source: str
    status: str
    score: int
    priority: str
    summary: str
    next_step: str


def score_record(row: dict[str, str]) -> int:
    score = 40
    role = row.get("contact_role", "").lower()
    source = row.get("source", "").lower()
    notes = row.get("notes", "").lower()
    current_priority = row.get("priority", "").lower()

    if any(word in role for word in ["founder", "owner"]):
        score += 25
    elif "manager" in role:
        score += 15

    if any(word in source for word in ["website", "referral", "portfolio"]):
        score += 15

    if any(word in notes for word in ["automation", "workflow", "report", "follow-up", "appointment"]):
        score += 15

    if current_priority == "high":
        score += 5

    return min(score, 100)


def priority_from_score(score: int) -> str:
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def next_step(priority: str) -> str:
    if priority == "high":
        return "Prepare a short human-reviewed response and move to active review."
    if priority == "medium":
        return "Collect missing context and review again."
    return "Keep in backlog until more context is available."


def review_record(row: dict[str, str]) -> RecordReview:
    score = score_record(row)
    priority = priority_from_score(score)
    company = row.get("company", "Unknown")
    role = row.get("contact_role", "Unknown")
    source = row.get("source", "Unknown")
    status = row.get("status", "new")
    notes = row.get("notes", "No notes provided")

    return RecordReview(
        company=company,
        role=role,
        source=source,
        status=status,
        score=score,
        priority=priority,
        summary=f"{company} | {role} | {notes}",
        next_step=next_step(priority),
    )


def load_records(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def print_report(reviews: list[RecordReview]) -> None:
    print("AI SDR Outbound System - Demo Report")
    print("=" * 44)
    print("Human-reviewed workflow assistant demo")
    print()

    for index, review in enumerate(reviews, start=1):
        print(f"{index}. {review.company}")
        print(f"   Role: {review.role}")
        print(f"   Source: {review.source}")
        print(f"   Status: {review.status}")
        print(f"   Score: {review.score}/100")
        print(f"   Priority: {review.priority}")
        print(f"   Summary: {review.summary}")
        print(f"   Next step: {review.next_step}")
        print()

    high_priority = sum(1 for review in reviews if review.priority == "high")
    print("Summary")
    print("-" * 44)
    print(f"Total records reviewed: {len(reviews)}")
    print(f"High priority records: {high_priority}")
    print("Policy: suggested actions require human review before use.")


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    records_path = project_root / "data" / "sample_records.csv"
    records = load_records(records_path)
    reviews = [review_record(row) for row in records]
    print_report(reviews)


if __name__ == "__main__":
    main()
