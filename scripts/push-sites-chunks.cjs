// Recover a large unpublished Sites commit by pushing image assets in small batches.
// Run only in the isolated .sites-release checkout; receive the temporary credential on stdin.
const fs = require('node:fs/promises')
const path = require('node:path')
const { spawn } = require('node:child_process')

const projectId = 'appgprj_6ab38027664c8191b93fa378a6baab0e'
const checkout = path.resolve(__dirname, '../.sites-release')
const gitExe = 'E:\\comfyui桌面版\\Git\\cmd\\git.exe'

async function git(args, credential) {
  const env = { ...process.env, GIT_TERMINAL_PROMPT: '0' }
  const auth = []
  if (credential) {
    env.SITES_GIT_AUTHORIZATION = `Authorization: Bearer ${credential.token}`
    auth.push('-c', 'credential.helper=', '-c', 'http.extraHeader=', '-c', 'http.followRedirects=false', `--config-env=http.${credential.remote_url}.extraHeader=SITES_GIT_AUTHORIZATION`)
  }
  const result = await new Promise((resolve, reject) => {
    const child = spawn(gitExe, [...auth, ...args], { cwd: checkout, env, windowsHide: true })
    let stdout = ''
    let stderr = ''
    child.stdout.on('data', chunk => { stdout += chunk })
    child.stderr.on('data', chunk => { stderr += chunk })
    child.once('error', reject)
    child.once('close', code => resolve({ code, stdout, stderr }))
  })
  if (result.code !== 0) {
    throw new Error((result.stderr || result.stdout || `Git exited ${result.code}`).replaceAll(credential?.token || '', '[redacted]'))
  }
  return result.stdout.trim()
}

async function images(directory) {
  const files = []
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name)
    if (entry.isDirectory()) files.push(...await images(filename))
    else if (entry.name.endsWith('.full.webp')) files.push({ file: path.relative(checkout, filename).replaceAll('\\', '/'), size: (await fs.stat(filename)).size })
  }
  return files
}

async function push(credential, ref) {
  const head = await git(['rev-parse', 'HEAD'])
  await git(['push', credential.remote_url, `${head}:${ref}`], credential)
  console.log(`Pushed ${head.slice(0, 10)}`)
}

async function main(credential) {
  const manifest = JSON.parse(await fs.readFile(path.join(checkout, '.openai/hosting.json'), 'utf8'))
  if (manifest.project_id !== projectId) throw new Error('Site ID mismatch')
  if (new URL(credential.remote_url).hostname !== 'git.chatgpt-team.site') throw new Error('Unexpected Sites source host')
  if (!credential.remote_url.includes(projectId) || !credential.token) throw new Error('Invalid Site credential')
  const ref = `refs/heads/${credential.branch}`
  const remoteHead = (await git(['ls-remote', '--heads', credential.remote_url, ref], credential)).split(/\s+/)[0]
  const currentHead = await git(['rev-parse', 'HEAD'])
  const status = await git(['status', '--porcelain'])
  if (status) throw new Error('Release checkout must be clean before splitting the unpublished commit')
  if (await git(['rev-list', '--count', `${remoteHead}..${currentHead}`]) !== '1') throw new Error('Expected one unpublished local commit')

  await git(['reset', '--soft', remoteHead])
  await git(['restore', '--staged', '.'])
  const pending = await git(['status', '--porcelain'])
  const unexpected = pending.split('\n').filter(line => line.startsWith('?? ') && !line.endsWith('.full.webp'))
  if (unexpected.length) throw new Error(`Unexpected untracked files: ${unexpected.join(', ')}`)

  await git(['add', '-u'])
  await git(['-c', 'user.name=Codex', '-c', 'user.email=codex@localhost', '-c', 'commit.gpgsign=false', 'commit', '-m', 'Optimize mobile portfolio layout and assets'])
  await push(credential, ref)

  const sourceImages = (await images(path.join(checkout, 'public/portfolio'))).sort((a, b) => b.size - a.size)
  const groups = []
  for (const image of sourceImages) {
    let group = groups.find(current => current.bytes + image.size <= 14 * 1048576)
    if (!group) {
      group = { bytes: 0, files: [] }
      groups.push(group)
    }
    group.files.push(image.file)
    group.bytes += image.size
  }

  for (let index = 0; index < groups.length; index += 1) {
    await git(['add', '--', ...groups[index].files])
    await git(['-c', 'user.name=Codex', '-c', 'user.email=codex@localhost', '-c', 'commit.gpgsign=false', 'commit', '-m', `Add full-size portfolio images ${index + 1}/${groups.length}`])
    await push(credential, ref)
    console.log(`Batch ${index + 1}/${groups.length}: ${(groups[index].bytes / 1048576).toFixed(1)} MB`)
  }

  if (await git(['status', '--porcelain'])) throw new Error('Uncommitted release files remain')
  const finalHead = await git(['rev-parse', 'HEAD'])
  const pushedHead = (await git(['ls-remote', '--heads', credential.remote_url, ref], credential)).split(/\s+/)[0]
  if (finalHead !== pushedHead) throw new Error('Final source SHA was not confirmed on Sites')
  console.log(`Verified complete Sites source: ${finalHead}`)
}

async function readCredential() {
  return new Promise((resolve, reject) => {
    let value = ''
    const hidden = process.stdin.isTTY
    const finish = error => {
      process.stdin.removeListener('data', onData)
      process.stdin.removeListener('end', onEnd)
      if (hidden) process.stdin.setRawMode(false)
      process.stdin.pause()
      error ? reject(error) : resolve(JSON.parse(value))
    }
    const onData = chunk => {
      value += chunk
      if (value.length > 65536) finish(new Error('Credential input is too long'))
      else if (value.includes('\n') || value.includes('\r')) finish()
    }
    const onEnd = () => finish(new Error('Credential input ended early'))
    if (hidden) {
      process.stdin.setRawMode(true)
      console.log('Ready for Sites credential JSON on stdin (input is hidden).')
    }
    process.stdin.setEncoding('utf8')
    process.stdin.on('data', onData)
    process.stdin.once('end', onEnd)
    process.stdin.resume()
  })
}

readCredential().then(main).catch(error => { console.error(error.message); process.exitCode = 1 })
