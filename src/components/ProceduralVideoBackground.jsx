import { useEffect, useRef, useState } from 'react'
import heroBackground from '../assets/hero-background.mp4'
import Ferrofluid from './Ferrofluid'

const clamp = (value, min, max) => Math.min(Math.max(value, min), max)

export function ProceduralVideoBackground() {
  const canvasRef = useRef(null)
  const videoRef = useRef(null)
  const [showCanvas, setShowCanvas] = useState(true)
  const [videoReady, setVideoReady] = useState(false)

  useEffect(() => {
    const canvas = canvasRef.current

    if (!canvas) {
      return undefined
    }

    const context = canvas.getContext('2d')

    if (!context) {
      return undefined
    }

    let frameId = 0

    const particles = Array.from({ length: 26 }, (_, index) => ({
      size: 1.5 + (index % 4),
      amplitudeX: 120 + index * 10,
      amplitudeY: 74 + index * 8,
      offset: index * 0.42,
      speed: 0.14 + index * 0.004,
      seedX: 0.12 + (index % 6) * 0.13,
      seedY: 0.2 + (index % 5) * 0.15,
    }))

    const resize = () => {
      const ratio = clamp(window.devicePixelRatio || 1, 1, 1.75)
      canvas.width = Math.floor(window.innerWidth * ratio)
      canvas.height = Math.floor(window.innerHeight * ratio)
    }

    const drawGlow = (x, y, radius, color) => {
      const gradient = context.createRadialGradient(x, y, 0, x, y, radius)
      gradient.addColorStop(0, color)
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)')
      context.fillStyle = gradient
      context.beginPath()
      context.arc(x, y, radius, 0, Math.PI * 2)
      context.fill()
    }

    const drawContourBand = (time, offset, color, lineWidth) => {
      const width = canvas.width
      const height = canvas.height

      context.beginPath()
      for (let x = -40; x <= width + 40; x += 12) {
        const wave =
          Math.sin(x * 0.0042 + time * 1.6 + offset) * 18 +
          Math.cos(x * 0.0018 - time * 1.1 + offset) * 34
        const y = height * (0.26 + offset * 0.08) + wave
        if (x === -40) {
          context.moveTo(x, y)
        } else {
          context.lineTo(x, y)
        }
      }
      context.strokeStyle = color
      context.lineWidth = lineWidth
      context.stroke()
    }

    const render = (timestamp = 0) => {
      const time = timestamp * 0.00018
      const width = canvas.width
      const height = canvas.height

      const baseGradient = context.createLinearGradient(0, 0, width, height)
      baseGradient.addColorStop(0, '#080203')
      baseGradient.addColorStop(0.42, '#140506')
      baseGradient.addColorStop(1, '#090506')
      context.fillStyle = baseGradient
      context.fillRect(0, 0, width, height)

      context.save()
      context.globalCompositeOperation = 'screen'
      drawGlow(width * 0.24, height * 0.24, width * 0.22, 'rgba(255, 98, 71, 0.12)')
      drawGlow(width * 0.7, height * 0.24, width * 0.18, 'rgba(255, 63, 28, 0.16)')
      drawGlow(
        width * (0.55 + Math.sin(time) * 0.06),
        height * (0.58 + Math.cos(time * 1.4) * 0.02),
        width * 0.3,
        'rgba(255, 39, 12, 0.18)',
      )
      context.restore()

      context.save()
      context.strokeStyle = 'rgba(255, 255, 255, 0.032)'
      context.lineWidth = 1
      for (let x = 0; x <= width; x += 90) {
        context.beginPath()
        context.moveTo(x, 0)
        context.lineTo(x, height)
        context.stroke()
      }
      for (let y = 0; y <= height; y += 90) {
        context.beginPath()
        context.moveTo(0, y)
        context.lineTo(width, y)
        context.stroke()
      }
      context.restore()

      for (let band = 0; band < 8; band += 1) {
        drawContourBand(time, band * 0.62, `rgba(255, 171, 159, ${0.014 + band * 0.006})`, 1)
      }

      context.save()
      context.fillStyle = 'rgba(255, 205, 193, 0.44)'
      particles.forEach((particle, index) => {
        const x =
          width * particle.seedX +
          Math.sin(time * particle.speed + particle.offset) * particle.amplitudeX
        const y =
          height * particle.seedY +
          Math.cos(time * (particle.speed + 0.07) + particle.offset * 1.4) * particle.amplitudeY
        const alpha = 0.16 + ((Math.sin(time * 3 + index) + 1) / 2) * 0.24

        context.globalAlpha = alpha
        context.beginPath()
        context.arc(x, y, particle.size, 0, Math.PI * 2)
        context.fill()
      })
      context.restore()

      context.save()
      context.strokeStyle = 'rgba(255, 168, 150, 0.08)'
      context.lineWidth = 1
      context.beginPath()
      context.moveTo(width * 0.58, 0)
      context.lineTo(width * 0.76, height)
      context.moveTo(width * 0.7, 0)
      context.lineTo(width * 0.88, height)
      context.stroke()
      context.restore()

      frameId = window.requestAnimationFrame(render)
    }

    resize()
    render()
    window.addEventListener('resize', resize)

    return () => {
      window.cancelAnimationFrame(frameId)
      window.removeEventListener('resize', resize)
    }
  }, [])

  useEffect(() => {
    const video = videoRef.current

    if (!video) {
      return undefined
    }

    let cancelled = false

    const attemptPlay = async () => {
      try {
        video.muted = true
        video.defaultMuted = true
        video.loop = true
        video.playsInline = true
        await video.play()
        if (!cancelled) {
          setVideoReady(true)
          setShowCanvas(false)
        }
      } catch {
        if (!cancelled) {
          setVideoReady(false)
          setShowCanvas(true)
        }
      }
    }

    attemptPlay()

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="hero-media">
      <video
        ref={videoRef}
        className={`hero-video${videoReady ? ' is-visible' : ''}`}
        autoPlay
        loop
        muted
        playsInline
        preload="auto"
        src={heroBackground}
        onCanPlay={() => {
          setVideoReady(true)
          setShowCanvas(false)
        }}
        onError={() => {
          setVideoReady(false)
          setShowCanvas(true)
        }}
      />
      <Ferrofluid
        className="hero-ferrofluid"
        colors={['#ffe7dc', '#ff6a42', '#ff2e18']}
        speed={0.52}
        scale={1.28}
        turbulence={1.28}
        fluidity={0.08}
        rimWidth={0.15}
        sharpness={3.8}
        shimmer={1.2}
        glow={1.8}
        flowDirection="up"
        opacity={0.48}
        mouseInteraction
        mouseStrength={0.8}
        mouseRadius={0.22}
        mouseDampening={0.12}
        mixBlendMode="screen"
      />
      <canvas
        ref={canvasRef}
        className={`hero-canvas${showCanvas ? ' is-visible' : ''}`}
        aria-hidden="true"
      />
    </div>
  )
}
