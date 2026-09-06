# Vim Golf

Dated Neovim editing challenges. Each challenge starts from a small config tree
and has one exact target. `play` creates a persistent worktree outside the repo,
opens it with your Neovim config, validates it on exit, and records the raw bytes
Neovim wrote to its input log. The byte count is a personal trend, not a portable
VimGolf score. Special keys can occupy more than one byte.

```bash
./vim-golf list
./vim-golf play 2026-08-19
./vim-golf check 2026-08-19
./vim-golf diff 2026-08-19
./vim-golf reset 2026-08-19
```

A challenge is named by its full date (`challenges/YYYY-MM-DD`). A bare day number
resolves against the current month; omitting the day selects today. Run `show DAY`
to reread the task. Day 2026-08-26 has an explicit `copy` step that puts its
payload on the macOS pasteboard.

The target files are committed under each day's `expected/` directory for
deterministic validation. Looking at them before solving the task defeats the
exercise.

`VIMGOLF_CHALLENGES_DIR` overrides the challenges directory;
`VIMGOLF_STATE_DIR` overrides the work/score state directory
(default `~/.local/state/vim-golf`).

## Setup-specific rules

- `d`, `c`, `x`, `s`, and their uppercase forms use the black-hole register in your mappings.
- `y`, `p`, and `P` are provided by Yanky. `<leader>p` opens yank history, and `[y` or `]y` cycles
  the most recent put through that history.
- `clipboard=unnamedplus` makes the unnamed register share the macOS pasteboard.
- `s` and `S` replace LazyVim's default Flash bindings after `VeryLazy`. The course does not claim
  Flash is available on those keys.
- LazyVim remaps bare `j` and `k` to display-line movement. Counts such as `8j` still move by file
  lines.

## Curriculum

Start each session with five minutes in `:VimBeBetter`, using the named game, then run the dated
challenge.

### August 2026

Days 1 through 18 are the ramp: core mechanics one at a time, each day one tool. Days 19 through 31 assume the ramp and
combine tools. Grinding several ramp days in one sitting works; they are sized at three to five edits each.

| Date       | Focus                                                      | VimBeBetter warm-up  |
|------------|------------------------------------------------------------|----------------------|
| 2026-08-01 | survival keys, counts, insert, replace-char, undo          | `hjkl`               |
| 2026-08-02 | linewise yank, put, delete, open                           | `words`              |
| 2026-08-03 | case operators and dot repeat                              | `case-converter`     |
| 2026-08-04 | joining lines                                              | `join-lines`         |
| 2026-08-05 | indent operators                                           | `indent-master`      |
| 2026-08-06 | increment and decrement                                    | `increment-game`     |
| 2026-08-07 | paragraph text objects                                     | `text-objects-basic` |
| 2026-08-08 | comment toggling as an operator                            | `comment-toggle`     |
| 2026-08-09 | insert-mode editing keys                                   | `speed-editing`      |
| 2026-08-10 | ranged `:s` substitute                                     | `substitute-basic`   |
| 2026-08-11 | replace mode, column-preserving edits                      | `visual-precision`   |
| 2026-08-12 | inside vs around text objects                              | `ci`                 |
| 2026-08-13 | whole-word search with selective landings                  | `word-boundaries`    |
| 2026-08-14 | yanking blocks across the file                             | `relative`           |
| 2026-08-15 | reusing the last insertion                                 | `dot-repeat`         |
| 2026-08-16 | yank register vs black-hole deletes                        | `refactor-race`      |
| 2026-08-17 | undo tree as navigation                                    | `whackamole`         |
| 2026-08-18 | ramp capstone, tool choice per edit                        | `vim-golf`           |
| 2026-08-19 | word and line motions, operator plus motion                | `word-boundaries`    |
| 2026-08-20 | `f`, `F`, `t`, `T`, `;`, `,`, quote text objects           | `find-char`          |
| 2026-08-21 | `/`, `n`, `N`, `*`, `cgn`, dot repeat                      | `dot-repeat`         |
| 2026-08-22 | delimiter text objects and `%`                             | `text-objects-basic` |
| 2026-08-23 | `gg`, `G`, counts, `{`, `}`, marks, jump list              | `relative`           |
| 2026-08-24 | counts, dot repeat, linewise operations                    | `dot-repeat`         |
| 2026-08-25 | visual block edits for aligned config                      | `visual-precision`   |
| 2026-08-26 | macOS pasteboard and unnamed register                      | `speed-editing`      |
| 2026-08-27 | named registers and black-hole changes                     | `text-objects-basic` |
| 2026-08-28 | Yanky history and cycling puts                             | `speed-editing`      |
| 2026-08-29 | replacing selections without losing yanked text            | `refactor-race`      |
| 2026-08-30 | recording and replaying macros                             | `macro-recorder`     |
| 2026-08-31 | multi-file capstone with search, Harpoon, and file pickers | `vim-golf`           |

## Origin

Extracted from the dotfiles repo (`exercises/vimgolf-august-2026`, 2026-09-06):
challenges moved verbatim under `challenges/`, the runner generalized from a
month-pinned script to date-named challenges.
