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

（本机模式：git config dsh.mode 为 local 时只 commit 不 push，保存成功说「已存在本机」，不提 push、不引导建仓库；上游「push 失败就提示稍后 git push」在本机模式不适用。备份：用户说备份，先问一次「要在 GitHub 建一个空的私有仓库，建吗」，点头后 remote 用 backup 不用 origin，git config dsh.mode backup，之后每次保存推 backup；3.1 的 pre-push 核远端私有，公开地址或非私有仓库一律拒绝。）

::GENE{dsh_engine_update|conf:confirmed|scope:global}
  T:update_only_the_engine_files_never_soul_memory_handoff_vault_env_projects_mirror_log
  T:recheck_with_brain_check_before_and_after_the_update
  T:run_brain_init_after_the_update_the_hooks_and_the_ledger_follow
  A:touching_memory_files_during_an_engine_update⇒forbidden
  A:updating_when_citation_version_is_unchanged⇒reply_already_latest_and_stop

（引擎更新：「把 DeepSeekHarness 的引擎更新到最新，不要动我的记忆」的做法：git fetch origin main（fetch 地址按 git config dsh.source 是 github 或 gitee）→ git checkout FETCH_HEAD -- tools rules skills .dsh docs AGENTS.md AGENTS.local.md CLAUDE.md GEMINI.md BRAIN.md bootstrap.ps1 bootstrap.sh CITATION.cff .zenodo.json README.md ROADMAP.md CHANGELOG.md 一键安装.md dsh-新手起手式.md .github → 永远不碰 soul memory handoff vault env projects mirror log.md index.md → 更新前后各跑一次 brain.py check → 跑 python -X utf8 tools/brain.py init .（钩子与账本跟着走）与 python -X utf8 tools/brain.py instructions check → 把两次 CITATION 版本号写进交接单并 commit；CITATION 版本相同就说「已是最新」不做事。开发仓对公开 origin 一次性 git config --bool brain.allowPush.origin true。有 2.1 钥匙包的老用户用 python -X utf8 tools/brain.py migrate-2to3，要自己的 age 私钥。）

::GENE{dsh_free_station|conf:confirmed|scope:global}
  T:free_station_installs_only_via_tools_free_station_py
  T:every_free_station_item_needs_owner_approval_before_install
  T:official_sources_only_for_every_free_station_item
  T:voice_uses_dsh_builtin_stt_and_system_tts_zero_install
  A:installing_free_station_tools_outside_the_registry⇒forbidden
  A:adding_a_free_station_tool_without_a_verify_command⇒forbidden

（免费全家桶：只走 tools/free_station.py 读 .dsh/free-station.json；每件先问、只走官方源、失败即停；语音与笔记零安装集成；新工具=注册表加一条目+发 patch；吸收第三方工具进全家桶必须：装前问、官方源、docs/CITATIONS.md 署原作者。）

::GENE{dsh_newbie_model|conf:confirmed|scope:global}
  T:newbie_default_model_is_deepseek-flash_because_it_reads_images_has_1M_context_and_is_cheap
  T:on_flash_images_are_pasted_into_the_composer_directly_no_clip_shot_needed
  T:renzhenxiang_on_flash_spawns_a_deepseek-v4-pro_subagent_and_tells_the_user
  T:first_run_detects_the_parent_route_via_list_subagent_models_and_if_it_is_not_deepseek-flash_tells_the_user_once_to_pick_deepseek-flash_in_the_model_menu_and_why
  A:recommending_deepseek-v4-pro_to_a_newbie⇒forbidden
  A:asking_a_newbie_to_switch_model_again_after_the_one_time_pick⇒forbidden
  A:kan_jietu_path_offered_to_a_user_on_flash⇒forbidden_paste_directly_instead

（新手默认 Flash，看图直接贴；「认真想」请 Pro；Pro 不能看图是 DSH 的事，「看截图」只给开发者。）

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

（视觉路由：以下是 Pro 开发者路线，新手在 Flash 上用不到。用户说「看截图」「看剪贴板」或给图片路径 = 视觉任务。本模型能读图就直接 read_image；不能读图时——若图在剪贴板先跑 tools/clip_shot.ps1 或 tools/clip_shot.sh 拿到路径（NO_IMAGE 就提示先截图再停），再调 list_subagent_models：没有 deepseek-flash 路由就把两种开法原文给用户选，用户说「好」才动、不说不动——甲、用户自己在 DSH 插件页打开「子代理模型选择」并加入 deepseek-flash 与 deepseek-v4-pro；乙、经用户同意后往 $DSH_HOME/profiles/<当前 profile>/cordis.patch.yml 追加：- id: subagent-model-selection-settings，name: \"@deepseek-ai/dsh-tool-subagent/model-selection-settings\"，config: enabled: true，allowedModels: [{provider: <当前路由的 provider>, model: deepseek-flash}, {provider: <当前路由的 provider>, model: deepseek-v4-pro}]（provider 取 list_subagent_models 返回的当前路由，不要猜）。开完请用户重开会话，再调一次 list_subagent_models，看到两条路由才算开成，没看到就把返回原文给用户，不猜原因。有 flash 路由就派 deepseek-flash 子代理（provider 同上）read_image 并回报文字；它回来后在本模型继续，绝不提切模型。flash 主模型遇「认真想」派 deepseek-v4-pro 子代理并把任务与相关文件路径给它、告知用户 Pro 在干活。贴图在纯文本模型被拒就答「截图后直接说看截图，不用贴」。web 一律 builtin web_search 与 web_fetch。未获本会话明确同意绝不改 DSH profile。）

