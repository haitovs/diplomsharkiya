export interface CityConfig {
  name: string;
  region: string;
  lat: number;
  lon: number;
}

export const CITIES: CityConfig[] = [
  { name: "Ashgabat", region: "Ahal", lat: 37.9601, lon: 58.3261 },
  { name: "Mary", region: "Mary", lat: 37.6005, lon: 61.8302 },
  { name: "Türkmenabat", region: "Lebap", lat: 39.0733, lon: 63.5786 },
  { name: "Dashoguz", region: "Dashoguz", lat: 41.8387, lon: 59.9650 },
  { name: "Balkanabat", region: "Balkan", lat: 39.5104, lon: 54.3672 },
  { name: "Awaza", region: "Turkmenbashi", lat: 40.0224, lon: 52.9693 },
];

export const CITY_NAMES = CITIES.map(c => c.name);

export const CITY_COORDS: Record<string, { lat: number; lon: number }> = Object.fromEntries(
  CITIES.map(c => [c.name, { lat: c.lat, lon: c.lon }])
);

export const DEFAULT_CENTER = { lat: 37.9601, lon: 58.3261 };
export const DEFAULT_ZOOM = 11;
