import { v4 as uuidv4 } from 'uuid';
import { Message } from "../types";

export const createMessage = (
  content: string,
  role: "user" | "assistant",
  sources?: any[]
): Message => ({
  id: (Date.now() + Math.floor(Math.random() * 1000)).toString(),
  role,
  content,
  sources,
});

export function formatUploadDate(timestamp: string | number | Date) {
  return new Date(timestamp).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

const GUEST_ID_KEY = 'guest_id';

export const getOrCreateGuestId = (): string => {
  if (typeof window === 'undefined') return '';
  
  let guestId = localStorage.getItem(GUEST_ID_KEY);
  
  if (!guestId) {
    guestId = uuidv4();
    localStorage.setItem(GUEST_ID_KEY, guestId);
  }
  
  return guestId;
};

export const getGuestId = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(GUEST_ID_KEY);
};