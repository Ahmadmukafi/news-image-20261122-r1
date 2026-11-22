import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const outPath = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), outPath);
if (statSync(outPath).size === 0) throw new Error("entry.png is empty");
