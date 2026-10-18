# NLP Fleet Query System

A simple web app that lets you ask questions about a fleet in plain English
and get answers from a database — no SQL required.

It uses **spaCy** to understand your text, detects what kind of fleet you're
asking about (trucks, rails, ships, or cargo), builds the matching SQL query,
and shows the results in a table.

## How it works

1. You type a question like *"show me all trucks"* in the web form.
2. spaCy (with a custom entity rule for fleet types) scans the text.
3. The app converts it into an SQL query.
4. The query runs against a SQLite database (`newfleet.db`).
5. The matching rows are displayed on the results page.

## Tech stack

- **Python**
- **Flask** – web framework
- **spaCy** – natural language processing (`en_core_web_sm` model)
- **SQLite** – database (`newfleet.db`)

## Project structure
