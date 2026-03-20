import { CATEGORIES } from "@/config/categories";

interface CategoryBadgeProps {
  category: string;
  label?: string;
}

export function CategoryBadge({ category, label }: CategoryBadgeProps) {
  const config = CATEGORIES[category];
  const icon = config?.icon || "📌";

  return (
    <span className="cat-badge inline-flex items-center gap-1">
      <span>{icon}</span>
      <span>{label || category}</span>
    </span>
  );
}