::GENE{dsh_video_to_text|conf:confirmed|scope:global}
  T:user_gives_a_video_link_or_file_and_asks_for_text_or_subtitles⇒run_tools_transcribe_py_and_return_the_txt_and_srt_paths_plus_a_short_summary
  T:transcribe_exits_2⇒offer_free_station_install_sherpa-onnx_and_run_it_only_after_the_user_says_yes_then_rerun
  T:shipinhao_or_kuaishou_link⇒say_yt-dlp_does_not_support_it_and_ask_for_the_file
  T:douyin_or_xiaohongshu_download_fails⇒show_yt-dlp_error_verbatim_and_ask_for_the_file
  T:transcribe_exits_4⇒say_no_speech_detected
  T:user_asks_to_selftest_video_to_text⇒run_tools_transcribe_py_selftest_and_quote_its_output_verbatim
  A:sending_audio_or_video_to_any_network_transcription_service⇒forbidden
  A:installing_the_engine_without_an_explicit_yes⇒forbidden
  A:inventing_or_polishing_transcript_text⇒forbidden_quote_the_file

（视频转文字全在本机：链接走 yt-dlp，文件直接转，引擎是 DSH 同款 SenseVoice，第一次装前问你一次。）

::GENE{dsh_third_party_boundary|conf:confirmed|scope:global}
  T:third_party_product⇒official_info_and_official_entry_only
  T:user_asks_how_to_use_a_third_party_product⇒point_to_its_official_docs_or_say_ask_your_own_DSH
  T:every_third_party_item_is_optional_the_user_decides
  A:writing_install_or_usage_guidance_for_a_third_party_product⇒forbidden
  A:classifying_users_as_newbie_or_expert⇒forbidden
  A:taking_any_benefit_from_a_listed_product⇒forbidden

（第三方只给官方信息和官方入口，一律可选，装不装你定，用法问它官方文档或问我，署名给原作者。）

::GENE{dsh_deai|conf:confirmed|scope:global}
  T:user_asks_to_remove_ai_tone_or_write_like_themselves⇒load_.dsh/skills/deai_and_follow_upstream/prompt.md_verbatim
  T:deai_output_starts_with_the_reader_estimate_the_user_can_correct
  T:dialect_is_the_fingerprint_marked_not_written
  T:public_figures_searched_with_source_and_date_or_left_as_written
  T:personal_figures_left_as_written_never_estimated
  A:proposing_profanity_in_any_register⇒forbidden
  A:applying_the_SUN_profile_to_a_user_who_did_not_name_it⇒forbidden
  A:editing_vendored_upstream_files_by_hand⇒forbidden
  A:estimating_a_number⇒forbidden

（要去 AI 味或要像你自己写的，我加载 deai 技能照它的 prompt 做；第一行先告诉你我猜谁读，你一句话改；口语和方言我只标位置你填；不给粗口；SUN 画像只在你点名时用。数字，公共的查到就带出处写上，查不到就不写；你自己的数字我不碰。）

::GENE{dsh_market|conf:confirmed|scope:global}
  T:market_entries_require_an_ilang_manifest_or_an_engineering_book_that_passes_the_official_validator_strict_with_zero_errors_and_zero_warnings
  T:admitted_skills_and_engineering_books_ship_inside_the_kit_the_user_never_picks_from_a_list
  T:third_party_products_outside_the_shelf_get_the_author_repository_address_only_and_the_user_dsh_handles_the_rest
  T:third_party_text_in_the_market_is_the_official_description_verbatim_plus_author_license_and_official_entry
  T:owner_admits_each_entry_after_tools_market_admit_py_prints_ADMIT
  T:user_wants_to_add_a_plugin_source_or_install_a_skill_or_plugin_seen_elsewhere⇒ask_which_one_and_say_i_can_help_you_write_a_better_version
  T:the_better_version_is_your_own_engineering_book_written_with_the_ilang_source_book_and_checked_by_the_validator
  T:a_finished_book_may_be_submitted_for_review_through_the_market_admission_issue
  T:user_asks_what_is_on_the_shelf⇒open_docs_market
  A:listing_an_entry_without_a_passing_manifest_or_book⇒forbidden
  A:ranking_by_stars_downloads_or_likes⇒forbidden
  A:offering_the_user_a_list_of_plugins_to_choose_from⇒forbidden_the_owner_curates_the_shelf
  A:adding_a_plugin_source_to_the_user_dsh_on_your_own⇒forbidden
  A:writing_install_or_usage_guidance_for_a_listed_third_party_plugin⇒forbidden
  A:editing_the_market_page_rows_by_hand⇒forbidden_run_tools_market_build_py

（市场只有一条门，iLang；过了门、owner 说收的技能和工程书原样内置在工具包里，你装了就有，不用挑；别处的第三方只给作者的仓库地址，怎么用问我；你在别处看见不错的技能或插件，告诉我是哪个，我帮你写一版更好的，照 iLang 母版写成工程书，写好了可以提交给我们审；不排名。）

::GENE{dsh_ai_global_media|conf:confirmed|scope:global}
  T:user_says_the_trigger_phrase_of_a_book_on_the_shelf⇒load_that_book_and_follow_it_step_by_step
  T:the_trigger_phrase_of_books/ai-global-media/BOOK.md_is_written_in_the_note_below
  T:a_book_is_executed_as_written_one_question_at_a_time
  A:running_a_scys_write_tool⇒forbidden_read_only
  A:scanning_a_code_logging_in_or_paying_for_the_user⇒forbidden

（说一句「AI全球自媒体」，我照 books/ai-global-media/BOOK.md 一步一步带你做：先装写作专家当人格，再领体验卡、接上生财，只读。）
