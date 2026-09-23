import BorderGlow from './BorderGlow'

const sagePalette = ['#61745a', '#a4af95', '#d9dfcf']

const variants = {
  default: {
    edgeSensitivity: 28,
    glowColor: '100 18 48',
    backgroundColor: '#fbfaf6',
    borderRadius: 8,
    glowRadius: 34,
    glowIntensity: 0.24,
    coneSpread: 14,
    fillOpacity: 0.06,
    colors: sagePalette,
  },
  hero: {
    edgeSensitivity: 26,
    glowColor: '100 18 48',
    backgroundColor: '#f2f3ec',
    borderRadius: 8,
    glowRadius: 34,
    glowIntensity: 0.24,
    coneSpread: 13,
    fillOpacity: 0.06,
    colors: sagePalette,
  },
  visual: {
    edgeSensitivity: 24,
    glowColor: '100 18 48',
    backgroundColor: '#f1f2e9',
    borderRadius: 6,
    glowRadius: 32,
    glowIntensity: 0.24,
    coneSpread: 12,
    fillOpacity: 0.06,
    colors: sagePalette,
  },
  project: {
    edgeSensitivity: 24,
    glowColor: '100 18 48',
    backgroundColor: '#fbfaf6',
    borderRadius: 8,
    glowRadius: 42,
    glowIntensity: 0.24,
    coneSpread: 14,
    fillOpacity: 0.06,
    colors: sagePalette,
  },
  mini: {
    edgeSensitivity: 34,
    glowColor: '100 18 48',
    backgroundColor: '#f0f1e9',
    borderRadius: 4,
    glowRadius: 24,
    glowIntensity: 0.16,
    coneSpread: 16,
    fillOpacity: 0.04,
    colors: sagePalette,
  },
  portrait: {
    edgeSensitivity: 22,
    glowColor: '100 18 48',
    backgroundColor: '#e8ecdf',
    borderRadius: 8,
    glowRadius: 46,
    glowIntensity: 0.24,
    coneSpread: 14,
    fillOpacity: 0.06,
    colors: sagePalette,
  },
}

export default function PortfolioCard({ variant = 'default', ...props }) {
  return <BorderGlow {...variants[variant]} {...props} />
}
