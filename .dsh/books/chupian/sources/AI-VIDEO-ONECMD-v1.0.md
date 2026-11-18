[TYPE:engineering_book]
[ID:AI-VIDEO-ONECMD]
[VERSION:1.0]
[DATE:2026-11-06]
[LANG:en]
[NOTE:One command, one video. User tells Grok Bot what video they want in one sentence. Grok Bot runs the entire pipeline: story, storyboard, art style, frames, prompts, generation, post-production, delivery. User installs nothing. Structured from Eian (@EianLu) published workflow, verified against Seedance 2.0 mini and 2.5 capabilities.]
::STATE{@USER, role:director_and_approver, gives:one_sentence_idea_and_approvals_at_gates, does:watches_drafts_says_yes_or_gives_notes, never:writes_prompts_draws_frames_runs_tools_installs_anything}
::STATE{@GROK, role:total_producer, does:story_storyboard_art_frames_prompts_generation_post_delivery, has:codex_access_for_images_seedance_access_for_video_ffmpeg_python_for_post, manages:internal_review_agents_as_needed}
::STATE{@TOOLS, image_gen:Codex_or_equivalent, video_gen:Seedance_2.0_mini_default_or_2.5, post:ffmpeg_and_python_via_grok_environment, upscale:code_based_720p_to_1080p}
::STATE{@INPUT, FILL_IDEA:one_sentence_from_user, FILL_LENGTH:optional_target_seconds_default_30, FILL_BUDGET:optional_max_spend_default_minimize}
::STATE{@RESOLUTION, rule:if_user_has_premium_plus_generate_at_1080p_directly_otherwise_720p_then_upscale}
::OBJECTIVE{id:g1|owner:user|trust:trusted|version:1|status:active}
  target: deliver a complete short video from a one-sentence idea. User approves at three gates (story, storyboard, first test shot). Everything else is automatic.
  ACCEPT: every RUBRIC passes, user says the video is done
  NON_GOALS: teaching user filmmaking, requiring user to install tools, requiring user to write prompts, delivering raw assets without assembly
  DONE_WHEN: user has a playable final cut and says it is done
::BOUNDARY{never:generate_video_before_story_and_frames_are_approved|scope:permanent}
::BOUNDARY{never:use_text_only_prompts_for_video_always_provide_first_and_last_frame_images|scope:permanent}
::BOUNDARY{never:use_new_generation_output_as_reference_for_next_use_original_approved_reference|scope:permanent}
::BOUNDARY{never:rely_on_video_model_for_on_screen_text_overlay_in_post|scope:permanent}
::BOUNDARY{never:delete_any_generated_take_keep_all_versions|scope:permanent}
::BOUNDARY{never:regenerate_video_before_checking_if_edit_or_code_fix_can_solve_it|scope:permanent}
::BOUNDARY{always:cost_hierarchy_fix_in_text_first_then_in_image_then_regenerate_video_last|scope:permanent}
::BOUNDARY{always:verify_tools_available_before_starting_report_missing_tools_do_not_pretend|scope:permanent}
::MODULE{PREFLIGHT|title:Check tools and ask user three questions}
  [STEP] 1 verify available tools: image generation (Codex or equivalent), video generation (Seedance API via ARK_API_KEY), ffmpeg, Python. Report any missing tool, do not proceed until resolved or user chooses alternative.
  [STEP] 2 check user subscription: if Premium+ detected, set resolution_mode=1080p_direct. Otherwise set resolution_mode=720p_then_upscale.
  [STEP] 3 ask user only if not provided: target length (default 30s), aspect ratio (default 16:9), music preference (yes/no, if yes what mood), budget ceiling if any
  [STEP] 4 confirm to user: "[tools ready]. [resolution mode]. Tell me your idea in one sentence."
::MODULE{STORY|title:Turn one sentence into a verified story}
  [STEP] 1 take user's one-sentence idea, expand into complete story with: protagonist goal, main conflict, opening hook, ending
  [STEP] 2 structure preference: fragment-style (each shot independent, no continuity required between shots) is most stable for AI video. Use continuous narrative only if user specifically requests it.
  [STEP] 3 self-check story against five rules:
    [NOTE] RULE 1: every plot turn must follow real-world logic (unless user wants fantasy). Ask: why does this happen? Where does this object come from? Would this really happen?
    [NOTE] RULE 2: can summarize what the video is about in one sentence. If not, story is too scattered, simplify.
    [NOTE] RULE 3: most eye-catching moment is in the first 3 seconds. If opening is boring, restructure.
    [NOTE] RULE 4: bystander reactions must be staggered (not everyone reacts at the same time, that looks AI-generated). Write: person A first, then person B one second later, then person C.
    [NOTE] RULE 5: every shot must be something the video model can actually produce. Avoid: people crossing paths, hands holding small objects, text on screen, mirrors/reflections, asymmetric features, one person doing three actions in one shot, too many background characters.
  [STEP] 4 open a fresh internal review agent, give it ONLY the story (no context, no conclusions). Let it read as a first-time viewer and report: what it understood, what confused it, what felt unrealistic. Merge fixes.
  [STEP] 5 present story to user for approval. GATE 1: user says yes or gives notes. Do not proceed until approved.
