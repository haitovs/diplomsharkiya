"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { v4 as uuidv4 } from "uuid";
import type { Transaction } from "@/types/event";

interface PaymentStoreState {
  transactions: Transaction[];
  addTransaction: (params: {
    eventId: string;
    title: string;
    amount: number;
    name: string;
    cardLast4: string;
  }) => string;
  getEventPurchaseCount: (eventId: string) => number;
  clearTransactions: () => void;
}

export const usePaymentStore = create<PaymentStoreState>()(
  persist(
    (set, get) => ({
      transactions: [],
      addTransaction: ({ eventId, title, amount, name, cardLast4 }) => {
        const txnId = `TXN-${uuidv4().replace(/-/g, "").slice(0, 8).toUpperCase()}`;
        const transaction: Transaction = {
          id: txnId,
          eventId,
          title,
          amount,
          name,
          cardLast4,
          date: new Date().toISOString(),
        };
        set((state) => ({
          transactions: [...state.transactions, transaction],
        }));
        return txnId;
      },
      getEventPurchaseCount: (eventId) =>
        get().transactions.filter((t) => t.eventId === eventId).length,
      clearTransactions: () => set({ transactions: [] }),
    }),
    { name: "sharkiya-payments" }
  )
);
