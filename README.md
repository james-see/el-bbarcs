# El-Bbarcs

An open-source, browser-native word board game inspired by Scrabble™ and Words With Friends™.

**No backend. No server. No tracking.** 100% runs in your browser.

## Play

Visit the GitHub Pages site: **https://james-see.github.io/el-bbarcs/**

Or clone and open `index.html` in any modern browser.

## Features

- **15×15 board** with classic bonus squares plus exclusive new ones
- **Quad Word (QW)** — 4× word score (El-Bbarcs exclusive ★)
- **Quad Letter (QL)** — 4× letter score (El-Bbarcs exclusive ★)
- **Double Word, Triple Word, Double Letter, Triple Letter** — all the classics
- **359,000+ word dictionary** loaded client-side, no API calls
- **2-player hot-seat** mode (pass-and-play on one device)
- **Blank tiles** that become any letter
- **Bingo bonus** — +50 points for using all 7 tiles in one play
- **Tile exchange** — swap tiles back to the bag
- **Shuffle rack, recall tiles, pass turn**
- **Works offline** — after first load, the dictionary is cached by the browser
- **Zero dependencies** — pure HTML/CSS/JS, no frameworks, no build step

## How to Play

1. Click a tile in your rack to select it
2. Click a cell on the board to place it
3. Build words horizontally or vertically
4. The first word must pass through the center star (★)
5. Subsequent words must connect to existing tiles
6. Click **Play Word** to submit your move
7. Blanks (★) can represent any letter — you'll be prompted to choose
8. Use all 7 tiles in one turn for a **+50 bingo bonus**

## Bonus Squares

| Symbol | Name | Effect |
|--------|------|--------|
| TW | Triple Word | 3× word score |
| **QW** | **Quad Word** ★ | **4× word score (exclusive)** |
| DW | Double Word | 2× word score |
| TL | Triple Letter | 3× letter value |
| **QL** | **Quad Letter** ★ | **4× letter value (exclusive)** |
| DL | Double Letter | 2× letter value |

★ = El-Bbarcs exclusive bonuses not found in standard word games

## Technical

- **Single file**: `index.html` — everything (HTML, CSS, JS) in one file
- **Dictionary**: `words.txt` — 359K English words (2-15 letters), loaded via `fetch()` and stored in a `Set` for O(1) lookup
- **No build step**: No npm, no bundler, no transpiler
- **GitHub Pages**: Deployed automatically via GitHub Pages from the main branch

## Word List

The dictionary is derived from the [dwyl/english-words](https://github.com/dwyl/english-words) list, filtered to 2-15 letter words. This is a general English word list, not an official tournament word list, so some tournament-valid words may be missing and some informal words may be present.

## License

MIT — do whatever you want with it.

## Disclaimer

El-Bbarcs is an independent, open-source word game. It is not affiliated with, endorsed by, or sponsored by Hasbro, Mattel, Zynga, or any other company. Scrabble is a registered trademark of Hasbro (US/Canada) and J.W. Spear & Sons/Mattel (rest of world). El-Bbarcs uses different bonus squares, different board layout positions for some bonuses, and a different name.