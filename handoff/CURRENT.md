---
type: handoff
name: handoff-current
description: The one active hand-off note. A session that reads status: open claims it first.
project: global
opened: 2026-11-05T00:00:00+00:00
agent: template
status: open
claimed_by: []
generated:
  by: mem-forever/2.0
  at: 2026-11-05T00:00:00+00:00
---
::STATE{@OWNER, kind:person, role:owner, alias:the I in this chat}
::STATE{@TASK, name:<one-line task>, repo:<repo>, branch:<branch>, cwd:<working directory>, owner:@OWNER}
::PROGRESS{date:<YYYY-MM-DD>|done:§<section> <finished, listed by milestone>|next:<the first thing to do next>|unverified:<claimed done but not tested>}
::FACT{key:where_files_are|value:<paths of deliverables, scripts, logs>|conf:confirmed}
::FACT{key:blockers|value:<what is stuck and who decides>|conf:confirmed}
::DECIDE{@OWNER}{what:<what was settled this round>|why:<why, or none>|context:<the block above it rests on, or none>}
::LESSON{id:<key>|type:<kind>|scope:project|conf:tentative}
<the lesson in one line. Source: where it came from>
