import { z } from "zod";

export const askRequestSchema = z.object({
  question: z.string().min(3).max(1000),
  topK: z.number().int().min(1).max(10).default(3),
  showSources: z.boolean().default(true)
});
