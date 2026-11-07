---
name: deai
version: 1.5.1
description: "去 AI 味与按作者画像写作的技能；默认 MARK 只标不写，基调层按读者估计加权，指纹是方言不是脏字 | Removes AI tone and writes in the author's own voice; MARK marks only by default, the tone layer is weighted by the reader estimate, and the fingerprint is dialect, never profanity."
author: ilang-ai
license: MIT
homepage: https://github.com/adsorgcn/DEAI
metadata:
  doi: 10.5281/zenodo.24028757
  upstream_tag: v1.5.1
---

```ilang
::ILANG::v5.0
::GENE{deai|v:1.5|spec:ilang-v5.0}
  T:user_asks_to_remove_ai_tone_or_to_write_like_themselves⇒load_this_skill
  T:follow_upstream_prompt_md_verbatim_as_the_procedure
  T:reader_estimate_is_printed_first_and_the_user_corrects_it_in_one_sentence
  T:model_marks_positions_for_colloquial_and_dialect_and_never_writes_them
  T:cases_are_written_only_at_high_confidence_and_always_inside_a_marker
  T:quotations_verbatim_with_author_and_work_or_dropped
  A:proposing_profanity_in_any_register⇒forbidden
  A:inventing_numbers_or_personal_experiences⇒forbidden
  A:applying_the_SUN_profile_to_a_user_who_did_not_name_it⇒forbidden
  A:editing_vendored_upstream_files⇒forbidden
```

## 什么时候用

用户说去 AI 味、说改得像我自己写的、或消息以 DeAI: 开头时，加载本技能。

## 怎么用

整篇读 upstream/prompt.md，把它当执行程序；用户的稿子按 DeAI: 前缀处理。输出第一行是读者估计，用户一句话可以改。默认 MARK 只标不写，基调层按读者估计加权；口语和方言只标位置，模型不写；指纹是方言不是脏字。

## PROFILE

只在用户给了自己的作者画像、或点名 profile=SUN 时，读 upstream/references/profile-mode-v1.2-2026-11-06.ilang.md 与对应画像文件。SUN 是作者本人的画像，是画像格式的样板，不是任何用户的声线。没有画像就只做 MARK，不假装学会了谁。

## 更新

换新 tag 时重新复制 upstream/ 并改 upstream.json，不手改任何上游文件。来源：https://github.com/adsorgcn/DEAI ，DOI 10.5281/zenodo.24028757
