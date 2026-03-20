interface PriceBadgeProps {
  price: number;
  freeText?: string;
}

export function PriceBadge({ price, freeText = "Free" }: PriceBadgeProps) {
  const isFree = price === 0;
  return (
    <span className={`price-badge ${isFree ? "price-free" : "price-paid"}`}>
      {isFree ? freeText : `${Math.round(price)} TMT`}
    </span>
  );
}
