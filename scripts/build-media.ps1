# Gera as mídias otimizadas da landing page a partir dos arquivos brutos em assets/.
# Uso (na raiz do projeto):  powershell -ExecutionPolicy Bypass -File scripts/build-media.ps1
#
# Vídeo do hero:
#   - trecho 2s -> 9s do bruto (Cubos_caindo.mp4)
#   - crop de 72px no topo (remove a marca d'água do gerador)
#   - loop sem emenda: os últimos 0,5s dissolvem no início do trecho (2,0s -> 2,5s),
#     então o arquivo começa em 2,5s e termina exatamente onde começa -> 6,5s, tudo dentro de 2-9s
#   - sem áudio, faststart, GOP curto para o loop reiniciar limpo
#   - desktop 1256x648 (paisagem) e mobile 364x648 (retrato, recorte central)
#   - AV1 (principal) + H.264 (fallback universal)

$ErrorActionPreference = 'Stop'
$root   = Split-Path -Parent $PSScriptRoot
$src    = Join-Path $root 'assets\videos\Cubos_caindo.mp4'
$vidOut = Join-Path $root 'assets\videos'
$imgOut = Join-Path $root 'assets\images'

$START      = 2.0   # início pedido
$END        = 9.0   # fim pedido
$FADE       = 0.5   # duração do dissolve de loop
$CROP_TOP   = 72    # altura removida no topo (marca d'água)
$W          = 1256
$H          = 720 - $CROP_TOP                 # 648
$MOBILE_W   = 364                              # ~9:16 sobre 648 de altura
$MOBILE_X   = [int](($W - $MOBILE_W) / 2)

$mainStart = $START + $FADE                    # 2.5
$offset    = ($END - $mainStart) - $FADE        # 6.0

function Invoke-FF([string[]]$ffArgs) {
  & ffmpeg -hide_banner -v error -y @ffArgs
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg falhou: $($ffArgs -join ' ')" }
}

$loopGraph = "[0:v]crop=${W}:${H}:0:${CROP_TOP},split=2[a][b];" +
             "[a]trim=start=${mainStart}:end=${END},setpts=PTS-STARTPTS[main];" +
             "[b]trim=start=${START}:end=${mainStart},setpts=PTS-STARTPTS[head];" +
             "[main][head]xfade=transition=fade:duration=${FADE}:offset=${offset},format=yuv420p"

$variants = @(
  @{ name = 'desktop'; graph = "$loopGraph[v]" },
  @{ name = 'mobile';  graph = "$loopGraph,crop=${MOBILE_W}:${H}:${MOBILE_X}:0[v]" }
)

foreach ($v in $variants) {
  $n = $v.name
  Write-Host "-> hero-$n (AV1)"
  Invoke-FF @('-i', $src, '-filter_complex', $v.graph, '-map', '[v]', '-an',
    '-c:v', 'libsvtav1', '-preset', '4', '-crf', '44', '-g', '60', '-svtav1-params', 'tune=0',
    '-movflags', '+faststart', (Join-Path $vidOut "hero-$n.av1.mp4"))

  Write-Host "-> hero-$n (H.264)"
  Invoke-FF @('-i', $src, '-filter_complex', $v.graph, '-map', '[v]', '-an',
    '-c:v', 'libx264', '-preset', 'veryslow', '-crf', '29', '-profile:v', 'high', '-g', '60',
    '-movflags', '+faststart', (Join-Path $vidOut "hero-$n.h264.mp4"))
}

# Poster = primeiro quadro do loop (2,5s do bruto), mesmo recorte do vídeo.
$posterDesk = "crop=${W}:${H}:0:${CROP_TOP}"
$posterMob  = "crop=${W}:${H}:0:${CROP_TOP},crop=${MOBILE_W}:${H}:${MOBILE_X}:0"
foreach ($p in @(@{ name = 'desktop'; vf = $posterDesk }, @{ name = 'mobile'; vf = $posterMob })) {
  $n = $p.name
  Write-Host "-> poster-$n (AVIF + WebP)"
  Invoke-FF @('-ss', "$mainStart", '-i', $src, '-vf', $p.vf, '-frames:v', '1',
    '-c:v', 'libaom-av1', '-still-picture', '1', '-crf', '40', '-cpu-used', '4', '-pix_fmt', 'yuv420p',
    (Join-Path $imgOut "poster-$n.avif"))
  Invoke-FF @('-ss', "$mainStart", '-i', $src, '-vf', $p.vf, '-frames:v', '1',
    '-c:v', 'libwebp', '-quality', '55', '-compression_level', '6',
    (Join-Path $imgOut "poster-$n.webp"))
}

# Logo do menu/rodapé em 2x da altura exibida (36px -> 72px).
Write-Host '-> logo-nav.webp'
Invoke-FF @('-i', (Join-Path $imgOut 'logo.webp'), '-vf', 'scale=-2:72:flags=lanczos',
  '-c:v', 'libwebp', '-quality', '90', '-compression_level', '6', (Join-Path $imgOut 'logo-nav.webp'))

Get-ChildItem $vidOut, $imgOut | Where-Object { $_.Name -ne 'Cubos_caindo.mp4' } |
  Select-Object Name, @{ n = 'KB'; e = { [math]::Round($_.Length / 1KB, 1) } } | Format-Table -AutoSize
