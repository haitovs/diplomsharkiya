"use client";

interface HeroProps {
  title: string;
  subtitle: string;
  icon?: string;
  badge?: string;
}

export function Hero({ title, subtitle, icon = "🎟️", badge = "Event Discovery Platform" }: HeroProps) {
  return (
    <div className="hero-banner">
      <p className="inline-block px-4 py-1.5 bg-white/15 border border-white/25 rounded-full text-sm font-medium mb-3">
        {icon} {badge}
      </p>
      <h1 className="text-3xl sm:text-4xl font-bold text-white tracking-tight mb-2">
        {title}
      </h1>
      <p className="text-white/85 text-lg max-w-lg mx-auto">
        {subtitle}
      </p>
    </div>
  );
}
