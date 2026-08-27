import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_PATH = ROOT / "gaming_taste_database_2026-08-12.json"
RATINGS_PATH = ROOT / "ratings.json"
WISHLIST_PATH = ROOT / "steam_wishlist.json"
CLARIFICATIONS_PATH = ROOT / "gaming_taste_migration_clarifications.json"
OUT_PATH = ROOT / "gaming_taste_live.json"


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def norm_title(value):
    value = value.lower().replace("’", "'").replace("–", "-").replace("—", "-")
    return re.sub(r"[^a-zа-яё0-9]+", "", value)


old = load(OLD_PATH)
ratings = load(RATINGS_PATH)
wishlist = load(WISHLIST_PATH)
clarifications = load(CLARIFICATIONS_PATH) if CLARIFICATIONS_PATH.exists() else {"clarifications": []}

live = copy.deepcopy(old)
live["schema_version"] = "2.0"
live["profile_type"] = "canonical_live_gaming_taste"
live["updated_at"] = "2026-08-27"
live["migrated_from"] = {
    "file": "gaming_taste_database_2026-08-12.json",
    "snapshot_date": old.get("snapshot_date"),
    "migration_rule": "The old snapshot was read once for migration. After this file exists, consumers must never read the old snapshot for recommendations, taste analysis, or sales filtering."
}
live.pop("snapshot_date", None)

live["canonical_usage"] = {
    "source_of_truth": True,
    "read_this_file_for_taste": True,
    "do_not_read_for_taste": ["gaming_taste_database_2026-08-12.json"],
    "external_factual_feeds": {
        "ratings": "ratings.json",
        "steam_wishlist": "steam_wishlist.json"
    },
    "note": "ratings.json and steam_wishlist.json remain live factual feeds. They are not substitute taste profiles. Wishlist membership means interest, not evidence that a game fits the user's taste."
}

live.setdefault("principles", {})
live["principles"].update({
    "newer_direct_user_evidence_overrides_older_inference": True,
    "wishlist_is_interest_not_fit_evidence": True,
    "stable_signals_only": "Update the taste model for durable evidence such as ratings, clear reasons, repeated patterns, lasting play constraints, and explicit corrections. Do not rewrite it for a temporary mood.",
    "single_canonical_taste_file": "All durable taste evidence and conclusions belong in gaming_taste_live.json. Do not create a second taste/evidence profile that consumers must merge at read time."
})

live["sources"] = {
    "conversation_evidence": "Direct user explanations accumulated in gaming conversations; durable newer evidence has priority over older inference.",
    "stopgame": {
        "user": ratings.get("user", "kentrap2011"),
        "count_at_last_migration": ratings.get("count"),
        "file": "ratings.json",
        "role": "live factual ratings feed"
    },
    "steam": {
        "profile": wishlist.get("profile"),
        "steamid64": wishlist.get("steamid64"),
        "wishlist_api": wishlist.get("wishlist_api"),
        "wishlist_count_at_last_migration": wishlist.get("count"),
        "file": "steam_wishlist.json",
        "role": "live interest/ownership-context feed; not proof of taste fit"
    }
}

# Keep every detailed historical game card, refresh its rating from the live ratings feed,
# and append newer rated games that were absent from the 2026-08-12 snapshot.
rating_by_norm = {norm_title(g["title"]): g for g in ratings.get("games", [])}
existing = {}
for card in live.get("stopgame_cards", []):
    key = norm_title(card.get("title", ""))
    existing[key] = card
    current = rating_by_norm.get(key)
    if current is not None:
        card["rating"] = current.get("rating")

for game in ratings.get("games", []):
    key = norm_title(game["title"])
    if key not in existing:
        live.setdefault("stopgame_cards", []).append({
            "title": game["title"],
            "rating": game.get("rating"),
            "what_liked": [],
            "what_disliked": [],
            "why_this_rating": "Причина оценки в доступном каноническом профиле пока не объяснена.",
            "separate_remarks": ["Добавлено при миграции из актуального ratings.json после снимка 2026-08-12."],
            "discussion_confidence": "низкая",
            "evidence_type": "rating_only"
        })

