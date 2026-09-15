import test from "node:test";
import assert from "node:assert/strict";
import { analyzePalette, contrastRatio, deltaE } from "./validate_palette.mjs";

test("black and white have the maximum WCAG contrast", () => {
  assert.equal(contrastRatio("#000000", "#ffffff"), 21);
});

test("identical colors have zero Delta E", () => {
  assert.equal(deltaE("#268bd2", "#268bd2"), 0);
});

test("analysis covers each surface comparison and unique pair", () => {
  const result = analyzePalette(["#268bd2", "#859900", "#b58900"], "#fdf6e3");
  assert.equal(result.surface.length, 3);
  assert.equal(result.pairs.length, 3);
});
