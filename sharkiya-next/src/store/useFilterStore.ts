"use client";

import { create } from "zustand";
import type { FilterState } from "@/types/event";

interface FilterStoreState extends FilterState {
  setCity: (city: string) => void;
  setCategories: (categories: string[]) => void;
  toggleCategory: (category: string) => void;
  setDatePreset: (preset: string) => void;
  setMaxPrice: (price: number) => void;
  setSearchQuery: (query: string) => void;
  setSortBy: (sortBy: string) => void;
  resetFilters: () => void;
}

const initialState: FilterState = {
  city: "All Cities",
  categories: [],
  datePreset: "All",
  maxPrice: 200,
  searchQuery: "",
  sortBy: "Date (Soonest)",
};

export const useFilterStore = create<FilterStoreState>((set) => ({
  ...initialState,
  setCity: (city) => set({ city }),
  setCategories: (categories) => set({ categories }),
  toggleCategory: (category) =>
    set((state) => ({
      categories: state.categories.includes(category)
        ? state.categories.filter((c) => c !== category)
        : [...state.categories, category],
    })),
  setDatePreset: (datePreset) => set({ datePreset }),
  setMaxPrice: (maxPrice) => set({ maxPrice }),
  setSearchQuery: (searchQuery) => set({ searchQuery }),
  setSortBy: (sortBy) => set({ sortBy }),
  resetFilters: () => set(initialState),
}));
