// Entry program for make.fun "Sum up 23 November's world news in one image"
// (news-image-20261123).
//
// The front page was drawn beforehand with draw_news.py and ships in this
// repository as entry.png. This program copies it to the output directory
// the grader reads. No network, no randomness, no clock: every run writes
// exactly the same bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
