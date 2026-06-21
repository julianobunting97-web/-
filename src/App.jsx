import { useEffect, useState } from 'react'
import portraitArt from './assets/portrait-abstract.svg'
import projectAi from './assets/project-ai.svg'
import projectLandscape from './assets/project-landscape.svg'
import projectPoster1532 from './assets/project-1532-poster.png'
import projectSketch from './assets/project-sketch.svg'
import projectStudio from './assets/project-studio.svg'
import PortfolioMotion from './components/PortfolioMotion'
import PortfolioCard from './components/PortfolioCard'
import { ProceduralVideoBackground } from './components/ProceduralVideoBackground'

const navigation = [
  { label: '首页', href: '#top' },
  { label: '个人经历', href: '#about' },
  { label: '精选项目', href: '#projects' },
  { label: '个人优势', href: '#strengths' },
  { label: '联系我', href: '#contact' },
]

const profileStats = [
  { value: '3.86 / 4.0', label: 'GPA' },
  { value: '3 / 40', label: '学年成绩排名' },
  { value: '9 / 40', label: '学年综测排名' },
  { value: '10+', label: '设计与 AI 工具' },
]

const profileDetails = [
  { label: '姓名', value: '曹硕' },
  { label: '学校', value: '潍坊学院' },
  { label: '专业', value: '环境设计（本科）' },
  { label: '地点', value: '山东省潍坊市奎文区' },
]

const heroPosterMetrics = [
  { value: '3.86', label: 'GPA' },
  { value: '3/40', label: '专业排名' },
  { value: '2027', label: '毕业时间' },
]

const projectCards = [
  {
    title: '潍坊市 1532 产业园改造项目',
    category: '景观更新 / 实践项目',
    period: '2026.05 - 2026.06',
    description:
      '围绕产业园公共空间更新展开场地测量、居民访谈、调研整理、展会讲解与效果图表达，在真实语境中平衡设计叙事、使用需求与落地可行性。',
    points: ['效果图展示', '短片展示'],
    image: projectPoster1532,
    layout: 'wide',
    visualMode: 'poster',
  },
  {
    title: '古建筑写生与空间观察研究',
    category: '手绘表达 / 研究作品',
    period: '写生实践',
    description:
      '以宏村、南屏等地古建筑为观察对象，通过速写与空间分析训练对结构秩序、尺度节奏与场所氛围的敏感度，沉淀更扎实的空间表达能力。',
    points: ['建筑速写', '空间比例判断', '场景氛围提炼'],
    image: projectSketch,
  },
  {
    title: 'AI 辅助空间概念生成实验',
    category: 'AI 设计 / 方法探索',
    period: '持续进行',
    description:
      '将 Stable Diffusion、ComfyUI 与 Codex 融入前期概念生成流程，用更快的方式验证材质、氛围与空间母题，提升方案发散效率与沟通直观度。',
    points: ['概念情绪版', '生成式草图', '方案方向筛选'],
    image: projectAi,
  },
  {
    title: '环境设计课程体系作品集合',
    category: '室内设计 / 学术作品',
    period: '2023 - 2026',
    description:
      '覆盖室内、家居、灯具、建筑模型与景观规划等课程内容，形成从概念构思、方案深化到图面表达的完整训练路径。',
    points: ['CAD 制图', '3D 建模', 'V-Ray 渲染', 'PS 后期表达'],
    image: projectStudio,
  },
]

const strengths = [
  {
    title: '跨领域空间视角',
    text: '同时关注室内、景观与建筑语境，能在不同尺度下组织空间逻辑与体验节奏。',
  },
  {
    title: 'AI 驱动的概念效率',
    text: '熟悉 Stable Diffusion、ComfyUI 与 Codex，可将灵感发散、图像实验与方案沟通接入设计流程。',
  },
  {
    title: '手绘与数字表达并行',
    text: '兼顾建筑速写功底与数字工具能力，从草图到渲染都能维持统一的审美与表达精度。',
  },
  {
    title: '细节意识与协作能力',
    text: '注重落地可行性，善于沟通协作，能快速适应项目节奏并高效推进任务。',
  },
]

