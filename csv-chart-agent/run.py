"""Runtime: upload a CSV, run the chart agent, download the generated chart.

Usage:
    python run.py path/to/data.csv

Requires these environment variables:
    ANTHROPIC_API_KEY   your Claude API key
    AGENT_ID            agent_... from the one-time setup (see README)
    ENV_ID              env_...   from the one-time setup (see README)
"""

import os
import sys
import time

import anthropic

WORKSPACE_SLUG = os.getenv("ANTHROPIC_WORKSPACE_SLUG", "default")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python run.py path/to/data.csv")
    csv_path = sys.argv[1]

    agent_id = os.environ["AGENT_ID"]
    env_id = os.environ["ENV_ID"]

    client = anthropic.Anthropic()

    # 1. Upload the CSV.
    with open(csv_path, "rb") as f:
        uploaded = client.beta.files.upload(file=(os.path.basename(csv_path), f, "text/csv"))

    # 2. Start a session with the CSV mounted read-only at /workspace/data.csv.
    session = client.beta.sessions.create(
        agent=agent_id,
        environment_id=env_id,
        title="CSV chart",
        resources=[{"type": "file", "file_id": uploaded.id, "mount_path": "/workspace/data.csv"}],
    )
    print(
        "Watch live: "
        f"https://platform.claude.com/workspaces/{WORKSPACE_SLUG}/sessions/{session.id}\n"
    )

    # 3. Stream-first, then send the kickoff (so we don't miss early events).
    kickoff = (
        "Read /workspace/data.csv, pick the chart that best fits the data, "
        "generate it with Python (matplotlib), and save the image to "
        "/mnt/session/outputs/. Briefly explain what you plotted."
    )
    with client.beta.sessions.events.stream(session_id=session.id) as stream:
        client.beta.sessions.events.send(
            session_id=session.id,
            events=[{"type": "user.message", "content": [{"type": "text", "text": kickoff}]}],
        )
        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="", flush=True)
            elif event.type == "session.status_terminated":
                break
            elif event.type == "session.status_idle":
                # idle is transient (e.g. waiting on a tool confirmation) —
                # only stop on a terminal stop_reason.
                if getattr(event.stop_reason, "type", None) == "requires_action":
                    continue
                break

    # 4. Download whatever the agent wrote to /mnt/session/outputs/.
    os.makedirs("outputs", exist_ok=True)
    files = None
    for _ in range(3):  # brief indexing lag after idle
        files = client.beta.files.list(scope_id=session.id, betas=["managed-agents-2026-04-01"])
        if files.data:
            break
        time.sleep(2)

    for f in files.data if files else []:
        dest = os.path.join("outputs", os.path.basename(f.filename))
        client.beta.files.download(f.id).write_to_file(dest)
        print(f"\nSaved: {dest}")

    # 5. Clean up the uploaded original. The session-scoped copy is garbage
    #    collected with the session.
    client.beta.files.delete(uploaded.id)


if __name__ == "__main__":
    main()
