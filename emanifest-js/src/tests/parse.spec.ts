import fs from 'fs/promises';
import { extractBoundary } from '../parse';
import { describe, it, expect } from 'vitest';

const mockContentType = 'multipart/mixed;boundary=Boundary_12_141861297_1692842024406';

// @ts-ignore
async function prepareContentsForTesting() {
  try {
    const filename = '100035569ELC-multipart-mixed.bin';
    return await fs.readFile(filename);
  } catch (error) {
    console.error('Error preparing contents for testing:', error);
  }
}

describe('Parsing multipart/mixed', () => {
  it('extracts the boundary', () => {
    const boundary = extractBoundary(mockContentType);
    expect(boundary).toBe('Boundary_12_141861297_1692842024406');
  });
});
