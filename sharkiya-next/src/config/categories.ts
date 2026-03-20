export interface CategoryConfig {
  icon: string;
  color: string;
  hex: string;
  description: string;
}

export const CATEGORIES: Record<string, CategoryConfig> = {
  Music: { icon: "🎵", color: "purple", hex: "#A855F7", description: "Concerts, performances, and musical events" },
  Tech: { icon: "💻", color: "blue", hex: "#3B82F6", description: "Tech talks, workshops, and meetups" },
  Sports: { icon: "⚽", color: "green", hex: "#22C55E", description: "Sports events, games, and competitions" },
  Food: { icon: "🍽️", color: "orange", hex: "#F97316", description: "Food festivals, tastings, and culinary events" },
  Art: { icon: "🎨", color: "pink", hex: "#EC4899", description: "Art exhibitions, galleries, and workshops" },
  Market: { icon: "🛍️", color: "cadetblue", hex: "#5F9EA0", description: "Markets, fairs, and shopping events" },
  Film: { icon: "🎬", color: "red", hex: "#EF4444", description: "Movie screenings and film festivals" },
  Wellness: { icon: "🧘", color: "lightgreen", hex: "#4ADE80", description: "Yoga, meditation, and wellness activities" },
  Business: { icon: "💼", color: "darkblue", hex: "#1E40AF", description: "Business conferences and networking" },
  Science: { icon: "🔬", color: "purple", hex: "#8B5CF6", description: "Science fairs, lectures, and exhibitions" },
  Kids: { icon: "👶", color: "beige", hex: "#FBBF24", description: "Children's activities and family events" },
  Travel: { icon: "✈️", color: "lightblue", hex: "#38BDF8", description: "Travel expos and tourism events" },
  Community: { icon: "👥", color: "gray", hex: "#94A3B8", description: "Community gatherings and social events" },
};

export const CATEGORY_NAMES = Object.keys(CATEGORIES);
