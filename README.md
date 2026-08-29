# stopgame-ratings-data

## Gaming taste profile

- `gaming_taste_live.json` — the single canonical live gaming-taste profile. Use this file for recommendations, taste analysis, and sale filtering.
- `gaming_taste_database_2026-08-12.json` — historical archive only. Do **not** read or merge it into current taste logic.
- `ratings.json` — live factual StopGame ratings feed.
- `steam_wishlist.json` — live Steam interest/context feed. Wishlist membership is not evidence that a game fits the user's taste.
- `.github/taste_update_request.json` — compact delta input for the existing taste-profile update workflow.

Durable new taste evidence and explicit corrections should be merged into `gaming_taste_live.json`. Temporary moods and assistant-only predictions should not be treated as user taste evidence.

## Chat usage

GitHub is the source of truth for live state. Copies in ChatGPT/File Library are reference or archive material and must not override newer GitHub state.

For a normal taste update, do not load or rewrite the full `gaming_taste_live.json` unless it is genuinely necessary. Read only the relevant section, write the smallest safe delta to `.github/taste_update_request.json`, and use the existing update workflow.

Do not read `gaming_taste_database_2026-08-12.json` during current recommendation or newsletter work.
