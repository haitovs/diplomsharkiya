"use client";

import { useTranslation } from "@/i18n/config";

export function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="border-t border-border-subtle py-6 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 text-center text-text-muted text-sm">
        <p>🎟️ {t("event_discovery_platform")} — Turkmenistan</p>
        <p className="mt-1">Version 1.0 — Built with Next.js</p>
      </div>
    </footer>
  );
}
