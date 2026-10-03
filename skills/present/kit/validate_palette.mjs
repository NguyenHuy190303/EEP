import { pathToFileURL } from "node:url";

function parseHex(value) {
  const normalized = value.trim().replace(/^#/, "");
  const expanded = normalized.length === 3
    ? normalized.split("").map((part) => part + part).join("")
    : normalized;
  if (!/^[0-9a-f]{6}$/i.test(expanded)) throw new Error(`Invalid hex color: ${value}`);
  return [0, 2, 4].map((index) => Number.parseInt(expanded.slice(index, index + 2), 16));
}

function linear(channel) {
  const value = channel / 255;
  return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
}

export function contrastRatio(a, b) {
  const luminance = (color) => {
    const [r, g, blue] = parseHex(color).map(linear);
    return 0.2126 * r + 0.7152 * g + 0.0722 * blue;
  };
  const [lighter, darker] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (lighter + 0.05) / (darker + 0.05);
}

function lab(color) {
  const [r, g, b] = parseHex(color).map(linear);
  const xyz = [
    (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047,
    0.2126 * r + 0.7152 * g + 0.0722 * b,
    (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883,
  ].map((value) => value > 0.008856 ? Math.cbrt(value) : 7.787 * value + 16 / 116);
  return [116 * xyz[1] - 16, 500 * (xyz[0] - xyz[1]), 200 * (xyz[1] - xyz[2])];
}

export function deltaE(a, b) {
  const left = lab(a);
  const right = lab(b);
  return Math.hypot(...left.map((value, index) => value - right[index]));
}

export function analyzePalette(colors, surface) {
  return {
    surface: colors.map((color) => ({ color, contrast: contrastRatio(color, surface) })),
    pairs: colors.flatMap((left, index) => colors.slice(index + 1).map((right) => ({
      left,
      right,
      deltaE: deltaE(left, right),
    }))),
  };
}

function option(args, name) {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : undefined;
}

function main(args) {
  const palette = args[0];
  const surface = option(args, "--surface");
  const mode = option(args, "--mode") ?? "unspecified";
  if (!palette || !surface) throw new Error("Usage: node validate_palette.mjs '#hex,#hex' --surface '#hex' [--mode light|dark] [--pairs all]");

  const colors = palette.split(",").map((color) => `#${color.trim().replace(/^#/, "")}`);
  const normalizedSurface = `#${surface.trim().replace(/^#/, "")}`;
  const result = analyzePalette(colors, normalizedSurface);

  console.log(`mode=${mode} surface=${normalizedSurface}`);
  for (const item of result.surface) {
    const note = item.contrast < 3 ? "pair with text/shape; not color-only" : "ok for non-text contrast";
    console.log(`${item.color} contrast=${item.contrast.toFixed(2)} ${note}`);
  }
  if (option(args, "--pairs") === "all") {
    for (const pair of result.pairs) {
      const note = pair.deltaE < 10 ? "pair with text/shape; colors are close" : "distinct";
      console.log(`${pair.left}/${pair.right} deltaE76=${pair.deltaE.toFixed(2)} ${note}`);
    }
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
