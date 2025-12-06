import { NextRequest } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const response = await fetch(`http://127.0.0.1:8000/download/${params.id}`)
  return new Response(response.body, {
    headers: response.headers,
  })
}
