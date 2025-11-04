/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: '/scopelock/docs',
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
