import BorderGlow from './BorderGlow'

const warmPalette = ['#ff4e2f', '#ff8a63', '#ffd4c0']
const emberPalette = ['#ff5d3a', '#ff784e', '#ffb48a']

const variants = {
  default: {
    edgeSensitivity: 28,
    glowColor: '12 100 72',
    backgroundColor: '#140b0d',
    borderRadius: 30,
    glowRadius: 34,
    glowIntensity: 1.1,
    coneSpread: 14,
    fillOpacity: 0.5,
    colors: warmPalette,
  },
  hero: {
    edgeSensitivity: 26,
    glowColor: '12 100 74',
    backgroundColor: '#160a0c',
    borderRadius: 28,
    glowRadius: 34,
    glowIntensity: 1.16,
    coneSpread: 13,
    fillOpacity: 0.62,
    colors: warmPalette,
  },
  visual: {
    edgeSensitivity: 24,
    glowColor: '14 100 76',
    backgroundColor: '#150a0b',
    borderRadius: 24,
    glowRadius: 32,
    glowIntensity: 1.18,
    coneSpread: 12,
    fillOpacity: 0.64,
    colors: emberPalette,
  },
  project: {
    edgeSensitivity: 24,
    glowColor: '13 100 74',
    backgroundColor: '#12080a',
    borderRadius: 32,
    glowRadius: 42,
    glowIntensity: 1.14,
    coneSpread: 14,
    fillOpacity: 0.58,
    colors: warmPalette,
  },
  mini: {
    edgeSensitivity: 34,
    glowColor: '14 100 76',
    backgroundColor: '#180d0f',
    borderRadius: 22,
    glowRadius: 24,
    glowIntensity: 1.04,
    coneSpread: 16,
    fillOpacity: 0.44,
    colors: emberPalette,
  },
  portrait: {
    edgeSensitivity: 22,
    glowColor: '12 100 72',
    backgroundColor: '#110709',
    borderRadius: 32,
    glowRadius: 46,
    glowIntensity: 1.14,
    coneSpread: 14,
    fillOpacity: 0.52,
    colors: warmPalette,
  },
}

export default function PortfolioCard({ variant = 'default', ...props }) {
  return <BorderGlow {...variants[variant]} {...props} />
}
