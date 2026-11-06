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

（owner 决策流：思考全部由 agent 完成，只把结论与推荐摆到 owner 面前；owner 零思考，只回答「做」或「过」，不再回答开放式问题。）
