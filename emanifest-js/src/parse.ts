type Part = {
  contentDispositionHeader: string;
  contentTypeHeader: string;
  data: number[];
};

type Input = {
  filename?: string;
  name?: string;
  type: string;
  data: Buffer;
};

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

function checkBoundary(headerBoundary: string): string {
  if (!headerBoundary) {
    throw new Error('headerBoundary is undefined');
  }
  if (headerBoundary.startsWith('--')) {
    return headerBoundary;
  }
  return '--' + headerBoundary;
}

/**
 * Parse a multipart response
 * This source was adapted from the parse-multipart npm package. It was modified to
 * work asynchronously, use ES modules. Also, just so we can inline this dependency, as the health of
 * the parse-multipart package is questionable.
 * https://github.com/freesoftwarefactory/parse-multipart
 * @param multipartBodyBuffer
 * @param headerBoundary
 */
export async function parse(multipartBodyBuffer: Buffer, headerBoundary: string): Promise<any[]> {
  const boundary = checkBoundary(headerBoundary);
  let lastLine = '';
  let header = '';
  let info = '';
  let state = 0;
  let buffer = [];
  const allParts = [];

  for (let i = 0; i < multipartBodyBuffer.length; i++) {
    const oneByte = multipartBodyBuffer[i];
    const prevByte = i > 0 ? multipartBodyBuffer[i - 1] : null;
    const newLineDetected = oneByte == 0x0a && prevByte == 0x0d;
    const newLineChar = oneByte == 0x0a || oneByte == 0x0d;

    if (!newLineChar) lastLine += String.fromCharCode(oneByte);

    if (0 == state && newLineDetected) {
      if (boundary == lastLine) {
        state = 1;
      }
      lastLine = '';
    } else if (1 == state && newLineDetected) {
      header = lastLine;
      state = 2;
      lastLine = '';
    } else if (2 == state && newLineDetected) {
      info = lastLine;
      state = 3;
      lastLine = '';
    } else if (3 == state && newLineDetected) {
      state = 4;
      buffer = [];
      lastLine = '';
    } else if (4 == state) {
      if (lastLine.length > boundary.length + 4) lastLine = ''; // mem save
      if (boundary == lastLine) {
        const j = buffer.length - lastLine.length;
        const data = buffer.slice(0, j - 1);
        const p: Part = { contentTypeHeader: header, contentDispositionHeader: info, data: data };
        // allParts.push(p);
        allParts.push(process(p));
        buffer = [];
        lastLine = '';
        state = 5;
        header = '';
        info = '';
      } else {
        buffer.push(oneByte);
      }
      if (newLineDetected) lastLine = '';
    } else if (5 == state) {
      if (newLineDetected) state = 1;
    }
  }
  return allParts;
}

async function process(part: Part): Promise<Input> {
  // will transform this object:
  // { header: 'Content-Disposition: form-data; name="uploads[]"; filename="A.txt"',
  // info: 'Content-Type: text/plain',
  // part: 'AAAABBBB' }
  // into this one:
  // { filename: 'A.txt', type: 'text/plain', data: <Buffer 41 41 41 41 42 42 42 42> }
  const obj = (str: string) => {
    const k = str.split('=');
    const a = k[0].trim();

    const b = JSON.parse(k[1].trim());
    const o = {};
    Object.defineProperty(o, a, {
      value: b,
      writable: true,
      enumerable: true,
      configurable: true,
    });
    return o;
  };
  // If the part only contains the 'Content-Type' header, set some defaults
  const info = part.contentDispositionHeader
    ? part.contentDispositionHeader.split(';')
    : [
        'Content-Disposition: form-data',
        ' filename="fd983141-4f82-4f0b-8290-f4e5db60b4589127020486266855753.tmp"',
        ' modification-date="Thu, 24 Aug 2023 00:32:06 GMT"',
        ' size=1029434',
        ' name="attachments.zip"',
      ];

  const filenameData = info[2];
  let input = {};
  if (filenameData) {
    input = obj(filenameData);
    const contentType = part.contentTypeHeader.split(':')[1].trim();
    Object.defineProperty(input, 'type', {
      value: contentType,
      writable: true,
      enumerable: true,
      configurable: true,
    });
  }
  // always process the name field
  Object.defineProperty(input, 'name', {
    value: info[1].split('=')[1].replace(/"/g, ''),
    writable: true,
    enumerable: true,
    configurable: true,
  });

  Object.defineProperty(input, 'data', {
    value: Buffer.from(part.data),
    writable: true,
    enumerable: true,
    configurable: true,
  });
  return input as Input;
}
