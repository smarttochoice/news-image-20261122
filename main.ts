// news-image-20261122 entry (Node 22, standard library only).
// The image is built ahead of time by draw.py (see README) and ships in
// this repository as entry.png; this program places a byte-identical copy
// at /output/entry.png. It writes the same bytes on every run.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const png = readFileSync(join(here, "entry.png"));

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), png);
