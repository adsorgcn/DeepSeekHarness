# DSH 本地补充（DeepSeekHarness 适配版）

AGENTS.md 本体保持与上游 Mem-Forever 一致；本文件是本仓库对 DSH 的补充，由 DSH 的 agent-instructions 作为附加覆盖自动加载。

::GENE{dsh_working_form|conf:confirmed|scope:global}
  T:index_is_addressing_not_storage
  T:judge_before_recording_reversible_work_is_not_recorded
  T:attention_not_flat
  T:cache_first_stable_prefix_tail_only_dynamics
  T:cross_validate_experience_with_ilang_canon
  A:pretending_to_see_an_image⇒switch_model_to_flash_and_say_so
  A:negative_claim_without_three_layer_check⇒recheck

::GENE{dsh_network_and_privacy|conf:confirmed|scope:global}
  T:github_unreachable⇒product_source_switches_to_gitee_mirror
  T:ilang_primary_unreachable⇒read_ilang_cn_and_name_the_source
  T:domestic_mirror_is_for_product_source_only_never_for_private_memory_backup
  T:private_memory_push_requires_an_owner_confirmed_private_repo
  A:push_soul_memory_handoff_to_a_public_remote⇒blocked_by_pre_push_guard
  A:claim_a_domestic_mirror_is_latest_without_checking_version⇒recheck

::GENE{dsh_decision_flow|conf:confirmed|scope:global}
  T:agent_judges_do_or_not_before_asking
  T:agent_does_all_the_thinking_and_presents_only_the_choice
  T:agent_states_its_choice_with_reason_and_default
  T:owner_replies_only_do_or_pass
  T:safe_reversible_default_proceeds_without_blocking
  A:open_question_to_owner⇒rephrase_as_judgment_with_recommendation
  A:making_owner_do_the_analysis⇒agent_rethinks_and_presents_the_decision_ready
  A:blocking_on_owner_choice_with_a_safe_default⇒rejudge_and_proceed
  A:treating_install_push_delete_or_network_write_as_a_safe_default⇒stop_and_ask_first

（owner 决策流：思考全部由 agent 完成，只把结论与推荐摆到 owner 面前；owner 零思考，只回答「做」或「过」，不再回答开放式问题。）

::GENE{dsh_memory_mode|conf:confirmed|scope:global}
  T:local_mode_commit_only_never_push
  T:local_mode_reply_is_saved_locally_never_mentions_push
  T:engine_update_never_touches_memory_files
  T:backup_mode_remote_named_backup_private_repo_only
  A:push_in_local_mode⇒blocked_push_url_is_DISABLED
  A:guiding_repo_creation_in_local_mode⇒violates_the_copy_paste_flow

（本机模式：git config dsh.mode 为 local 时只 commit 不 push，保存成功说「已存在本机」，不提 push、不引导建仓库；上游「push 失败就提示稍后 git push」在本机模式不适用。备份：用户说备份，先问一次「要在 GitHub 建一个空的私有仓库，建吗」，点头后 remote 用 backup 不用 origin，git config dsh.mode backup、git config dsh.allowMemoryPush true，之后每次保存推 backup；公开地址或非私有仓库一律拒绝。）

::GENE{dsh_engine_update|conf:confirmed|scope:global}
  T:update_only_the_engine_files_never_soul_memory_handoff_vault_env_projects_mirror_log
  T:recheck_with_brain_check_before_and_after_the_update
  T:reinstall_guard_pre_push_hook_after_the_update
  A:touching_memory_files_during_an_engine_update⇒forbidden
  A:updating_when_citation_version_is_unchanged⇒reply_already_latest_and_stop

（引擎更新：「把 DeepSeekHarness 的引擎更新到最新，不要动我的记忆」的做法：git fetch origin main（fetch 地址按 git config dsh.source 是 github 或 gitee）→ git checkout FETCH_HEAD -- tools rules skills .dsh docs AGENTS.md AGENTS.local.md CLAUDE.md GEMINI.md BRAIN.md bootstrap.ps1 bootstrap.sh CITATION.cff .zenodo.json README.md ROADMAP.md CHANGELOG.md 一键安装.md dsh-新手起手式.md .github → 永远不碰 soul memory handoff vault env projects mirror log.md index.md → 更新前后各跑一次 brain.py check → 重新复制 tools/guard-pre-push.sh 到 .git/hooks/pre-push → 把两次 CITATION 版本号写进交接单并 commit；CITATION 版本相同就说「已是最新」不做事。）
