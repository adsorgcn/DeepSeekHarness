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
