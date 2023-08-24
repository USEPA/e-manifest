import fs from 'fs/promises';
import { extractBoundary, parse } from '../parse';
import { describe, it, expect } from 'vitest';

const fileBoundary = 'Boundary_10_712184523_1692837126159';
const mockContentType = `multipart/mixed;boundary=${fileBoundary}`;

// @ts-ignore
async function readMultipartBodyForTesting() {
  try {
    const filename = `${__dirname}/100035569ELC-multipart-mixed.bin`;
    return await fs.readFile(filename);
  } catch (error) {
    console.error('Error preparing contents for testing:', error);
  }
}

describe('Parse module', () => {
  it('extracts the boundary', () => {
    const boundary = extractBoundary(mockContentType);
    expect(boundary).toBe(fileBoundary);
  });
  it('splits the body into two parts', async () => {
    const body = await readMultipartBodyForTesting();
    const boundary = extractBoundary(mockContentType);
    if (body && boundary) {
      const parts = parse(body, boundary);
      parts
        .then((parts) => parts[0])
        .then((part) => {
          // fs.writeFile('test.pdf', part.data);
          console.log('output: ', part);
        });
    }
  });
});
