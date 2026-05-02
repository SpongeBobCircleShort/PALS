export type SourceMatch = {
  rank: number;
  score: number;
  sourceFile: string;
  pageNum: number;
  chunkIndex: number;
  text: string;
};

export type AskRequest = {
  question: string;
  topK?: number;
  showSources?: boolean;
};

export type AskResponse = {
  question: string;
  socraticQuestions: string[];
  hint: { supportSentences: string[] };
  takeaway: string;
  sources: SourceMatch[];
};
