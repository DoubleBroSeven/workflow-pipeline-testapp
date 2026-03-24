# workflow-pipeline-testapp
E2E test consumer for workflow-pipeline — Python link manager

## Wildcard Pipeline

This project uses [workflow-pipeline](https://github.com/DoubleBroSeven/workflow-pipeline) to manage development workflows.

| Setting | Value |
|---|---|
| Ticketing | file-based |
| Git Host | github |
| Branch Strategy | development → epic/E1 → E1/E1-001 |
| Language | python |
| Test Runner | pytest |

### Commands
```bash
workflow-pipeline status          # View pipeline state
workflow-pipeline epic list       # List epics
workflow-pipeline run             # Pick up next ticket
workflow-pipeline ticket done ID  # Complete a ticket
```

### Workflow
1. Create an epic with tickets
2. Approve the epic (`gate approve`)
3. `run` picks up the next ticket and creates a branch
4. Code, test, commit
5. `ticket done` → `epic complete` → PR
