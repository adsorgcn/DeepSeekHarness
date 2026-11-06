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

::GENE{dsh_free_station|conf:confirmed|scope:global}
  T:free_station_installs_only_via_tools_free_station_py
  T:every_free_station_item_needs_owner_approval_before_install
  T:official_sources_only_for_every_free_station_item
  T:voice_uses_dsh_builtin_stt_and_system_tts_zero_install
  A:installing_free_station_tools_outside_the_registry⇒forbidden
  A:adding_a_free_station_tool_without_a_verify_command⇒forbidden

（免费全家桶：只走 tools/free_station.py 读 .dsh/free-station.json；每件先问、只走官方源、失败即停；语音与笔记零安装集成；新工具=注册表加一条目+发 patch。）

::GENE{dsh_vision_routing|conf:confirmed|scope:global}
  T:vision_task_recognized_from_kan_jietu_or_kan_jiantieban_or_image_path
  T:vision_on_image_capable_model_use_read_image_directly
  T:vision_on_text_only_model_use_clip_shot_then_flash_subagent_with_read_image_prompt
  T:continue_on_current_model_after_flash_child_returns_never_mention_switching
  T:renzhenxiang_on_flash_main_model_spawns_Pro_subagent_and_tells_the_user
  T:web_questions_use_builtin_web_search_and_web_fetch
  A:asking_the_user_to_switch_model⇒forbidden
  A:image_pasted_into_the_composer_on_a_text_only_model⇒reply_one_line_screenshot_then_say_kan_jietu
  A:flash_route_missing_in_list_subagent_models⇒offer_the_two_switch_ways_and_stop_until_the_user_says_yes
  A:editing_the_dsh_profile_without_an_explicit_yes_in_this_conversation⇒forbidden
  A:clip_shot_prints_no_image⇒say_screenshot_first_then_kan_jietu_and_stop

（视觉路由：用户说「看截图」「看剪贴板」或给图片路径 = 视觉任务。本模型能读图就直接 read_image；不能读图时——若图在剪贴板先跑 tools/clip_shot.ps1 或 tools/clip_shot.sh 拿到路径（NO_IMAGE 就提示先截图再停），再调 list_subagent_models：没有 deepseek-flash 路由就把两种开法原文给用户选，用户说「好」才动、不说不动——甲、用户自己在 DSH 插件页打开「子代理模型选择」并加入 deepseek-flash 与 deepseek-v4-pro；乙、经用户同意后往 $DSH_HOME/profiles/<当前 profile>/cordis.patch.yml 追加：- id: subagent-model-selection-settings，name: \"@deepseek-ai/dsh-tool-subagent/model-selection-settings\"，config: enabled: true，allowedModels: [{provider: <当前路由的 provider>, model: deepseek-flash}, {provider: <当前路由的 provider>, model: deepseek-v4-pro}]（provider 取 list_subagent_models 返回的当前路由，不要猜）。开完请用户重开会话，再调一次 list_subagent_models，看到两条路由才算开成，没看到就把返回原文给用户，不猜原因。有 flash 路由就派 deepseek-flash 子代理（provider 同上）read_image 并回报文字；它回来后在本模型继续，绝不提切模型。flash 主模型遇「认真想」派 deepseek-v4-pro 子代理并把任务与相关文件路径给它、告知用户 Pro 在干活。贴图在纯文本模型被拒就答「截图后直接说看截图，不用贴」。web 一律 builtin web_search 与 web_fetch。未获本会话明确同意绝不改 DSH profile。）
