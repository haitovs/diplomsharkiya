interface StatCardProps {
  icon: string;
  value: string | number;
  label: string;
  delta?: string;
}

export function StatCard({ icon, value, label, delta }: StatCardProps) {
  return (
    <div className="stat-card">
      <p className="text-3xl mb-1">{icon}</p>
      <p className="text-2xl font-bold text-text-primary">{value}</p>
      <p className="text-sm text-text-secondary">{label}</p>
      {delta && <p className="text-sm text-accent-secondary mt-1">{delta}</p>}
    </div>
  );
}
