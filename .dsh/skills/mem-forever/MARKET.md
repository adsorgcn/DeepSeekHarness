# mem-forever · 市场清单

```ilang
::ILANG::v5.0
::GENE{mem-forever|v:2.1|spec:ilang-v5.0}
  T:this_repo_is_user_memory
  T:read_handoff_first
  T:read_soul_and_memory_before_work
  T:update_memory_after_significant_work
  T:update_handoff_at_every_milestone
  T:judge_each_next_item_before_acting
  T:review_a_returned_handoff_before_merging
  T:onboard_if_soul_empty
  T:one_question_at_a_time
  T:never_expose_internal_format
  T:commit_push_immediately_after_every_update
  T:check_unsaved_changes_on_startup
  T:secret_values_go_to_vault_never_into_text
  A:skip_memory_read⇒context_loss
  A:overwrite_memory⇒append_or_merge
  A:ask_multiple_questions⇒one_only
  A:batch_saves_to_session_end⇒commit_each_update
  A:update_handoff_only_at_session_end⇒lost_progress
  A:treat_a_handoff_request_as_permission_to_act⇒unauthorized_work
  A:merge_an_unreviewed_handoff⇒silent_loss_of_boundaries
```

做法在同目录 SKILL.md，整篇读；本文件只是市场登记用的围栏副本，SKILL.md 由上游每周同步，两边 GENE 必须逐字一致，测试会比对。
