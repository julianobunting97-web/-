import { useEffect } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export default function PortfolioMotion() {
  useEffect(() => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduceMotion) return undefined

    const ctx = gsap.context(() => {
      gsap.set('.hero-topline, .eyebrow, .hero-caption, .hero-text, .hero-actions, .hero-meta-strip', {
        opacity: 0,
        y: 42,
      })
      gsap.set('.hero-title-cn, .hero-title-en', {
        opacity: 0,
        yPercent: 110,
        scaleY: 1.35,
        scaleX: 0.9,
        filter: 'blur(10px)',
      })
      gsap.set('.hero-video, .hero-ferrofluid', {
        scale: 1.12,
        opacity: 0,
      })
      gsap.set('.nav-surface', {
        y: -24,
        opacity: 0,
      })
      gsap.set('.hero-grid, .hero-vignette, .hero-overlay', {
        opacity: 0,
      })

      const heroTimeline = gsap.timeline({
        defaults: {
          ease: 'power3.out',
        },
      })

      heroTimeline
        .to('.hero-video', {
          opacity: 1,
          scale: 1,
          duration: 1.6,
          ease: 'power2.out',
        })
        .to(
          '.hero-ferrofluid',
          {
            opacity: 0.9,
            scale: 1,
            duration: 1.8,
            ease: 'power2.out',
          },
          '<',
        )
        .to(
          '.hero-grid, .hero-vignette, .hero-overlay',
          {
            opacity: (index) => (index === 0 ? 0.22 : 1),
            duration: 1.2,
            stagger: 0.08,
          },
          '-=1.2',
        )
        .to(
          '.nav-surface',
          {
            y: 0,
            opacity: 1,
            duration: 1.1,
            ease: 'power3.out',
          },
          '-=0.9',
        )
        .to(
          '.hero-title-cn',
          {
            opacity: 1,
            yPercent: 0,
            scaleY: 1,
            scaleX: 1,
            filter: 'blur(0px)',
            duration: 1.3,
            ease: 'power4.out',
          },
          '-=0.55',
        )
        .to(
          '.hero-title-en',
          {
            opacity: 1,
            yPercent: 0,
            scaleY: 1,
            scaleX: 1,
            filter: 'blur(0px)',
            duration: 1.45,
            ease: 'power4.out',
          },
          '-=1.05',
        )
        .to(
          '.hero-topline, .eyebrow, .hero-caption, .hero-text, .hero-actions, .hero-meta-strip',
          {
            opacity: 1,
            y: 0,
            duration: 1.1,
            stagger: 0.09,
            ease: 'power3.out',
          },
          '-=1.05',
        )

      gsap.to('.hero-video', {
        yPercent: 6,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 1.2,
        },
      })

      gsap.to('.hero-ferrofluid', {
        yPercent: -4,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 1.4,
        },
      })

      gsap.utils.toArray('.section').forEach((section) => {
        const heading = section.querySelector('.section-display')
        const cards = section.querySelectorAll('.motion-card')
        const visuals = section.querySelectorAll('.motion-visual')

        if (heading) {
          gsap.set(heading, {
            opacity: 0,
            yPercent: 36,
            scale: 1.08,
            filter: 'blur(12px)',
          })

          gsap.to(heading, {
            opacity: 0.14,
            yPercent: 0,
            scale: 1,
            filter: 'blur(0px)',
            duration: 1.8,
            ease: 'power4.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 74%',
              end: 'top 34%',
              scrub: 0.8,
            },
          })
        }

        if (cards.length) {
          gsap.set(cards, {
            opacity: 0,
            y: 86,
            scale: 0.94,
            rotateX: -8,
          })

          gsap.to(cards, {
            opacity: 1,
            y: 0,
            scale: 1,
            rotateX: 0,
            duration: 1.25,
            stagger: 0.12,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 60%',
            },
          })
        }

        visuals.forEach((visual, index) => {
          gsap.fromTo(
            visual,
            {
              clipPath: 'inset(0 0 100% 0 round 24px)',
              y: 56,
              scale: 1.06,
            },
            {
              clipPath: 'inset(0 0 0% 0 round 24px)',
              y: 0,
              scale: 1,
              duration: 1.6,
              delay: index * 0.06,
              ease: 'power3.out',
              scrollTrigger: {
                trigger: visual,
                start: 'top 76%',
              },
            },
          )

          gsap.to(visual, {
            yPercent: -5,
            ease: 'none',
            scrollTrigger: {
              trigger: visual,
              start: 'top bottom',
              end: 'bottom top',
              scrub: 1.2,
            },
          })
        })
      })
    })

    return () => {
      ctx.revert()
      ScrollTrigger.getAll().forEach((trigger) => trigger.kill())
    }
  }, [])

  return null
}

