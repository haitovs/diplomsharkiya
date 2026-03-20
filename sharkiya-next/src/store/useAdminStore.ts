"use client";

import { create } from "zustand";

interface AdminStoreState {
  isAuthenticated: boolean;
  username: string;
  login: (username: string) => void;
  logout: () => void;
}

export const useAdminStore = create<AdminStoreState>((set) => ({
  isAuthenticated: false,
  username: "",
  login: (username) => set({ isAuthenticated: true, username }),
  logout: () => set({ isAuthenticated: false, username: "" }),
}));