# Stale wishlist predictions were assistant forecasts, not user evidence. The current wishlist
# remains available separately in steam_wishlist.json and must not be duplicated here.
live.pop("steam_wishlist", None)

# Resolve stale current-play state from the old snapshot.
old_current_play = live.pop("current_play", None)
live["status_corrections_after_snapshot"] = [
    {
        "game": "Final Fantasy VII Remake",
        "old_state": old_current_play,
        "current_state": "finished/rated",
        "rating": 3.5,
        "reason": "The old snapshot still marked the game as in progress; current ratings.json contains the final 3.5/5 rating."
    }
]

# Refine older aggregate patterns rather than discarding them.
for item in live.get("taste_profile", []):
    pattern = item.get("pattern", "")
    if pattern.startswith("Сложность работает"):
        item.update({
            "pattern": "Сложность сама по себе не является минусом; особенно ценна, когда превращается в понятное освоение и мастерство.",
            "strength": "очень высокая",
            "raises": "Видимый рост навыка, паттерны, комбо, тайминги, поиск подхода, ограничения и испытания, где результат зависит от собственного мастерства.",
            "lowers": "Не высокая сложность сама по себе, а бессодержательные одинаковые попытки, непрозрачность или повторы в игре, которая уже не интересна.",
            "evidence_positive": [
                "Ultimate Mortal Kombat 3",
                "Cuphead",
                "The Legend of Dragoon",
                "Пара Па — 8-стрелочный режим и чувство редкого мастерства",
                "Sifu — сильный интерес к challenge-прохождению без старения"
            ],
            "evidence_negative": [
                "Cuphead — повторы могут утомлять при долгой серии попыток",
                "Comix Zone — сложность ограничивала удовольствие в конкретной игре",
                "Far Cry — сложность не спасает скучный основной цикл"
            ]
        })
    if pattern.startswith("Кооператив особенно ценен"):
        item.update({
            "pattern": "Совместный/социальный игровой опыт особенно ценен, когда рождает решения, роли и общие воспоминания; нативный co-op для этого не обязателен.",
            "strength": "высокая",
            "raises": "Распределение ролей, совместная тактика, помощь друг другу, обсуждение решений и сам опыт прохождения рядом с близкими/друзьями.",
            "lowers": "Сам факт наличия мультиплеера без содержательного взаимодействия не является автоматическим плюсом.",
            "evidence_positive": [
                "Battle City — совместная тактика с женой",
                "Perfect World — данжи и помощь менее опытным игрокам",
                "Cuphead — игра с дочерью",
                "Darksiders — очень нравилось совместно проходить/смотреть и обсуждать с друзьями в общежитии, несмотря на single-player",
                "Hogwarts Legacy — текущее семейное прохождение даёт дополнительный плюс, несмотря на single-player"
            ]
        })

fi = live.setdefault("factor_importance", {})
fi["сложность"] = {
    "level": "сама по себе нейтральна; мастерство — сильный плюс",
    "note": "Пользователь обычно выбирает максимальную сложность. Высокая сложность не штрафуется автоматически. Положительный сигнал — когда она раскрывает паттерны, тайминги, комбо, способы прохождения и заметный рост навыка."
}
fi["продолжительность"] = {
    "level": "не критерий качества, но важный практический риск",
    "note": "Очень длинная игра может стать любимой (RDR2), но при игре примерно раз в неделю 80+ часов растягиваются на месяцы и заметно повышают риск усталости/недопрохождения."
}
fi["мастерство_и_глубина"] = {
    "level": "очень важно",
    "note": "Сильнее, чем предполагалось в снимке 2026-08-12. Особенно ценится возможность стать заметно лучше, освоить редкий/сложный режим, персонажа, приёмы или специальный способ прохождения."
}
fi["достижения"] = {
    "level": "важный дополнительный слой мотивации, оценивать отдельно от качества базовой игры",
    "note": "Автоматические сюжетные достижения почти не ценны. Лучшие достижения заставляют менять стиль игры, осваивать механику, вводят ограничения или дают конкретный challenge."
}
fi["совместный_социальный_опыт"] = {
    "level": "сильный усилитель",
    "note": "Совместность может повысить ценность даже single-player игры, если прохождение становится общим опытом с друзьями или семьёй."
}