::MODULE{STORYBOARD|title:Define every shot's camera, composition, and color}
  [STEP] 1 write shot table: one row per shot with columns: timestamp, generation_seconds (round up, add 0.5s buffer), shot_size (wide/medium/close-up), camera_position (eye-level/high/low/over-shoulder/through-object), camera_movement (pan/tilt/push/pull/static), who_moves_where (use screen left/right not character left/right), what_expression_drives_the_beat, how_this_shot_transitions_to_next
  [STEP] 2 camera rules:
    [NOTE] flat front eye-level maximum twice in entire video, rest must vary (high angle, low angle, over shoulder, through object, behind subject)
    [NOTE] every shot must have something moving: person entering/leaving frame, object drifting, camera pushing in. If nothing moves, the shot looks like a still image.
    [NOTE] do not repeat the same shot size consecutively (three close-ups in a row = boring). Alternate wide/medium/close-up.
    [NOTE] camera movement must have a reason: following an object, revealing something, emphasizing emotion. No movement for movement's sake.
    [NOTE] any frame frozen at any second must look good as a still image. Default composition: golden ratio (subject at 38% or 62% from left, not center).
  [STEP] 3 design color palette BEFORE drawing any frame. List exact colors per scene. Convert to black-and-white and check: if subject blends into background, contrast is too low, redesign palette.
  [STEP] 4 present storyboard to user. GATE 2: user approves or gives notes. Do not proceed until approved.

::MODULE{ART_STYLE|title:Lock visual style and draw character sheets}
  [STEP] 1 if user provided reference images: analyze style, extract: line quality, color treatment, texture, lighting approach
  [STEP] 2 if no reference: propose 2-3 style options (hand-drawn/flat color/realistic/American cartoon), let user pick
  [STEP] 3 write one-sentence style description that will be used in every prompt (e.g. "clean modern 2D hand-drawn animation, flat color blocks, crisp lines, no grain or texture")
  [STEP] 4 draw character sheet for each character: front view, side view, 3-4 expressions. Fixed features (tattoos, scars, accessories) must specify exact position (e.g. "tattoo on LEFT forearm") to prevent position drift across shots.
  [STEP] 5 draw key prop sheet if story has important objects
::MODULE{FRAMES|title:Draw first and last frame for every shot}
  [STEP] 1 before drawing, write out for each shot: what first frame shows, what last frame shows, what happens between them. Send to internal review agent for approval before spending image generation quota.
  [STEP] 2 draw last frame first (usually has more content), then modify last frame to create first frame. This ensures camera position and composition match between the two.
  [STEP] 3 for shots at the same location and camera angle: modify previous frame, do not redraw from scratch (Codex supports local image editing).
  [STEP] 4 if camera movement is push-in: last frame can be a crop+zoom of first frame. If first and last frame have identical composition, there will be no camera movement in the generated video.
  [STEP] 5 check all frames before proceeding:
    [NOTE] CHECK 1: any object used in the action must be visible in the first frame. If character picks up a cup later, cup must be in frame from the start.
    [NOTE] CHECK 2: bystander poses in first frame must be pre-positioned for their reaction. A 5-second clip cannot show someone going from relaxed to shocked if first frame shows them already shocked.
    [NOTE] CHECK 3: first frame and last frame must have same number of people, same props, same clothing, same background elements. Count everything.
    [NOTE] CHECK 4: aspect ratio must match target (16:9). Crop before submitting. First and last frame must be same dimensions.
    [NOTE] CHECK 5: verify against character sheet: face consistent, accessories in correct position, clothing matches.
  [STEP] 6 open internal review agent, give it: both frames + character sheet + storyboard row. Agent checks all five points above. Must say "pass" before submitting to video generation. This is the last checkpoint before spending money.
::MODULE{PROMPTS|title:Write seven-section video prompts}
  [STEP] 1 every video prompt uses this fixed structure:
    [NOTE] SECTION 1 [ART STYLE]: one-sentence style description from ART_STYLE module. Add: "entire clip's style, color, and character design are identical to first and last frame."
    [NOTE] SECTION 2 [SHOT]: total seconds, shot size, camera position, camera movement (if static write "no push no pull no pan no tilt, no cut").
    [NOTE] SECTION 3 [COMPOSITION AND COLOR]: where people and objects are in frame, wall and light colors. Must match first frame exactly.
    [NOTE] SECTION 4 [CHARACTERS]: each person's appearance, clothing, fixed features, exact starting position and pose. Reference character sheet.
    [NOTE] SECTION 5 [ACTION TIMELINE]: second-by-second what happens. One or two main actions maximum per shot. Stagger reactions (person A first, person B one second later).
    [NOTE] SECTION 6 [MUST MAINTAIN]: list everything that must stay constant throughout (number of people, specific props, clothing details, weather, lighting).
    [NOTE] SECTION 7 [MUST NOT HAPPEN]: list specific unwanted behaviors. Use POSITIVE language ("hands stay at sides throughout" not "do not move hands"). Negative instructions often fail.
  [STEP] 2 common model errors to prevent in prompt writing:
    [NOTE] multiple people doing same action simultaneously → write who does what first, who follows
    [NOTE] wind/weather doing human actions (mailman using hands to open bag when wind should do it) → write "hands never touch the bag" AND specify what causes the action
    [NOTE] clouds/moon/plants growing faces → never write "cartoon cloud", write "puffy gray-white cumulus with only cotton-like texture and shadow"
    [NOTE] person walking wrong direction → write screen direction: "walks toward screen left, crosses the door on the left side"
    [NOTE] ambiguous descriptions → be specific: "old man inside the stone house window, upper left" not "the person behind the window"
    [NOTE] object count changing → write exact numbers: "only one yellow envelope, then his arms are full of white envelopes"
    [NOTE] objects appearing from nowhere → only use objects already visible in first frame
    [NOTE] objects teleporting → describe full motion path: "hat slides back along the head, he catches it behind, puts it back on"
    [NOTE] rain/hat/tattoo disappearing mid-shot → draw them in BOTH first and last frame
    [NOTE] character's mouth moving when no dialogue → write "character does not speak" explicitly
    [NOTE] music appearing when not wanted (Seedance 2.5) → plan to strip audio in post, add sound separately
    [NOTE] last frames jumping to end-frame position (Seedance 2.5) → in post, freeze on a good frame, cut the jump
    [NOTE] first frame overly sharp (Seedance 2.5) → remove first frame in post
  [STEP] 3 open internal review agent with: prompt + first frame + last frame + character sheet + storyboard + color rules. Agent checks every word against both images. Must say "pass" before submission. This is real money.
::MODULE{GENERATE|title:Submit to Seedance and manage takes}
  [STEP] 1 resolution: if resolution_mode=1080p_direct, generate at 1080p. If resolution_mode=720p_then_upscale, generate at 720p (saves ~60% cost per shot).
  [STEP] 2 model selection: Seedance 2.0 mini for standard shots (cheaper, audio often usable). Seedance 2.5 for complex shots requiring higher fidelity (3x cost of 2.0 mini). Default to 2.0 mini unless shot complexity demands 2.5.
  [STEP] 3 test with hardest shot first. If it works, remaining shots will likely work. If it fails, fix approach before burning budget on easier shots.
  [STEP] 4 submit shot with first frame + last frame + prompt. Wait for result.
  [STEP] 5 review each take three passes: (1) character consistency (2) spatial continuity and action (3) sound only
  [STEP] 6 if take has problems, check in this order before regenerating:
    [NOTE] can the problem be cut away? (bad first/last frames → trim them)
    [NOTE] can code fix it? (slight color drift → code correction, mouth moving → code patch, camera not pushing enough → code zoom)
    [NOTE] only regenerate if edit and code both fail. Before regenerating, CHANGE the prompt or the frame. Same inputs = same output.
  [STEP] 7 keep ALL takes including failed ones. Failed takes may have usable segments.
  [STEP] 8 track budget: running total after each generation. Alert user if approaching budget ceiling.
::MODULE{POST|title:Assemble, transition, color grade, upscale, deliver}
  [STEP] 1 assemble all approved takes in shot order using ffmpeg via code
  [STEP] 2 transitions: motion-blur cuts at 8-16 segments, half-shutter. Match transition style to story beats, not random.
  [STEP] 3 color grading: adjust saturation and brightness only, do not shift hue. Protect accent colors and skin tones. No grain, no soft glow, no vignette.
  [STEP] 4 if resolution_mode=720p_then_upscale: upscale to 1080p using code-based super-resolution
  [STEP] 5 audio: Seedance 2.0 mini audio is often usable (ambient sound effects). Seedance 2.5 may inject unwanted music even when told not to → strip audio, add effects separately. If user requested music, add music track aligned to story beats.
  [STEP] 6 text overlays: any on-screen text is added in post with code, never generated by video model. Same text asset used everywhere the same prop appears.
  [STEP] 7 subtitle timing: align to actual speech timing in rendered video, not script timing
  [STEP] 8 rough cut review: check four things:
    [NOTE] action continuity: does a reaching hand repeat across cuts?
    [NOTE] dialogue completeness: any words cut off? Subtitles readable in time?
    [NOTE] ambient sound: door sound when no door moved? Rain stopping abruptly?
    [NOTE] music: too loud during dialogue? Sudden cut on scene transition?

::MODULE{REVIEW|title:Fresh-eyes review of final cut}
  [STEP] 1 open fresh internal review agent. Give it ONLY the final video file. No story, no storyboard, no conclusions.
  [STEP] 2 agent watches as first-time viewer: writes what story it understood, lists anything confusing
  [STEP] 3 agent does frame-by-frame check: repeated actions, prop count changes, continuity breaks, color jumps, face deformation, text errors
  [STEP] 4 agent outputs: confirmed issues (with timestamps) and suspected issues (with timestamps). Clear distinction.
  [STEP] 5 fix confirmed issues. Suspected issues: check manually, fix if real.
  [STEP] 6 show final cut to user. GATE 3: user approves or gives notes.
  [STEP] 7 if user approves: proceed to DELIVER. If notes: fix and re-review.
::MODULE{DELIVER|title:Final deliverables}
  [LINE] 1. final video file: [format] [duration] [resolution]
  [LINE] 2. total spend: [amount] (breakdown per shot/version)
  [LINE] 3. version history: all takes preserved
  [LINE] 4. project folder: story / storyboard / character sheets / color palette / all frames / all takes / final cut / budget log / lessons learned
  [LINE] 5. lessons learned file: art style description, prompt patterns that worked, errors encountered and fixes, for next video
::RUBRIC{R1: user provided only one-sentence idea and approvals at three gates, everything else was automatic|check:human}
::RUBRIC{R2: story approved before any image generation|check:human}
::RUBRIC{R3: storyboard approved before any frame drawing|check:human}
::RUBRIC{R4: every video shot had first AND last frame, no text-only prompts|check:automated}
::RUBRIC{R5: internal review agent approved frames before every video submission|check:automated}
::RUBRIC{R6: all references used original approved images, never chained generation outputs|check:automated}
::RUBRIC{R7: no on-screen text generated by video model, all text overlaid in post|check:human}
::RUBRIC{R8: resolution matches user subscription (P+ = 1080p direct, otherwise 720p upscaled)|check:automated}
::RUBRIC{R9: cost hierarchy followed (text fix > image fix > code fix > regenerate)|check:human}
::RUBRIC{R10: all takes preserved including failed ones|check:automated}
::RUBRIC{R11: fresh review agent saw final cut without any prior context|check:automated}
::RUBRIC{R12: total spend within budget ceiling|check:automated}
::FALLBACK{tool_not_available⇒report_to_user_and_wait_do_not_pretend|codex_quota_exhausted⇒pause_image_work_resume_when_quota_resets_do_not_switch_to_inferior_tool|seedance_generation_fails⇒change_prompt_or_frame_then_retry_never_retry_same_inputs|budget_ceiling_approaching⇒alert_user_with_remaining_amount_and_remaining_shots|story_review_agent_finds_major_issues⇒fix_before_proceeding_do_not_skip_review|color_drift_across_shots⇒fix_each_shot_to_match_its_own_first_frame_color_in_post|user_not_satisfied_after_3_review_rounds⇒pause_and_reassess_story_or_storyboard_not_generation_parameters}
::PRIORITY{ BOUNDARY > user_approval_at_gates > cost_efficiency > story_quality > visual_consistency > resolution > speed }
::FACT{key:cost_reference|value:seedance_2.0_mini_is_baseline_2.5_is_3x_cost_720p_saves_60_percent_vs_1080p|conf:confirmed}
::FACT{key:reference_discipline|value:always_use_original_approved_reference_never_chain_outputs|conf:confirmed}
::FACT{key:fragment_structure|value:fragment_style_story_most_stable_for_AI_video_each_shot_independent|conf:confirmed}
::FACT{key:model_audio|value:2.0_mini_audio_often_usable_2.5_may_inject_music_even_when_told_not_to_strip_and_replace|conf:confirmed}
::FACT{key:prompt_format|value:seven_section_fixed_structure_style_shot_composition_characters_timeline_maintain_must_not|conf:confirmed}
::FACT{key:review_principle|value:fresh_agent_no_context_catches_what_main_agent_misses_because_main_agent_knows_intent_and_fills_gaps|conf:confirmed}
::FACT{key:source|value:structured_from_EianLu_published_workflow_2026-11-05|conf:confirmed}
