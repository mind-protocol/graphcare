/**
 * Example: Docs Page for mindprotocol.ai
 *
 * Path: mindprotocol.ai/[org]/docs/[[...slug]]
 *
 * Real-time docs rendered from L3 views via WebSocket
 */

'use client'

import { useDocsView } from './useDocsView'
import ReactMarkdown from 'react-markdown'

interface DocsPageProps {
  params: {
    org: string
    slug?: string[]
  }
}

export default function DocsPage({ params }: DocsPageProps) {
  const { org, slug } = params
  const viewId = slug?.[0] || 'index'

  const { data, loading, error, refresh } = useDocsView(org, viewId)

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading {viewId} view...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-red-900 mb-2">Error Loading Docs</h2>
          <p className="text-red-700">{error}</p>
          <button
            onClick={refresh}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <p className="text-gray-600">No data available</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-8">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{data.title}</h1>
          <p className="text-sm text-gray-500">
            {data.org} · {data.row_count} items · Generated {new Date(data.generated_at).toLocaleString()}
          </p>
        </div>
        <button
          onClick={refresh}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center gap-2"
        >
          <RefreshIcon />
          Refresh
        </button>
      </div>

      {/* View-specific rendering */}
      {viewId === 'architecture' && <ArchitectureView data={data.data} />}
      {viewId === 'api-reference' && <APIReferenceView data={data.data} />}
      {viewId === 'coverage' && <CoverageView data={data.data} />}
      {viewId === 'index' && <IndexView data={data.data} />}
    </div>
  )
}

// ============================================================================
// View Components
// ============================================================================

function ArchitectureView({ data }: { data: any[] }) {
  return (
    <div className="space-y-8">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-blue-900 mb-2">Architecture Overview</h2>
        <p className="text-blue-700">Found {data.length} specifications</p>
      </div>

      {data.map((spec, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-2">{spec.spec_name}</h3>
          <p className="text-gray-600 mb-4">{spec.spec_desc}</p>

          <div className="flex items-center gap-4 text-sm">
            <span className="text-gray-500">
              <strong>Implementations:</strong> {spec.impl_count}
            </span>
            <span className="text-gray-500">
              <strong>Path:</strong> <code className="bg-gray-100 px-2 py-1 rounded">{spec.spec_path}</code>
            </span>
          </div>

          {spec.implementations && spec.implementations.length > 0 && (
            <ul className="mt-4 space-y-1">
              {spec.implementations.map((impl: string, j: number) => (
                <li key={j} className="text-sm text-gray-700">
                  → {impl}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  )
}

function APIReferenceView({ data }: { data: any[] }) {
  return (
    <div className="space-y-6">
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-green-900 mb-2">API Endpoints</h2>
        <p className="text-green-700">Found {data.length} endpoints</p>
      </div>

      {data.map((endpoint, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-mono font-bold text-gray-900 mb-2">{endpoint.endpoint}</h3>
          <p className="text-gray-600 mb-2">{endpoint.desc}</p>
          <p className="text-sm text-gray-500">
            <strong>File:</strong> <code className="bg-gray-100 px-2 py-1 rounded">{endpoint.file}</code>
          </p>
          {endpoint.docs && (
            <div className="mt-4 text-sm text-gray-700 prose">
              <ReactMarkdown>{endpoint.docs}</ReactMarkdown>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

function CoverageView({ data }: { data: any[] }) {
  const total = data.reduce((sum, item) => sum + (item.count || 0), 0)

  return (
    <div className="space-y-6">
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-purple-900 mb-2">Coverage Report</h2>
        <p className="text-purple-700">Total nodes: {total}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.map((item, i) => (
          <div key={i} className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="text-3xl font-bold text-gray-900 mb-1">{item.count}</div>
            <div className="text-sm text-gray-600">{item.type}</div>
            <div className="mt-2 text-xs text-gray-500">
              {((item.count / total) * 100).toFixed(1)}% of total
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function IndexView({ data }: { data: any[] }) {
  return (
    <div className="space-y-6">
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Documentation Index</h2>
        <p className="text-gray-600">{data.length} documents available</p>
      </div>

      <div className="grid gap-4">
        {data.map((doc, i) => (
          <a
            key={i}
            href={`#${doc.path}`}
            className="block bg-white border border-gray-200 rounded-lg p-6 hover:border-blue-400 hover:shadow-md transition"
          >
            <h3 className="text-lg font-bold text-gray-900 mb-1">{doc.title}</h3>
            <p className="text-sm text-gray-600 mb-2">{doc.desc}</p>
            <code className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">{doc.path}</code>
          </a>
        ))}
      </div>
    </div>
  )
}

function RefreshIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
    </svg>
  )
}