const honors = [
  '普通话二级甲等',
  '2024 学年暑期“三下乡”社会实践优秀个人',
  '2023-2024 学年潍坊学院三等奖学金',
  '2024-2025 学年潍坊学院优秀学生',
  '2024-2025 学年潍坊学院二等奖学金',
]

const contactItems = [
  { label: '电话', value: '133 6144 4417', href: 'tel:13361444417' },
  { label: '邮箱', value: '13361444417@163.com', href: 'mailto:13361444417@163.com' },
  { label: '城市', value: '山东省潍坊市', href: null },
]

function SectionHeader({ index, title, description }) {
  return (
    <div className="section-header">
      <div className="section-index">{index}</div>
      <div>
        <p className="section-kicker">{title}</p>
        <p className="section-description">{description}</p>
      </div>
      <div className="section-display" aria-hidden="true">
        {title}
      </div>
    </div>
  )
}

export default function App() {
  const [navCompact, setNavCompact] = useState(false)
  const [projectMediaModal, setProjectMediaModal] = useState(null)

  useEffect(() => {
    const handleScroll = () => {
      const heroSection = document.getElementById('top')
      if (!heroSection) return

      const trigger = Math.max(heroSection.offsetHeight - window.innerHeight * 0.18, 120)

      setNavCompact(window.scrollY >= trigger)
    }

    handleScroll()
    window.addEventListener('scroll', handleScroll, { passive: true })

    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  useEffect(() => {
    if (!projectMediaModal) return undefined

    const handleKeydown = (event) => {
      if (event.key === 'Escape') {
        setProjectMediaModal(null)
      }
    }

    window.addEventListener('keydown', handleKeydown)
    return () => {
      window.removeEventListener('keydown', handleKeydown)
    }
  }, [projectMediaModal])

  return (
    <div className="page-shell">
      <PortfolioMotion />
      <div className={`floating-nav${navCompact ? ' is-compact' : ''}`}>
        <div className={`container nav-surface${navCompact ? ' is-compact' : ''}`}>
          <a className="brand" href="#top">
            <span className="brand-mark" />
            <span>CAO SHUO / PORTFOLIO</span>
          </a>
          <div className="nav-links">
            {navigation.map((item) => (
              <a key={item.href} className={item.href === '#top' ? 'is-active' : ''} href={item.href}>
                {item.label}
              </a>
            ))}
          </div>
          <a className="button button-ghost nav-cta" href="mailto:13361444417@163.com">
            联系我
          </a>
        </div>
      </div>

      <header className="hero" id="top">
        <ProceduralVideoBackground />
        <div className="hero-overlay" />
        <div className="hero-grid" />
        <div className="hero-vignette hero-vignette-top" />
        <div className="hero-vignette hero-vignette-bottom" />

        <div className="container hero-layout">
          <div className="hero-copy">
            <div className="hero-topline">
              <span className="hero-kicker">CAO SHUO PORTFOLIO</span>
              <span className="hero-separator" />
              <span className="hero-kicker">INTERIOR / AI / LANDSCAPE</span>
            </div>
            <p className="eyebrow">环境设计本科在读 · 室内设计师 / AI 设计师 / 景观规划师</p>
            <h1>
              <span className="hero-title-cn">CAO SHUO</span>
              <span className="hero-title-en">PORTFOLIO</span>
            </h1>
            <p className="hero-caption">空间灵感生成，克制表达，精准落地。</p>
            <p className="hero-text">
              聚焦室内设计、AI 概念生成与景观规划实践，
              用更清晰的空间逻辑和更高效的表达方式推动方案成立。
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#projects">
                查看精选项目
              </a>
              <a className="button button-secondary" href="mailto:13361444417@163.com">
                发起联系
              </a>
            </div>
            <div className="hero-meta-strip">
              {heroPosterMetrics.map((item) => (
                <div key={item.label} className="hero-meta-item">
                  <strong>{item.value}</strong>
                  <span>{item.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main>
        <section className="section" id="about">
          <div className="container">
            <SectionHeader
              index="01"
              title="个人经历"
              description="以真实经历为核心整理的个人介绍、联系方式与项目数据。"
            />

            <div className="about-grid">
              <PortfolioCard className="portrait-card motion-card" variant="portrait">
                <img className="motion-visual" src={portraitArt} alt="曹硕人物形象占位图" />
              </PortfolioCard>

              <PortfolioCard className="about-card motion-card" variant="default">
                <div className="about-copy">
                  <p className="mini-label">About Me</p>
                  <h2>环境设计本科在读，专注空间表达、设计逻辑与 AI 工具融合。</h2>
                  <p>
                    我目前就读于潍坊学院环境设计专业，具备扎实的专业理论基础与实践能力，熟悉
                    CAD、3Dmax、V-Ray、Photoshop，也在主动将 Stable Diffusion、ComfyUI、Codex
                    融入设计流程。
                  </p>
                  <p>
                    我关注空间从概念到落地的完整路径，擅长在细节控制、视觉表达和沟通协作之间找到平衡，
                    也希望通过更多实践项目持续提升自己的设计判断与执行力。
                  </p>
                </div>

                <div className="detail-grid">
                  {profileDetails.map((item) => (
                    <PortfolioCard key={item.label} className="detail-card motion-card" variant="mini">
                      <span>{item.label}</span>
                      <strong>{item.value}</strong>
                    </PortfolioCard>
                  ))}
                </div>

                <div className="stats-grid">
                  {profileStats.map((item) => (
                    <PortfolioCard key={item.label} className="stat-card motion-card" variant="mini">
                      <strong>{item.value}</strong>
                      <span>{item.label}</span>
                    </PortfolioCard>
                  ))}
                </div>

                <div className="contact-strip">
                  {contactItems.map((item) =>
                    item.href ? (
                      <PortfolioCard
                        key={item.label}
                        as="a"
                        className="contact-strip-card motion-card"
                        href={item.href}
                        variant="mini"
                      >
                        <span>{item.label}</span>
                        <strong>{item.value}</strong>
                      </PortfolioCard>
                    ) : (
                      <PortfolioCard key={item.label} className="contact-strip-card motion-card" variant="mini">
                        <span>{item.label}</span>
                        <strong>{item.value}</strong>
                      </PortfolioCard>
                    ),
                  )}
                </div>

                <div className="honor-block">
                  <p className="mini-label">荣誉与认可</p>
                  <div className="honor-list">
                    {honors.map((honor) => (
                      <span key={honor}>{honor}</span>
                    ))}
                  </div>
                </div>
              </PortfolioCard>
            </div>
          </div>
        </section>

        <section className="section" id="projects">
          <div className="container">
            <SectionHeader
              index="02"
              title="精选项目"
              description="首版先用高质感占位视觉承载内容结构，后续可替换为你的真实作品图。"
            />

            <div className="projects-grid">
              {projectCards.map((project) => (
                <PortfolioCard
                  as="article"
                  key={project.title}
                  className={`project-card motion-card ${project.layout ? `project-card-${project.layout}` : ''}`}
                  variant="project"
                >
                  <div
                    className={`project-visual${project.visualMode ? ` project-visual-${project.visualMode}` : ''}`}
                  >
                    <img className="motion-visual" src={project.image} alt={project.title} />
                  </div>
                  <div className="project-info">
                    <div className="project-topline">
                      <span>{project.category}</span>
                      <span>{project.period}</span>
                    </div>
                    <h3>{project.title}</h3>
                    <p>{project.description}</p>
                    <div className="project-points">
                      {project.title === '潍坊市 1532 产业园改造项目' ? (
                        <>
                          <button
                            type="button"
                            className="project-media-trigger"
                            onClick={() =>
                              setProjectMediaModal({
                                type: 'images',
                                title: '效果图展示',
                                subtitle: '预留 10 张效果图素材位，可后续逐张替换。',
                                items: Array.from({ length: 10 }, (_, index) => ({
                                  title: `效果图 ${String(index + 1).padStart(2, '0')}`,
                                  meta: 'PNG / JPG / WebP',
                                })),
                              })
                            }
                          >
                            <strong>效果图展示</strong>
                            <span>10 张素材位</span>
                          </button>
                          <button
                            type="button"
                            className="project-media-trigger"
                            onClick={() =>
                              setProjectMediaModal({
                                type: 'videos',
                                title: '短片展示',
                                subtitle: '预留 3 个视频素材位，可后续接入本地 MP4 或外链视频。',
                                items: Array.from({ length: 3 }, (_, index) => ({
                                  title: `短片 ${String(index + 1).padStart(2, '0')}`,
                                  meta: 'MP4 / MOV / 16:9',
                                })),
                              })
                            }
                          >
                            <strong>短片展示</strong>
                            <span>3 个视频位</span>
                          </button>
                        </>
                      ) : (
                        project.points.map((point) => <span key={point}>{point}</span>)
                      )}
                    </div>
                  </div>
                </PortfolioCard>
              ))}
            </div>
          </div>
        </section>

        <section className="section" id="strengths">
          <div className="container">
            <SectionHeader
              index="03"
              title="个人优势"
              description="从技能结构、表达方式到协作意识，形成我当前的设计方法。"
            />

            <div className="strength-grid">
              {strengths.map((item, index) => (
                <PortfolioCard
                  key={item.title}
                  as="article"
                  className="strength-card motion-card"
                  variant="default"
                >
                  <span className="strength-index">{String(index + 1).padStart(2, '0')}</span>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </PortfolioCard>
              ))}
            </div>
          </div>
        </section>

        <section className="contact-stage" id="contact">
          <div className="container contact-layout">
            <div className="contact-copy">
              <p className="eyebrow">LET'S BUILD SOMETHING PRECISE</p>
              <h2>如果你正在寻找一位兼具空间审美、执行意识与 AI 设计理解的合作对象，我们可以聊聊。</h2>
              <p>
                目前可沟通实习机会、设计合作与作品集完善方向。这个首版网站已经为后续加入真实项目图、
                页面动效和案例详情预留好了结构。
              </p>
            </div>

            <PortfolioCard className="contact-card motion-card" variant="default">
              {contactItems.map((item) =>
                item.href ? (
                  <a key={item.label} className="contact-row" href={item.href}>
                    <span>{item.label}</span>
                    <strong>{item.value}</strong>
                  </a>
                ) : (
                  <div key={item.label} className="contact-row">
                    <span>{item.label}</span>
                    <strong>{item.value}</strong>
                  </div>
                ),
              )}
              <a className="button button-primary contact-button" href="mailto:13361444417@163.com">
                发送邮件
              </a>
            </PortfolioCard>
          </div>
        </section>
      </main>

      {projectMediaModal ? (
        <div className="project-modal-backdrop" onClick={() => setProjectMediaModal(null)}>
          <div className="project-modal-shell" onClick={(event) => event.stopPropagation()}>
            <div className="project-modal-head">
              <div>
                <p className="mini-label">Project Media</p>
                <h3>{projectMediaModal.title}</h3>
                <p>{projectMediaModal.subtitle}</p>
              </div>
              <button
                type="button"
                className="project-modal-close"
                onClick={() => setProjectMediaModal(null)}
                aria-label="关闭媒体弹层"
              >
                ×
              </button>
            </div>

            <div
              className={`project-media-grid${projectMediaModal.type === 'videos' ? ' is-video-grid' : ''}`}
            >
              {projectMediaModal.items.map((item) => (
                <div key={item.title} className="project-media-slot">
                  <div className="project-media-slot-visual">
                    <span>{projectMediaModal.type === 'videos' ? 'VIDEO' : 'IMAGE'}</span>
                  </div>
                  <strong>{item.title}</strong>
                  <small>{item.meta}</small>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
