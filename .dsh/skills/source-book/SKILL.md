---
name: source-book
version: 2.9
description: "把攻略、教程变成 AI 能照着执行的工程书：贴来一篇攻略、一个链接或一张截图，说一句「变工程书」 | Turns any tutorial or guide into an iLang engineering book an agent can carry out end to end"
whenToUse: "用户说「变工程书」「出工程书」，或贴来攻略、教程、链接、截图，要 AI 以后照着做时加载；用户说「照这本书做」并指着 books/ 下的一本书时也加载。"
author: ilang-ai
license: MIT
homepage: https://ilang.ai/source-book/
metadata:
  doi: 10.5281/zenodo.21821452
  upstream_tag: v5.0.14
---

```ilang
::ILANG::v5.0
::GENE{source-book|v:2.9|spec:ilang-v5.0}
  T:user_hands_over_a_tutorial_and_says_make_it_a_book⇒load_this_skill
  T:follow_the_source_book_in_.github/bot_verbatim_as_the_procedure
  T:the_tutorial_is_whatever_the_user_pasted_linked_or_screenshotted
  T:the_grammar_checker_already_sits_in_the_kit_at_tools/ilang_grammar_validator.py
  T:each_book_is_saved_in_its_own_folder_under_books_in_the_workspace
  T:user_says_carry_out_this_book⇒read_that_BOOK.md_and_do_what_it_says
  A:doing_the_tutorial_while_writing_the_book⇒forbidden
  A:copying_the_tutorial_s_numbers_prices_or_earning_claims_into_the_book⇒forbidden
  A:editing_the_source_book_or_filling_its_blanks_before_the_user_gives_the_tutorial⇒forbidden
  A:putting_a_book_on_any_shelf_or_pushing_it_anywhere_without_the_owner_s_word⇒forbidden
```

## 什么时候用

用户贴来一篇攻略或教程，或者给一个链接、一张截图，说「变工程书」，加载本技能。用户说「照这本书做」，也加载本技能。

## 变工程书

母版就是随工具包带着的那一份，在 `.github/bot/` 下，文件名看 `.github/bot/MOTHER.source.txt` 的 file 那一行。它是 gzip 压着的，用 python 的 gzip 模块按 UTF-8 解开，整篇读完。

把解开的全文原样当作你的执行程序，一个字不改，照它做：

- 它要的 tutorial 就是用户给的那篇攻略：贴的文字、链接或截图。用户没给，就用一句话问他要。
- 它要的 user language 看用户用什么语言跟你说话。
- 它要的工作目录填当前工作区下的 `books/<给这本书起的英文短名>/`，没有就建。
- 它让你取语法校验器：工具包里已经有 `tools/ilang_grammar_validator.py`，线上取不到就用这一份。
- 回复的格式照母版写的来，不多一句不少一句。

写书的时候不替用户做攻略里的事。攻略里的数字、价格、收入不照抄，在官方来源核实过的才写进书里。

## 照这本书做

用户说「照这本书做」：读他指的那本 `books/<名字>/BOOK.md`，没指就用最新写的那一本，把它当作执行程序照着做。书里留给用户填的空先问他；要他决定、授权、付款的地方停下来等他。

用户想让 Grok Bot 来做：告诉他把那本 BOOK.md 拖进 Bot 的聊天，说一句「照这本书做」。

## 更新

母版只有 `.github/bot/` 下那一份，和仓库里的客服机器人共用，来源和哈希记在 `MOTHER.source.txt`。换新版时换那一份并改那一行哈希，不手改原文。来源：https://ilang.ai/source-book/ ，仓库 https://github.com/ilang-ai/ilang-spec 的 products/source-book/。
