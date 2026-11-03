# Sifu — результат отдельной тестовой примерки Steam (01)

**Дата:** 2026-11-03  
**Репозиторий:** `kentrap2011-hub/stopgame-ratings-data`  
**Ветка публикации:** `gh-pages`  
**Ветка отчёта:** `main`  
**Статус:** файлы и страница записаны в `gh-pages`; публичный HTTP-ответ GitHub Pages не удалось проверить из данной среды.

## Тестовая страница

https://kentrap2011-hub.github.io/stopgame-ratings-data/steam-showcase-sifu-preview-01/

**Финальный коммит публикации `gh-pages`:** [`4ba10fa42e3ba2653a4fb56e4542f7001954873b`](https://github.com/kentrap2011-hub/stopgame-ratings-data/commit/4ba10fa42e3ba2653a4fb56e4542f7001954873b).  
**Коммит добавления исходных PNG и страницы:** [`5b4ea4bf2f07f92ad429b60bd58f740a78d24b3a`](https://github.com/kentrap2011-hub/stopgame-ratings-data/commit/5b4ea4bf2f07f92ad429b60bd58f740a78d24b3a).

## Оригинальные PNG

Все три файла переданы в GitHub из точных исходных байтов ChatGPT Library, без генерации, изменений, пережатия или изменения размеров. Полученные в GitHub Git blob SHA равны Git blob SHA, локально рассчитанным по исходным файлам.

| Вариант | Путь в `gh-pages` | Размер и разрешение | SHA-256 оригинала | Git blob SHA |
|---|---|---|---|---|
| A — Коридор свернулся | `steam-showcase-sifu-preview-01/images/corridor-fold.png` | 1 943 652 B; 1914×822 | `73049e1470f77ef4acaabc2a53b3c8665430606c10619dbc044cae8d480b131b` | `c1773b03c42da0e460cfa3a9225b6ed4f72588f2` |
| B — Тень не умеет воскресать | `steam-showcase-sifu-preview-01/images/aging-shadow.png` | 2 046 530 B; 2172×724 | `5633081c4f6655f85aed78c0a5a796e9bc8983c7bf4855728980a2c4c5dc2bc6` | `8791303de12d51a07a609c68f25b8ebce8ee5e1b` |
| C — Ниже линии удара | `steam-showcase-sifu-preview-01/images/below-strike.png` | 1 784 491 B; 2172×724 | `5cae0370bfd7d177daccbf037462346ec9cb3e87cdd88e30d75fcd41579b93e4` | `ffa3576bc007dbf4ceaed6c4aae552acadf678f5` |

Прямые URL для открытия в браузере:

- A: https://kentrap2011-hub.github.io/stopgame-ratings-data/steam-showcase-sifu-preview-01/images/corridor-fold.png
- B: https://kentrap2011-hub.github.io/stopgame-ratings-data/steam-showcase-sifu-preview-01/images/aging-shadow.png
- C: https://kentrap2011-hub.github.io/stopgame-ratings-data/steam-showcase-sifu-preview-01/images/below-strike.png

## Реализовано

- Отдельная папка `steam-showcase-sifu-preview-01/` с `index.html`, `styles.css`, `script.js` и тремя локальными PNG.
- Мобильная тёмная примерка профиля KentRAP с шапкой, областью Steam Artwork Showcase и дополнительной колонкой на широком экране.
- Фон SS_Landscape и аватар KentRAP взяты по тем же общедоступным внешним адресам Steam CDN, которые применялись в старых тестовых страницах.
- Переключение вкладок A/B/C без скачивания, отображение одного оригинального PNG прямо внутри макета.
- Отдельная действующая ссылка «Открыть оригинал» на каждый PNG (новая вкладка).
- Сохранение естественных пропорций изображений без обрезки и имитации финальных слотов Steam.
- Явная маркировка страницы как **тестовой**, а не production-экспорта для Steam.

## Не реализовано и ограничения

- **Не** создавались вертикальные финальные изображения и их нарезка для загрузки в Steam; никаких новых художественных генераций.
- **Не** менялись `gh-pages/index.html`, `gh-pages/steam-profile-preview/`, старые страницы и проекты; оба коммита затрагивают только новый каталог.
- **HTTP-проверка публичного сайта не подтверждена:** средство внешней веб-проверки не открыло ни новую страницу, ни ранее существующую страницу `steam-profile-preview/`; оно сообщает, что URL недоступен через этот инструмент. Это не доказательство HTTP 404. Проведена проверка GitHub-ветки и объектов; независимая проверка браузером GitHub Pages остаётся ограничением.
- Загрузка **фона SS_Landscape и аватара** зависит от внешних адресов Steam CDN; их доступность из мобильной сети не измерялась.
- Headless Chromium в доступном контейнере блокирует навигацию (включая localhost) административным ограничением, поэтому визуальный mobile screenshot не подтверждён.

## Проведённые проверки

1. GitHub API: `gh-pages` содержит три PNG по указанным путям; `fetch_file` возвращает точные ожидаемые Git SHA для каждого.
2. GitHub: коммит добавления содержит ровно шесть новых файлов в отдельном каталоге, дополнительный коммит меняет только его `index.html` и `styles.css`.
3. Локально: PNG signature, IHDR-размеры и SHA-256 проверены; все совпадают с исходниками.
4. Локально: `node --check` — PASS; эмулированные DOM-переключения A/B/C меняют пути к изображению, подписи, ширину/высоту и URL оригинала — PASS для всех трёх.
5. Публичный HTTP-статус GitHub Pages и загрузка изображений в реальном Android-браузере — **NOT VERIFIED** из-за ограничения инструмента, не заявлены как PASS.
