import { api } from "./apiInterceptor";
import { Document, AnswerResponse } from "@/app/types";

export async function uploadDocuments(files: File[], guestId: string) {
  const formData = new FormData();
  files.forEach(file => formData.append("files", file));

  const { data } = await api.post(`/documents/upload?guest_id=${guestId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function getDocuments(guestId: string): Promise<Document[]> {
  const { data } = await api.get(`/documents?guest_id=${guestId}`);
  return data;
}

export async function askQuestion(question: string, guestId: string): Promise<AnswerResponse> {
  const { data } = await api.post(`/qa/ask?guest_id=${guestId}`, { question });
  return data;
}