live["play_pattern_and_length"] = {
    "typical_frequency": "примерно один игровой день/вечер в неделю",
    "session_length": "может быть длинной, иногда до примерно 6 часов; проблема не в необходимости коротких сессий",
    "main_risk": "elapsed-time fatigue: очень длинная игра растягивается на много недель/месяцев, поэтому возвращаться и удерживать вовлечённость становится труднее",
    "length_heuristic_hours": [
        {"range": "8–20", "fit": "идеально"},
        {"range": "20–35", "fit": "очень хорошо"},
        {"range": "35–50", "fit": "умеренный риск"},
        {"range": "50–80", "fit": "осторожно"},
        {"range": "80–100+", "fit": "существенный практический минус/риск усталости"}
    ],
    "weekly_gap_resilience_raises": ["ясные главы/цели", "легко вспоминаемое управление", "не слишком много систем и политических/сюжетных сущностей одновременно"],
    "dlc_rule": "Очень крупное DLC разумно оценивать как отдельную игру и при необходимости делать паузу между базой и дополнением."
}

live["mastery_profile"] = {
    "strength": "очень высокая",
    "summary": "Механическое мастерство — один из сильнейших положительных сигналов. Пользователю нравится не просто сложность, а ощущение, что он научился делать что-то хорошо или лучше большинства/собственного прошлого результата.",
    "evidence": [
        "Ultimate Mortal Kombat 3 — нравилось глубоко изучать одного бойца, приёмы и длинные комбинации.",
        "Пара Па — особенно нравился 8-стрелочный режим с диагоналями; мало кто хорошо умел, пользователь умел, и именно это чувство мастерства было важно.",
        "Perfect World — нравилось быть опытным игроком и помогать менее опытным.",
        "Cuphead — нравилось искать правильный подход к боссу.",
        "Sifu — очень зацепила идея сложного achievement/challenge закончить игру без старения."
    ],
    "guardrail": "Не сводить все рекомендации к сложным action-играм: это сильный фактор, но рекомендации должны учитывать сюжет, атмосферу, разнообразие и другие подтверждённые сигналы."
}

live["achievement_profile"] = {
    "role": "separate_from_base_game_fit",
    "general": "Достижения интересуют как дополнительная мотивация и видимый профиль прогресса. Они ценны, когда меняют поведение игрока, а не просто фиксируют неизбежное прохождение сюжета.",
    "strong_positive": [
        "mastery/challenge achievements",
        "ограничения и необычные стили прохождения",
        "no-hit/no-death или специальные методы боя, когда challenge осмысленный",
        "достижения на глубокое использование механик",
        "NG+ achievement способен дать причину для повторного прохождения",
        "конечные коллекционные цели могут превратить расплывчатый сбор в понятную задачу"
    ],
    "weak_or_negative": [
        "автоматические сюжетные достижения",
        "бессодержательный grind",
        "огромные чек-листы ради зачистки карты"
    ],
    "scale": {
        "5/5": "действительно создают новые стили прохождения/испытания",
        "4/5": "заметно углубляют использование механик",
        "3/5": "дают осмысленные дополнительные цели/секреты",
        "2/5": "в основном коллекционки или grind",
        "1/5": "почти полностью автоматические сюжетные"
    }
}

