"use client";

import { useState, useRef } from "react";
import { useTranslation } from "@/i18n/config";
import { usePaymentStore } from "@/store/usePaymentStore";
import type { Event } from "@/types/event";

interface PaymentDialogProps {
  event: Event;
  onClose: () => void;
}

export function PaymentDialog({ event, onClose }: PaymentDialogProps) {
  const { t } = useTranslation();
  const { addTransaction } = usePaymentStore();
  const [cardNumber, setCardNumber] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");
  const [cardholder, setCardholder] = useState("");
  const [errors, setErrors] = useState<string[]>([]);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [success, setSuccess] = useState<{ txnId: string; cardLast4: string } | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  function validate(): string[] {
    const errs: string[] = [];
    const cleanCard = cardNumber.replace(/\s/g, "");
    if (!/^\d{16}$/.test(cleanCard)) errs.push(t("invalid_card"));
    if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(expiry.trim())) errs.push(t("invalid_expiry"));
    if (!/^\d{3}$/.test(cvv.trim())) errs.push(t("invalid_cvv"));
    if (!cardholder.trim()) errs.push(t("fill_required"));
    return errs;
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errs = validate();
    if (errs.length > 0) {
      setErrors(errs);
      return;
    }
    setErrors([]);
    setProcessing(true);
    setProgress(0);

    let pct = 0;
    timerRef.current = setInterval(() => {
      pct += 5;
      setProgress(pct);
      if (pct >= 100) {
        if (timerRef.current) clearInterval(timerRef.current);
        const cleanCard = cardNumber.replace(/\s/g, "");
        const txnId = addTransaction({
          eventId: event.id,
          title: event.title,
          amount: event.price,
          name: cardholder.trim(),
          cardLast4: cleanCard.slice(-4),
        });
        setSuccess({ txnId, cardLast4: cleanCard.slice(-4) });
        setProcessing(false);
      }
    }, 60);
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {success ? (
          <div className="text-center">
            <p className="text-5xl mb-4">🎉</p>
            <h3 className="text-xl font-bold text-accent-secondary mb-4">{t("payment_successful")}</h3>
            <div className="bg-bg-secondary rounded-lg p-4 text-left text-sm space-y-2 mb-6">
              <div className="flex justify-between">
                <span className="text-text-secondary">{t("transaction_id")}</span>
                <span className="font-mono font-semibold">{success.txnId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">{t("event_title")}</span>
                <span className="font-semibold">{event.title}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">{t("amount")}</span>
                <span className="font-semibold">{Math.round(event.price)} TMT</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">{t("card_number")}</span>
                <span className="font-mono">•••• {success.cardLast4}</span>
              </div>
            </div>
            <button onClick={onClose} className="btn-primary w-full">
              ✅ {t("done")}
            </button>
          </div>
        ) : (
          <>
            <h3 className="text-xl font-bold mb-1">🎫 {t("payment_form_title")}</h3>
            <p className="text-text-secondary text-sm mb-1">{event.title}</p>
            <p className="text-accent-primary font-bold mb-4">{t("amount")}: {Math.round(event.price)} TMT</p>

            {errors.length > 0 && (
              <div className="bg-error/10 border border-error/30 rounded-lg p-3 mb-4">
                {errors.map((err, i) => (
                  <p key={i} className="text-error text-sm">{err}</p>
                ))}
              </div>
            )}

            {processing ? (
              <div className="py-8">
                <p className="text-center text-text-secondary mb-4">{t("processing_payment")}</p>
                <div className="w-full bg-bg-secondary rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-100"
                    style={{
                      width: `${progress}%`,
                      background: "linear-gradient(90deg, #6366F1, #10B981)",
                    }}
                  />
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1">{t("card_number")}</label>
                  <input
                    type="text"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    maxLength={16}
                    placeholder="1234567812345678"
                    className="input"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1">{t("expiry_date")}</label>
                    <input
                      type="text"
                      value={expiry}
                      onChange={(e) => setExpiry(e.target.value)}
                      maxLength={5}
                      placeholder="MM/YY"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1">{t("cvv")}</label>
                    <input
                      type="password"
                      value={cvv}
                      onChange={(e) => setCvv(e.target.value)}
                      maxLength={3}
                      placeholder="123"
                      className="input"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1">{t("cardholder_name")}</label>
                  <input
                    type="text"
                    value={cardholder}
                    onChange={(e) => setCardholder(e.target.value)}
                    placeholder="JOHN DOE"
                    className="input"
                  />
                </div>
                <button type="submit" className="btn-success w-full text-base py-2.5">
                  💳 {t("pay_now")} — {Math.round(event.price)} TMT
                </button>
                <button type="button" onClick={onClose} className="btn-ghost w-full text-sm">
                  {t("cancel")}
                </button>
              </form>
            )}
          </>
        )}
      </div>
    </div>
  );
}
