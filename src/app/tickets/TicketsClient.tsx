"use client";

import { Hero } from "@/components/ui/Hero";
import { StatCard } from "@/components/ui/StatCard";
import { useTranslation } from "@/i18n/config";
import { usePaymentStore } from "@/store/usePaymentStore";
import { formatDate, formatTime } from "@/lib/utils";

export function TicketsClient() {
  const { t } = useTranslation();
  const { transactions, clearTransactions } = usePaymentStore();

  const reversed = [...transactions].reverse();
  const totalSpent = transactions.reduce((sum, txn) => sum + txn.amount, 0);
  const uniqueEvents = new Set(transactions.map(txn => txn.eventId)).size;

  return (
    <>
      <Hero title={t("my_tickets")} subtitle={t("tickets_subtitle")} icon="🎫" />

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
        <StatCard icon="🎫" value={transactions.length} label={t("total_tickets")} />
        <StatCard icon="🎉" value={uniqueEvents} label={t("unique_events")} />
        <StatCard icon="💰" value={`${totalSpent} TMT`} label={t("total_spent")} />
      </div>

      {reversed.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-5xl mb-4">🎫</p>
          <h3 className="text-lg font-semibold mb-2">{t("no_tickets_yet")}</h3>
          <p className="text-text-secondary text-sm">{t("visit_events_to_buy")}</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {reversed.map((txn) => (
              <div key={txn.id} className="card overflow-hidden">
                {/* Ticket header */}
                <div className="bg-gradient-to-r from-indigo-500 to-purple-500 px-4 py-3">
                  <p className="text-white font-mono text-xs opacity-80">{txn.id}</p>
                </div>

                <div className="p-4">
                  <h4 className="font-semibold text-text-primary truncate mb-2">{txn.title}</h4>

                  <div className="space-y-1.5 text-sm text-text-secondary mb-3">
                    <div className="flex items-center gap-2">
                      <span>📅</span>
                      <span>{formatDate(txn.date)} {formatTime(txn.date)}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span>👤</span>
                      <span>{txn.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span>💳</span>
                      <span>•••• {txn.cardLast4}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-3 border-t border-border-subtle">
                    <span className="text-xs text-text-muted">{t("amount")}</span>
                    <span className="text-lg font-bold text-accent-primary">{txn.amount} TMT</span>
                  </div>
                </div>

                {/* Ticket tear edge */}
                <div className="flex justify-between px-1 -mt-px">
                  {Array.from({ length: 20 }).map((_, i) => (
                    <div key={i} className="w-2 h-2 rounded-full bg-bg-primary -mb-1" />
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Clear all */}
          <div className="text-center">
            <button
              onClick={() => {
                if (confirm(t("clear_tickets_confirm"))) clearTransactions();
              }}
              className="btn-ghost text-sm text-error border-error/20 hover:bg-error/5"
            >
              🗑️ {t("clear_all_tickets")}
            </button>
          </div>
        </>
      )}
    </>
  );
}
