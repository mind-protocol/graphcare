/**
 * useDocsView - React hook for WebSocket-based docs views
 *
 * Connects to L3 Docs Service via WebSocket, requests views, handles live updates.
 */

import { useEffect, useState, useRef } from 'react'

interface ViewData {
  org: string
  view_id: string
  title: string
  data: any[]
  generated_at: string
  row_count: number
}

interface UseDocsViewResult {
  data: ViewData | null
  loading: boolean
  error: string | null
  refresh: () => void
}

export function useDocsView(org: string, viewId: string = 'index'): UseDocsViewResult {
  const [data, setData] = useState<ViewData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const ws = useRef<WebSocket | null>(null)
  const requestId = useRef(0)

  const refresh = () => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      setError('WebSocket not connected')
      return
    }

    const reqId = `req_${Date.now()}_${++requestId.current}`

    ws.current.send(JSON.stringify({
      type: 'docs.view.request',
      org,
      view_id: viewId,
      request_id: reqId
    }))

    setLoading(true)
  }

  useEffect(() => {
    // Connect to L3 Docs Service
    const wsUrl = process.env.NEXT_PUBLIC_L3_DOCS_WS || 'ws://localhost:8003'
    ws.current = new WebSocket(wsUrl)

    ws.current.onopen = () => {
      console.log('✅ Connected to L3 Docs Service')

      // Subscribe to org updates
      ws.current?.send(JSON.stringify({
        type: 'docs.subscribe',
        org
      }))

      // Request initial view data
      refresh()
    }

    ws.current.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)

        switch (msg.type) {
          case 'docs.view.data':
            setData(msg)
            setLoading(false)
            setError(null)
            console.log(`✅ Received view data: ${msg.view_id} (${msg.row_count} rows)`)
            break

          case 'docs.cache.invalidated':
            console.log(`🔄 Cache invalidated for ${msg.org}, refreshing...`)
            // Auto-refresh on cache invalidation
            setTimeout(refresh, 500)
            break

          case 'docs.subscribed':
            console.log(`✅ Subscribed to ${msg.org} docs`)
            break

          case 'error':
            setError(msg.message)
            setLoading(false)
            console.error('❌ Error:', msg.message)
            break

          default:
            console.log('Unknown message type:', msg.type)
        }
      } catch (err) {
        console.error('Failed to parse message:', err)
      }
    }

    ws.current.onerror = (err) => {
      console.error('WebSocket error:', err)
      setError('WebSocket connection error')
      setLoading(false)
    }

    ws.current.onclose = () => {
      console.log('WebSocket disconnected')
    }

    // Cleanup
    return () => {
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [org, viewId])

  return { data, loading, error, refresh }
}
