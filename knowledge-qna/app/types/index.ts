export interface Document {
  document_id: string;
  document_name: string;
  upload_timestamp: string;
}

export interface Source {
  document_name: string;
  excerpt: string;
}

export interface AnswerResponse {
  answer: string;
  sources: Source[];
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}