live["multiplayer_and_gacha"] = {
    "multiplayer": "нейтрально по умолчанию: наличие multiplayer само по себе не плюс и не минус; плюс появляется через интересную механику, мастерство или содержательное взаимодействие",
    "gacha": "нейтрально по умолчанию: наличие гачи не считать самостоятельным минусом; важнее качество геймплея, прогрессии, монетизации и комфорт без обязательного доната"
}

live["shared_play_clarifications"] = clarifications.get("clarifications", [])

live["recommendation_rules"] = {
    "base_game_and_achievements": "Всегда оценивать соответствие самой игры и качество/полезность достижений отдельно.",
    "wishlist": "Wishlist означает интерес, а не backlog и не доказательство попадания во вкус.",
    "avoid_overfitting": "Не превращать один сильный сигнал (например, паркур, мастерство или сюжет) в обязательное условие всех рекомендаций; использовать совокупность факторов и сохранять разнообразие кандидатов.",
    "long_games": "Не отбрасывать длинные игры автоматически, но явно учитывать практический риск растяжения на месяцы.",
    "difficulty": "Не штрафовать игру только за высокую сложность; отдельно оценивать ясность обучения, качество повторных попыток и награду за освоение.",
    "social_single_player": "Single-player игра может получить дополнительный плюс, если хорошо работает как общий семейный/дружеский опыт рядом с экраном."
}

live["evidence_log"] = [
    {
        "date": "2026-08-27",
        "type": "migration_resolution",
        "topic": "length",
        "evidence": "Продолжительность не является самостоятельным признаком качества, но при текущем режиме игры становится практическим фактором риска; 80+ часов могут растянуться на месяцы."
    },
    {
        "date": "2026-08-27",
        "type": "migration_resolution",
        "topic": "shared play",
        "evidence": "Darksiders и Hogwarts Legacy не являются co-op играми; они находятся среди положительных социальных примеров потому, что Darksiders очень нравилось совместно переживать с друзьями в общежитии, а Hogwarts Legacy сейчас является семейным прохождением и это дополнительный плюс."
    },
    {
        "date": "2026-08-27",
        "type": "newer_durable_signal",
        "topic": "mastery",
        "evidence": "Позднейшие обсуждения Пара Па, Perfect World, файтингов и challenge-достижений усилили вывод: механическое мастерство — один из сильнейших положительных сигналов."
    },
    {
        "date": "2026-08-27",
        "type": "newer_durable_signal",
        "topic": "achievements",
        "evidence": "Ценятся достижения, которые дают новые challenge/ограничения/стили; сюжетные авто-достижения почти не добавляют мотивации."
    },
    {
        "date": "2026-08-27",
        "type": "status_correction",
        "topic": "Final Fantasy VII Remake",
        "evidence": "Старый snapshot отмечал игру как незавершённую; актуальная финальная оценка — 3.5/5."
    }
]

live["migration_audit"] = {
    "resolved_conflicts": [
        "Продолжительность: старая формулировка 'условно нейтральна' уточнена как практический риск при редком недельном режиме игры, без утверждения что длинные игры сами по себе хуже.",
        "Darksiders/Hogwarts Legacy: уточнено, почему single-player игры являются положительными примерами совместного опыта.",
        "Final Fantasy VII Remake: stale in-progress state replaced by final 3.5/5 rating."
    ],
    "not_conflicts_but_refinements": [
        "Высокая сложность не отрицательный сигнал; сильнее выделено мастерство.",
        "Добавлен отдельный профиль достижений.",
        "Добавлена нейтральная базовая позиция к multiplayer и gacha.",
        "Добавлен недельный режим игры и шкала риска по длительности."
    ],
    "intentionally_not_migrated": [
        "Old steam_wishlist prediction cards. They were assistant forecasts, can become stale, and the old profile itself states that assistant predictions are not user evidence. Current wishlist remains in steam_wishlist.json."
    ]
}

with OUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(live, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Wrote {OUT_PATH.name}: {len(live.get('stopgame_cards', []))} game evidence cards; ratings feed count={ratings.get('count')}; wishlist feed count={wishlist.get('count')}")
