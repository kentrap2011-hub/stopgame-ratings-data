# stopgame-ratings-data

## Gaming taste profile

- `gaming_taste_live.json` — the single canonical live gaming-taste profile. Use this file for recommendations, taste analysis, and sale filtering.
- `gaming_taste_database_2026-08-12.json` — historical archive only. Do **not** read or merge it into current taste logic.
- `ratings.json` — live factual StopGame ratings feed.
- `steam_wishlist.json` — live Steam interest/context feed. Wishlist membership is not evidence that a game fits the user's taste.

Durable new taste evidence and explicit corrections should be merged directly into `gaming_taste_live.json`. Temporary moods and assistant-only predictions should not be treated as user taste evidence.
