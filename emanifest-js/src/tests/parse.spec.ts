import fs from 'fs/promises';
import { describe, it, expect } from 'vitest';

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
  it('instantiates an object', () => {
    expect(true).toBe('boolean');
  });
});
