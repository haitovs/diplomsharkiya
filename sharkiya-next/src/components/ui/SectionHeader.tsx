interface SectionHeaderProps {
  title: string;
  subtitle?: string;
}

export function SectionHeader({ title, subtitle }: SectionHeaderProps) {
  return (
    <div className="my-6">
      <h3 className="text-xl font-semibold text-text-primary">{title}</h3>
      {subtitle && <p className="text-text-secondary mt-1">{subtitle}</p>}
    </div>
  );
}
