/**
 * Extract the boundary that separates the parts of a multipart response
 * @param contentType string
 */
export function extractBoundary(contentType: string): string | null {
  const boundaryMatch = contentType.match(/boundary=([^;]+)/);
  if (boundaryMatch) {
    return boundaryMatch[1];
  }
  return null;
}
