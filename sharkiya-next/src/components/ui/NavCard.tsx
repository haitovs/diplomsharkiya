import Link from "next/link";

interface NavCardProps {
  href: string;
  icon: string;
  title: string;
  description: string;
  linkText: string;
}

export function NavCard({ href, icon, title, description, linkText }: NavCardProps) {
  return (
    <Link href={href} className="nav-card block">
      <p className="text-3xl mb-3">{icon}</p>
      <h4 className="text-lg font-semibold text-text-primary mb-1">{title}</h4>
      <p className="text-sm text-text-secondary mb-3">{description}</p>
      <span className="text-accent-primary text-sm font-medium">{linkText} →</span>
    </Link>
  );
}
