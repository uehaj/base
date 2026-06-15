import { test } from 'node:test';
import assert from 'node:assert/strict';
import { greet } from '../src/hello.js';

test('greet はデフォルトで world に挨拶する', () => {
  // 引数なしの既定挨拶を確認する。
  assert.equal(greet(), 'Hello, world!');
});

test('greet は渡した名前に挨拶する', () => {
  // 名前を渡したときの出力を確認する。
  assert.equal(greet('base'), 'Hello, base!');
});
