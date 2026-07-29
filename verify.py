#!/usr/bin/env python3
"""Ad-hoc verification of El-Bbarcs game logic by running JS in Node."""
import subprocess, sys, os, tempfile

html_path = "/Users/jc/p/el-bbarcs/index.html"
with open(html_path) as f:
    html = f.read()
start = html.rindex("<script>") + len("<script>")
end = html.rindex("</script>")
js_code = html[start:end]

test_js = """
const elements = {};
const document = {
  getElementById: (id) => elements[id] || {classList:{add(){},remove(){}},style:{},textContent:'',innerHTML:'',appendChild(){},addEventListener(){},onclick:null,dataset:{}},
  querySelectorAll: () => [],
  createElement: () => ({className:'',dataset:{},innerHTML:'',textContent:'',addEventListener(){},appendChild(){},style:{},classList:{add(){},remove(){}}}),
  querySelector: () => null,
};
const window = {};
const console2 = console;
const confirm = () => true;
const setTimeout = (fn) => {};
const clearTimeout = () => {};
""" + js_code + """

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console2.log('  PASS: ' + name); }
  catch(e) { failed++; console2.log('  FAIL: ' + name + ' - ' + e.message); }
}
function assert(cond, msg) { if(!cond) throw new Error(msg); }

test('Bag has 100 tiles', () => {
  const bag = createBag();
  assert(bag.length === 100, 'Expected 100, got ' + bag.length);
});
test('Tile distribution correct', () => {
  const bag = createBag();
  const counts = {};
  for (const t of bag) { const key = t.isBlank ? 'BLANK' : t.letter; counts[key] = (counts[key] || 0) + 1; }
  assert(counts['E'] === 12, 'E should be 12');
  assert(counts['A'] === 9, 'A should be 9');
  assert(counts['Q'] === 1, 'Q should be 1');
  assert(counts['BLANK'] === 2, 'BLANK should be 2');
  assert(counts['Z'] === 1, 'Z should be 1');
});
test('Tile values correct', () => {
  assert(TILE_VALUES['A'] === 1, 'A=1');
  assert(TILE_VALUES['Q'] === 10, 'Q=10');
  assert(TILE_VALUES['Z'] === 10, 'Z=10');
  assert(TILE_VALUES['BLANK'] === 0, 'BLANK=0');
});
test('Bonus squares: 8 TW, 16 DW, 12 TL, 22 DL, 4 QW, 8 QL', () => {
  const types = {tw:0, dw:0, tl:0, dl:0, qw:0, ql:0};
  for (const [k,v] of Object.entries(BONUSES)) types[v]++;
  assert(types.tw === 8, 'TW=8 got ' + types.tw);
  assert(types.dw === 16, 'DW=16 got ' + types.dw);
  assert(types.tl === 12, 'TL=12 got ' + types.tl);
  assert(types.dl === 22, 'DL=22 got ' + types.dl);
  assert(types.qw === 4, 'QW=4 got ' + types.qw);
  assert(types.ql === 8, 'QL=8 got ' + types.ql);
});
test('QW at correct positions', () => {
  assert(BONUSES['5,2'] === 'qw', '5,2');
  assert(BONUSES['5,12'] === 'qw', '5,12');
  assert(BONUSES['9,2'] === 'qw', '9,2');
  assert(BONUSES['9,12'] === 'qw', '9,12');
});
test('QL at correct positions', () => {
  const qls = Object.entries(BONUSES).filter(([,v])=>v==='ql').map(([k])=>k).sort();
  const expected = ['10,12','10,2','12,10','12,4','2,10','2,4','4,12','4,2'].sort();
  assert(JSON.stringify(qls) === JSON.stringify(expected), 'QL positions: ' + JSON.stringify(qls));
});
test('Board is 15x15 and empty', () => {
  initBoard();
  assert(G.board.length === 15, '15 rows');
  assert(G.board[0].length === 15, '15 cols');
  assert(G.board[7][7] === null, 'center empty');
});
test('isValidWord works', () => {
  G.dictionaryReady = false;
  assert(isValidWord('anything') === true, 'should be true when not ready');
  G.dictionaryReady = true;
  G.dictionary = new Set(['cat','dog','rain']);
  assert(isValidWord('cat') === true, 'cat valid');
  assert(isValidWord('xyzqq') === false, 'xyzqq invalid');
  assert(isValidWord('RAIN') === true, 'RAIN valid (case-insensitive)');
});
test('QW scoring: CAT on QW = 20', () => {
  initBoard();
  G.placedTiles = [
    {row:5, col:2, letter:'C', value:3, isBlank:false, rackIdx:0},
    {row:5, col:3, letter:'A', value:1, isBlank:false, rackIdx:1},
    {row:5, col:4, letter:'T', value:1, isBlank:false, rackIdx:2}
  ];
  const words = findWordsFormed();
  const score = calculateScore(words);
  assert(score === 20, 'Expected 20, got ' + score);
});
test('QL scoring: C on QL, T on DL = 15', () => {
  initBoard();
  G.placedTiles = [
    {row:2, col:4, letter:'C', value:3, isBlank:false, rackIdx:0},
    {row:2, col:5, letter:'A', value:1, isBlank:false, rackIdx:1},
    {row:2, col:6, letter:'T', value:1, isBlank:false, rackIdx:2}
  ];
  const words = findWordsFormed();
  const score = calculateScore(words);
  assert(score === 15, 'Expected 15, got ' + score);
});
test('TW scoring: CAT on TW = 15', () => {
  initBoard();
  G.placedTiles = [
    {row:0, col:0, letter:'C', value:3, isBlank:false, rackIdx:0},
    {row:0, col:1, letter:'A', value:1, isBlank:false, rackIdx:1},
    {row:0, col:2, letter:'T', value:1, isBlank:false, rackIdx:2}
  ];
  const words = findWordsFormed();
  const score = calculateScore(words);
  assert(score === 15, 'Expected 15, got ' + score);
});
test('Bingo: 7 tiles = +50 bonus', () => {
  initBoard();
  G.placedTiles = [
    {row:7, col:1, letter:'T', value:1, isBlank:false, rackIdx:0},
    {row:7, col:2, letter:'R', value:1, isBlank:false, rackIdx:1},
    {row:7, col:3, letter:'A', value:1, isBlank:false, rackIdx:2},
    {row:7, col:4, letter:'I', value:1, isBlank:false, rackIdx:3},
    {row:7, col:5, letter:'N', value:1, isBlank:false, rackIdx:4},
    {row:7, col:6, letter:'E', value:1, isBlank:false, rackIdx:5},
    {row:7, col:7, letter:'D', value:2, isBlank:false, rackIdx:6}
  ];
  const words = findWordsFormed();
  const score = calculateScore(words);
  assert(score === 58, 'Expected 58 (8+50), got ' + score);
});
test('First move must include center', () => {
  initBoard();
  G.placedTiles = [
    {row:0, col:0, letter:'C', value:3, isBlank:false, rackIdx:0},
    {row:0, col:1, letter:'A', value:1, isBlank:false, rackIdx:1},
    {row:0, col:2, letter:'T', value:1, isBlank:false, rackIdx:2}
  ];
  const result = validateMove();
  assert(!result.valid, 'Should be invalid');
  assert(result.error.includes('center'), 'Error should mention center');
});
test('Tiles must be in single line', () => {
  initBoard();
  G.board[7][7] = {letter:'X', value:8, isBlank:false, playerId:0};
  G.placedTiles = [
    {row:6, col:6, letter:'C', value:3, isBlank:false, rackIdx:0},
    {row:8, col:8, letter:'A', value:1, isBlank:false, rackIdx:1}
  ];
  const result = validateMove();
  assert(!result.valid, 'Should be invalid (diagonal)');
});
test('New game resets state', () => {
  newGame();
  assert(G.players.length === 2, '2 players');
  assert(G.players[0].score === 0, 'P1 score 0');
  assert(G.players[1].score === 0, 'P2 score 0');
  assert(G.players[0].rack.length === 7, 'P1 has 7 tiles');
  assert(G.players[1].rack.length === 7, 'P2 has 7 tiles');
  assert(G.bag.length === 86, 'Bag has 86, got ' + G.bag.length);
  assert(G.gameOver === false, 'Game not over');
  assert(G.currentPlayer === 0, 'P1 starts');
});

console2.log('\\n' + passed + ' passed, ' + failed + ' failed');
process.exit(failed > 0 ? 1 : 0);
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.js', prefix='hermes-verify-', dir='/tmp', delete=False) as f:
    f.write(test_js)
    tmp_path = f.name

result = subprocess.run(['node', tmp_path], capture_output=True, text=True, timeout=30)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Exit code:", result.returncode)
os.unlink(tmp_path)
sys.exit(result.returncode)