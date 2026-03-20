"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UIStoreState {
  savedEvents: string[];
  toggleSave: (eventId: string) => void;
  isSaved: (eventId: string) => boolean;
  clearSaved: () => void;
}

export const useUIStore = create<UIStoreState>()(
  persist(
    (set, get) => ({
      savedEvents: [],
      toggleSave: (eventId) =>
        set((state) => ({
          savedEvents: state.savedEvents.includes(eventId)
            ? state.savedEvents.filter((id) => id !== eventId)
            : [...state.savedEvents, eventId],
        })),
      isSaved: (eventId) => get().savedEvents.includes(eventId),
      clearSaved: () => set({ savedEvents: [] }),
    }),
    { name: "sharkiya-saved" }
  )
);
