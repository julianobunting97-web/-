import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import PortfolioMotion from './components/PortfolioMotion'
import PortfolioCard from './components/PortfolioCard'
import ProfileCard from './components/ProfileCard'
import { ProceduralVideoBackground } from './components/ProceduralVideoBackground'
import portraitCaoShuo from './assets/portrait-cao-shuo.png'

const contactEmail = 'julianobunting97@gmail.com'
const gmailComposeUrl = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + contactEmail

const navigation = [
  { label: '首页', href: '#top' },
  { label: '个人经历', href: '#about' },
  { label: '精选项目', href: '#projects' },
  { label: '个人优势', href: '#strengths' },
  { label: '联系我', href: '#contact' },
]

const profileStats = [
  { value: '3.86 / 4.0', label: 'GPA' },
  { value: '2 / 40', label: '学年成绩排名' },
  { value: '7 / 40', label: '学年综测排名' },
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

const park1532Images = [
  { title: '效果图 01', meta: '生态休闲节点', src: '/portfolio/1532-park/renders/render-01.jpeg' },
  { title: '效果图 02', meta: '场地细节表达', src: '/portfolio/1532-park/renders/render-02.png' },
  { title: '效果图 03', meta: '公共空间视角', src: '/portfolio/1532-park/renders/render-03.jpeg' },
  { title: '效果图 04', meta: '景观动线片段', src: '/portfolio/1532-park/renders/render-04.jpeg' },
  { title: '效果图 05', meta: '节点氛围塑造', src: '/portfolio/1532-park/renders/render-05.jpeg' },
  { title: '效果图 06', meta: '空间体验补充', src: '/portfolio/1532-park/renders/render-06.jpeg' },
  { title: '效果图 07', meta: '场地界面细节', src: '/portfolio/1532-park/renders/render-07.png' },
  { title: '效果图 08', meta: '夜景氛围片段', src: '/portfolio/1532-park/renders/render-08.jpeg' },
  { title: '效果图 09', meta: '休闲节点视角', src: '/portfolio/1532-park/renders/render-09.jpeg' },
  { title: '效果图 10', meta: '公共设施细节', src: '/portfolio/1532-park/renders/render-10.png' },
  { title: '效果图 11', meta: '景观构筑物视角', src: '/portfolio/1532-park/renders/render-11.jpeg' },
  { title: '效果图 12', meta: '空间材质表达', src: '/portfolio/1532-park/renders/render-12.png' },
  { title: '效果图 13', meta: '场景体验补充', src: '/portfolio/1532-park/renders/render-13.png' },
  { title: '效果图 14', meta: '节点近景表达', src: '/portfolio/1532-park/renders/render-14.jpeg' },
  { title: '效果图 15', meta: '项目细节收束', src: '/portfolio/1532-park/renders/render-15.jpeg' },
]

const park1532Videos = [
  {
    title: '项目短片 01',
    meta: 'Bilibili 外链 / 方案汇报短片',
    embedUrl: 'https://player.bilibili.com/player.html?bvid=BV1nRMh6LEZs&page=1&t=1&high_quality=1&danmaku=0',
    externalUrl: 'https://www.bilibili.com/video/BV1nRMh6LEZs?t=1.4',
    poster: '/portfolio/1532-park-cover.jpg',
  },
]

const office1532Images = [
  { title: '效果图 01', meta: '胡桃木会议桌细节', src: '/portfolio/1532-office/renders/render-01.jpeg' },
  { title: '效果图 02', meta: '吧台空间', src: '/portfolio/1532-office/renders/render-02.png' },
  { title: '效果图 03', meta: '办公区白天', src: '/portfolio/1532-office/renders/render-03.png' },
  { title: '效果图 04', meta: '办公区夜景', src: '/portfolio/1532-office/renders/render-04.png' },
  { title: '效果图 05', meta: '办公空间视角', src: '/portfolio/1532-office/renders/render-05.png' },
  { title: '效果图 06', meta: '创意会议室', src: '/portfolio/1532-office/renders/render-06.jpeg' },
  { title: '效果图 07', meta: '大厅空间', src: '/portfolio/1532-office/renders/render-07.png' },
  { title: '效果图 08', meta: '隔音舱', src: '/portfolio/1532-office/renders/render-08.png' },
  { title: '效果图 09', meta: '公共办公区夜景', src: '/portfolio/1532-office/renders/render-09.png' },
  { title: '效果图 10', meta: '公共办公区域', src: '/portfolio/1532-office/renders/render-10.png' },
  { title: '效果图 11', meta: '机房空间', src: '/portfolio/1532-office/renders/render-11.jpeg' },
  { title: '效果图 12', meta: '景观休闲区', src: '/portfolio/1532-office/renders/render-12.jpg' },
  { title: '效果图 13', meta: '私密洽谈室', src: '/portfolio/1532-office/renders/render-13.png' },
  { title: '效果图 14', meta: '展览空间', src: '/portfolio/1532-office/renders/render-14.png' },
]

const familyHomeImages = [
  { title: '效果图 01', meta: '客厅空间', src: '/portfolio/family-home/renders/render-01.jpeg' },
  { title: '效果图 02', meta: '餐厅空间', src: '/portfolio/family-home/renders/render-02.jpeg' },
  { title: '效果图 03', meta: '直播间', src: '/portfolio/family-home/renders/render-03.png' },
  { title: '效果图 04', meta: '老年房间', src: '/portfolio/family-home/renders/render-04.png' },
  { title: '效果图 05', meta: '卫生间', src: '/portfolio/family-home/renders/render-05.png' },
]

const singleApartmentImages = [
  { title: '效果图 01', meta: '公寓主视角', src: '/portfolio/single-apartment/renders/render-01.png' },
  { title: '效果图 02', meta: '厨房空间', src: '/portfolio/single-apartment/renders/render-02.jpeg' },
  { title: '效果图 03', meta: '电竞房', src: '/portfolio/single-apartment/renders/render-03.jpeg' },
  { title: '摄影图 01', meta: '厨房摄影', src: '/portfolio/single-apartment/renders/photo-kitchen-01.png' },
  { title: '摄影图 02', meta: '客厅摄影 01', src: '/portfolio/single-apartment/renders/photo-living-01.png' },
  { title: '摄影图 03', meta: '客厅摄影 02', src: '/portfolio/single-apartment/renders/photo-living-02.png' },
  { title: '摄影图 04', meta: '客厅摄影 03', src: '/portfolio/single-apartment/renders/photo-living-03.png' },
  { title: '摄影图 05', meta: '客厅摄影 04', src: '/portfolio/single-apartment/renders/photo-living-04.png' },
  { title: '摄影图 06', meta: '电竞房摄影', src: '/portfolio/single-apartment/renders/photo-gaming-01.png' },
]

const courtyardImages = [
  { title: '效果图 01', meta: '前院空间', src: '/portfolio/courtyard/renders/render-01.jpeg' },
  { title: '效果图 02', meta: '后院空间', src: '/portfolio/courtyard/renders/render-02.jpeg' },
  { title: '效果图 03', meta: '侧道夜景', src: '/portfolio/courtyard/renders/render-03.jpeg' },
  { title: '效果图 04', meta: '影壁墙', src: '/portfolio/courtyard/renders/render-04.jpeg' },
]

const conceptSpaceImages = [
  { title: '效果图 01', meta: '建筑全貌', src: '/portfolio/concept-space/renders/render-01.png' },
  { title: '效果图 02', meta: '建筑特写', src: '/portfolio/concept-space/renders/render-02.png' },
  { title: '效果图 03', meta: '一层空间', src: '/portfolio/concept-space/renders/render-03.jpg' },
  { title: '效果图 04', meta: '二楼空间', src: '/portfolio/concept-space/renders/render-04.png' },
  { title: '效果图 05', meta: '俯视图', src: '/portfolio/concept-space/renders/render-05.png' },
  { title: '效果图 06', meta: '侧视图', src: '/portfolio/concept-space/renders/render-06.png' },
  { title: '效果图 07', meta: '室外瀑布', src: '/portfolio/concept-space/renders/render-07.png' },
  { title: '效果图 08', meta: '室外街景', src: '/portfolio/concept-space/renders/render-08.png' },
  { title: '效果图 09', meta: '室外摆拍', src: '/portfolio/concept-space/renders/render-09.png' },
  { title: '效果图 10', meta: '室外散步', src: '/portfolio/concept-space/renders/render-10.png' },
  { title: '效果图 11', meta: '特写摄影', src: '/portfolio/concept-space/renders/render-11.png' },
  { title: '效果图 12', meta: '蝴蝶意象', src: '/portfolio/concept-space/renders/render-12.png' },
]

const conceptSpaceVideos = [
  {
    title: '项目短片 01',
    meta: 'Bilibili 外链 / 海洋艺术展馆',
    embedUrl: 'https://player.bilibili.com/player.html?bvid=BV1pXMh62EA9&page=1&t=37&high_quality=1&danmaku=0',
    externalUrl: 'https://www.bilibili.com/video/BV1pXMh62EA9?t=37.1',
    poster: '/portfolio/concept-space/videos/concept-space-poster.jpg',
  },
]

const projectCards = [
  {
    slug: '1532-park',
    title: '潍坊市 1532 产业园改造项目',
    category: '景观更新 / 实践项目',
    period: '2026.05 - 2026.06',
    description:
      '以潍坊世纪公园更新为背景，围绕公共空间、生态休闲与城市记忆展开改造设计，通过展板、效果图与短片呈现完整方案叙事。',
    points: ['效果图展示', '短片展示'],
    image: '/portfolio/1532-park-cover.jpg',
    boards: [
      { src: '/portfolio/1532-park-cover.jpg', alt: '潍坊市 1532 产业园改造项目海报' },
      { src: '/portfolio/1532-park/boards/board-01.jpg', alt: '潍坊市 1532 产业园改造项目展板 1' },
      { src: '/portfolio/1532-park/boards/board-02.jpg', alt: '潍坊市 1532 产业园改造项目展板 2' },
    ],
    layout: 'wide',
    visualMode: 'poster',
    media: {
      images: park1532Images,
      videos: park1532Videos,
    },
  },
  {
    slug: '1532-office',
    title: '1532 办公空间设计',
    category: '办公空间 / 室内设计',
    period: '空间改造',
    description:
      '围绕共享办公、会议交流、展览展示与休闲洽谈组织空间关系，在理性功能中加入更具温度的材质、灯光和开放式办公体验。',
    points: ['公共办公区', '会议空间', '展览空间', '洽谈区域'],
    image: '/portfolio/1532-office-cover.png',
    boards: [
      { src: '/portfolio/1532-office/boards/board-01.jpg', alt: '1532 办公空间设计展板 1' },
      { src: '/portfolio/1532-office/boards/board-02.jpg', alt: '1532 办公空间设计展板 2' },
    ],
    layout: 'wide',
    visualMode: 'poster',
    media: {
      images: office1532Images,
      videos: [],
    },
  },
  {
    slug: 'family-home',
    title: '三口之家侘寂风住宅设计',
    category: '住宅空间 / 室内设计',
    period: '家居方案',
    description:
      '以低饱和材质、自然肌理和柔和光线塑造安静克制的居住氛围，兼顾家庭成员的生活动线、休憩需求与空间情绪。',
    points: ['客厅', '餐厅', '直播间', '老人房'],
    image: '/portfolio/family-home-cover.jpeg',
    media: {
      images: familyHomeImages,
      videos: [],
    },
  },
  {
    slug: 'single-apartment',
    title: '单人公寓室内设计',
    category: '小户型 / 室内设计',
    period: '居住空间',
    description:
      '针对单人生活方式重构紧凑空间的功能效率，强化厨房、休息、娱乐和收纳之间的连续性，让小空间具备完整生活场景。',
    points: ['厨房', '电竞房', '紧凑动线', '功能整合'],
    image: '/portfolio/single-apartment-cover.png',
    media: {
      images: singleApartmentImages,
      videos: [],
    },
  },
  {
    slug: 'courtyard',
    title: '庭院景观设计',
    category: '庭院营造 / 景观设计',
    period: '庭院方案',
    description:
      '通过前院、后院、侧道和影壁墙组织归家路径与停留节点，结合夜景照明与植物层次，营造安静、有秩序的户外生活空间。',
    points: ['前院', '后院', '侧道夜景', '影壁墙'],
    image: '/portfolio/courtyard-cover.jpeg',
    media: {
      images: courtyardImages,
      videos: [],
    },
  },
  {
    slug: 'concept-space',
    title: '海洋艺术与生态科技概念空间',
    category: '概念空间 / AI 设计',
    period: '概念展馆',
    description:
      '以海洋艺术、生态科技与未来展陈为关键词，探索建筑体量、沉浸式空间和自然意象之间的关系，形成更具叙事感的概念场景。',
    points: ['概念建筑', '生态科技', '沉浸展陈', '短片表达'],
    image: '/portfolio/concept-space-cover.jpg',
    media: {
      images: conceptSpaceImages,
      videos: conceptSpaceVideos,
    },
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
  { label: '邮箱', value: contactEmail, href: gmailComposeUrl },
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

function ProjectVideoEmbed({ item }) {
  if (item.embedUrl) {
    return (
      <div className="project-video-embed">
        <iframe
          src={item.embedUrl}
          title={item.title}
          allow="fullscreen; autoplay; encrypted-media; picture-in-picture"
          allowFullScreen
          loading="lazy"
        />
        <a href={item.externalUrl} target="_blank" rel="noreferrer">
          在 Bilibili 打开
        </a>
      </div>
    )
  }

  return (
    <div className="project-video-player">
      <video src={item.src} poster={item.poster} controls preload="metadata" />
      <div className="project-video-controls" aria-label="视频快进控制">
        <button
          type="button"
          onClick={(event) => {
            const video = event.currentTarget.closest('.project-video-player')?.querySelector('video')
            if (video) {
              video.currentTime = Math.max(video.currentTime - 10, 0)
            }
          }}
        >
          后退 10s
        </button>
        <button
          type="button"
          onClick={(event) => {
            const video = event.currentTarget.closest('.project-video-player')?.querySelector('video')
            if (video) {
              video.currentTime += 10
            }
          }}
        >
          快进 10s
        </button>
      </div>
    </div>
  )
}

function ProjectDetailPage({ project, onOpenMedia, onOpenImage }) {
  const images = project.media?.images || []
  const videos = project.media?.videos || []

  return (
    <main className="project-detail-page" id="top">
      <section className="project-detail-hero">
        <div className="container project-detail-hero-grid">
          <div className="project-detail-copy">
            <a className="project-back-link" href="/#projects">
              返回精选项目
            </a>
            <p className="eyebrow">{project.category}</p>
            <h1>{project.title}</h1>
            <p>{project.description}</p>
            <div className="project-detail-actions">
              {images.length > 0 ? (
                <button
                  type="button"
                  className="button button-primary"
                  onClick={() =>
                    onOpenMedia({
                      type: 'images',
                      title: `${project.title} · 效果图展示`,
                      subtitle: '项目效果图已接入，可继续补充更多角度与细节图。',
                      items: images,
                    })
                  }
                >
                  查看全部效果图
                </button>
              ) : null}
              {videos.length > 0 ? (
                <button
                  type="button"
                  className="button button-ghost"
                  onClick={() =>
                    onOpenMedia({
                      type: 'videos',
                      title: `${project.title} · 短片展示`,
                      subtitle: '项目短片已接入，视频文件较大，首次播放可能需要一点缓冲。',
                      items: videos,
                    })
                  }
                >
                  播放项目短片
                </button>
              ) : null}
            </div>
          </div>
          <div className={`project-detail-cover${project.boards ? ' project-detail-cover-boards' : ''}`}>
            {project.boards ? (
              project.boards.map((board, index) => {
                const previewItem = {
                  ...board,
                  title: `展板 ${String(index + 1).padStart(2, '0')}`,
                  meta: project.title,
                }

                return (
                  <button
                    type="button"
                    key={board.src}
                    className="project-detail-board"
                    onClick={() =>
                      onOpenImage(
                        previewItem,
                        project.boards.map((item, boardIndex) => ({
                          ...item,
                          title: `展板 ${String(boardIndex + 1).padStart(2, '0')}`,
                          meta: project.title,
                        })),
                      )
                    }
                  >
                    <img src={board.src} alt={board.alt} />
                    <span>查看原图</span>
                  </button>
                )
              })
            ) : (
              <img src={project.image} alt={project.title} />
            )}
          </div>
        </div>
      </section>

      <section className="section project-detail-section">
        <div className="container">
          <SectionHeader
            index="01"
            title="项目图集"
            description="独立项目详情页，用于集中展示该项目的完整效果图与关键视觉素材。"
          />
          <div className="project-detail-gallery">
            {images.map((item) => (
              <article key={item.src} className="project-detail-gallery-card">
                <button type="button" onClick={() => onOpenImage(item, images)}>
                  <img src={item.src} alt={item.title} loading="lazy" />
                </button>
                <div>
                  <strong>{item.title}</strong>
                  <span>{item.meta}</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {videos.length > 0 ? (
        <section className="section project-detail-section">
          <div className="container">
            <SectionHeader
              index="02"
              title="项目短片"
              description="视频支持拖动进度条、快进和后退，适合展示空间叙事与方案动线。"
            />
            <div className="project-detail-video-list">
              {videos.map((item) => (
                <PortfolioCard
                  key={item.embedUrl || item.src}
                  className="project-detail-video-card motion-card"
                  variant="default"
                >
                  <ProjectVideoEmbed item={item} />
                  <div>
                    <strong>{item.title}</strong>
                    <span>{item.meta}</span>
                  </div>
                </PortfolioCard>
              ))}
            </div>
          </div>
        </section>
      ) : null}
    </main>
  )
}

export default function App() {
  const [navCompact, setNavCompact] = useState(false)
  const [projectMediaModal, setProjectMediaModal] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [pathname, setPathname] = useState(() => window.location.pathname)

  const activeProjectSlug = pathname.match(/^\/projects\/([^/]+)/)?.[1]
  const activeProject = projectCards.find((project) => project.slug === activeProjectSlug)
  const navHref = (href) => (activeProject ? `/${href}` : href)
  const previewItems = imagePreview?.items ?? (imagePreview ? [imagePreview] : [])
  const previewIndex = imagePreview?.index ?? 0
  const currentPreview = previewItems[previewIndex]
  const canSwitchPreview = previewItems.length > 1

  const openImagePreview = (item, items = [item]) => {
    const list = items.length ? items : [item]
    const index = Math.max(0, list.findIndex((entry) => entry.src === item.src))

    setImagePreview({ items: list, index })
  }

  const switchImagePreview = (direction) => {
    setImagePreview((preview) => {
      if (!preview?.items?.length) return preview

      const nextIndex = (preview.index + direction + preview.items.length) % preview.items.length
      return { ...preview, index: nextIndex }
    })
  }

  useEffect(() => {
    const handleScroll = () => {
      if (activeProject) {
        setNavCompact(window.scrollY > 80)
        return
      }

      const heroSection = document.getElementById('top')
      if (!heroSection) return

      setNavCompact(heroSection.getBoundingClientRect().bottom <= 96)
    }

    handleScroll()
    window.addEventListener('scroll', handleScroll, { passive: true })
    window.addEventListener('resize', handleScroll)

    return () => {
      window.removeEventListener('scroll', handleScroll)
      window.removeEventListener('resize', handleScroll)
    }
  }, [activeProject])

  useEffect(() => {
    const handlePopState = () => {
      setPathname(window.location.pathname)
    }

    window.addEventListener('popstate', handlePopState)
    return () => {
      window.removeEventListener('popstate', handlePopState)
    }
  }, [])

  useEffect(() => {
    if (!projectMediaModal && !imagePreview) return undefined

    const handleKeydown = (event) => {
      if (event.key === 'Escape') {
        if (imagePreview) {
          setImagePreview(null)
        } else {
          setProjectMediaModal(null)
        }
      } else if (imagePreview && event.key === 'ArrowLeft') {
        event.preventDefault()
        switchImagePreview(-1)
      } else if (imagePreview && event.key === 'ArrowRight') {
        event.preventDefault()
        switchImagePreview(1)
      }
    }

    window.addEventListener('keydown', handleKeydown)
    return () => {
      window.removeEventListener('keydown', handleKeydown)
    }
  }, [projectMediaModal, imagePreview])

  return (
    <div className="page-shell">
      <PortfolioMotion />
      <div className={`floating-nav${navCompact ? ' is-compact' : ''}`}>
        <div className={`container nav-surface${navCompact ? ' is-compact' : ''}`}>
          <a className="brand" href={activeProject ? '/' : '#top'}>
            <span className="brand-mark" />
            <span>CAO SHUO / PORTFOLIO</span>
          </a>
          <div className="nav-links">
            {navigation.map((item) => (
              <a key={item.href} className={item.href === '#top' ? 'is-active' : ''} href={navHref(item.href)}>
                {item.label}
              </a>
            ))}
          </div>
          <a
            className="button button-ghost nav-cta"
            href={gmailComposeUrl}
            target="_blank"
            rel="noreferrer"
          >
            联系我
          </a>
        </div>
      </div>

      {activeProject ? (
        <ProjectDetailPage
          project={activeProject}
          onOpenMedia={setProjectMediaModal}
          onOpenImage={openImagePreview}
        />
      ) : (
        <>
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
            <p className="eyebrow">环境设计本科在读 · 室内设计师 / AIGC 设计师 / 景观规划师</p>
            <h1>
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
              <div className="portrait-card-shell motion-card">
                <ProfileCard
                  className="portrait-card"
                  name="曹硕"
                  title="AIGC设计师"
                  handle="caoshuo"
                  status="Portfolio"
                  avatarUrl={portraitCaoShuo}
                  miniAvatarUrl={portraitCaoShuo}
                  showUserInfo={false}
                  enableTilt={true}
                  enableMobileTilt={false}
                  behindGlowEnabled
                  innerGradient="linear-gradient(160deg, rgba(255,123,0,0.18) 0%, rgba(255,255,255,0.02) 52%, rgba(36,56,84,0.22) 100%)"
                />
              </div>

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
                    {project.boards ? (
                      <div className="project-board-strip">
                        {project.boards.map((board, index) => {
                          const boardItems = project.boards.map((item, boardIndex) => ({
                            ...item,
                            title: `展板 ${String(boardIndex + 1).padStart(2, '0')}`,
                            meta: project.title,
                          }))

                          return (
                            <div className="project-board-item" key={board.src}>
                              <img className="motion-visual" src={board.src} alt={board.alt} />
                              <button
                                type="button"
                                className="project-board-open"
                                onClick={() => setImagePreview({ items: boardItems, index })}
                              >
                                查看原图
                              </button>
                            </div>
                          )
                        })}
                      </div>
                    ) : (
                      <img className="motion-visual" src={project.image} alt={project.title} />
                    )}
                  </div>
                  <div className="project-info">
                    <div className="project-topline">
                      <span>{project.category}</span>
                      <span>{project.period}</span>
                    </div>
                    <h3>{project.title}</h3>
                    <p>{project.description}</p>
                    <div className="project-points">
                      {project.media ? (
                        <>
                          <button
                            type="button"
                            className="project-media-trigger"
                            onClick={() =>
                              setProjectMediaModal({
                                type: 'images',
                                title: `${project.title} · 效果图展示`,
                                subtitle: '项目效果图已接入，可继续补充更多角度与细节图。',
                                items: project.media.images,
                              })
                            }
                          >
                            <strong>效果图展示</strong>
                            <span>{project.media.images.length} 张效果图</span>
                          </button>
                          {project.media.videos.length > 0 ? (
                            <button
                              type="button"
                              className="project-media-trigger"
                              onClick={() =>
                                setProjectMediaModal({
                                  type: 'videos',
                                  title: `${project.title} · 短片展示`,
                                  subtitle: '项目短片已接入，视频文件较大，首次播放可能需要一点缓冲。',
                                  items: project.media.videos,
                                })
                              }
                            >
                              <strong>短片展示</strong>
                              <span>{project.media.videos.length} 个视频</span>
                            </button>
                          ) : null}
                        </>
                      ) : (
                        project.points.map((point) => <span key={point}>{point}</span>)
                      )}
                    </div>
                    <a className="project-detail-link" href={`/projects/${project.slug}`}>
                      查看项目详情
                    </a>
                    {project.media ? (
                      <div className="project-media-preview" aria-label={`${project.title} 更多媒体预览`}>
                        {project.media.images.slice(0, project.media.videos.length > 0 ? 3 : 4).map((item) => (
                          <button
                            key={item.src}
                            type="button"
                            className="project-media-thumb"
                            onClick={() =>
                              setProjectMediaModal({
                                type: 'images',
                                title: `${project.title} · 效果图展示`,
                                subtitle: '项目效果图已接入，可继续补充更多角度与细节图。',
                                items: project.media.images,
                              })
                            }
                          >
                            <img src={item.src} alt={item.title} loading="lazy" />
                            <span>{item.title}</span>
                          </button>
                        ))}
                        {project.media.videos.slice(0, 1).map((item) => (
                          <button
                            key={item.embedUrl || item.src}
                            type="button"
                            className="project-media-thumb is-video"
                            onClick={() =>
                              setProjectMediaModal({
                                type: 'videos',
                                title: `${project.title} · 短片展示`,
                                subtitle: '项目短片已接入，视频文件较大，首次播放可能需要一点缓冲。',
                                items: project.media.videos,
                              })
                            }
                          >
                            <img src={item.poster} alt={item.title} loading="lazy" />
                            <span>播放短片</span>
                          </button>
                        ))}
                      </div>
                    ) : null}
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
              <a
                className="button button-primary contact-button"
                href={gmailComposeUrl}
                target="_blank"
                rel="noreferrer"
              >
                发送邮件
              </a>
            </PortfolioCard>
          </div>
        </section>
      </main>
        </>
      )}

      {projectMediaModal ? createPortal(
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
                    {projectMediaModal.type === 'videos' ? (
                      <ProjectVideoEmbed item={item} />
                    ) : (
                      <img src={item.src} alt={item.title} loading="lazy" />
                    )}
                  </div>
                  <div className="project-media-slot-copy">
                    <div>
                      <strong>{item.title}</strong>
                      <small>{item.meta}</small>
                    </div>
                    {projectMediaModal.type === 'images' ? (
                      <button
                        type="button"
                        onClick={() => openImagePreview(item, projectMediaModal.items)}
                      >
                        查看原图
                      </button>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>,
        document.body,
      ) : null}

      {currentPreview ? createPortal(
        <div className="image-preview-backdrop" onClick={() => setImagePreview(null)}>
          <div className="image-preview-shell" onClick={(event) => event.stopPropagation()}>
            <div className="image-preview-head">
              <div>
                <p className="mini-label">Original Image</p>
                <h3>{currentPreview.title}</h3>
                <p>{currentPreview.meta}</p>
              </div>
              <button
                type="button"
                className="image-preview-close"
                onClick={() => setImagePreview(null)}
                aria-label="关闭原图预览"
              >
                ×
              </button>
            </div>
            <div className="image-preview-frame">
              {canSwitchPreview ? (
                <button
                  type="button"
                  className="image-preview-nav image-preview-nav-prev"
                  onClick={() => switchImagePreview(-1)}
                  aria-label="上一张图片"
                >
                  ‹
                </button>
              ) : null}
              <img src={currentPreview.src} alt={currentPreview.title} />
              {canSwitchPreview ? (
                <button
                  type="button"
                  className="image-preview-nav image-preview-nav-next"
                  onClick={() => switchImagePreview(1)}
                  aria-label="下一张图片"
                >
                  ›
                </button>
              ) : null}
              {canSwitchPreview ? (
                <span className="image-preview-count">
                  {previewIndex + 1} / {previewItems.length}
                </span>
              ) : null}
            </div>
          </div>
        </div>,
        document.body,
      ) : null}
    </div>
  )
}
