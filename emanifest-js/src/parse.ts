/**
 * This file contains the code to parse a multipart response as defined in RFC 1341
 * https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
 *
 * This source was adapted from the parse-multipart npm package. It was modified to
 * work asynchronously, use ES modules, export Types. Also, just can inline this dependency, as the health of
 * the parse-multipart package is questionable.
 * https://github.com/freesoftwarefactory/parse-multipart
 */

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

enum ParsingState {
  INIT,
  READING_HEADERS,
  READING_INFO,
  READING_DATA,
  READING_PART_SEPARATOR,
  OTHER,
  OTHER_2,
}

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
 * @param multipartBodyBuffer
 * @param headerBoundary
 */
export async function parse(multipartBodyBuffer: Buffer, headerBoundary: string): Promise<any[]> {
  const boundary = checkBoundary(headerBoundary);
  // Set initial state before looping through the multipartBodyBuffer
  let lastLine = ''; // The last line read
  let header = '';
  let info = ''; // info about the part (e.g., content-disposition) that's included BEFORE the actual part's data
  let state = ParsingState.INIT;
  let buffer = [];
  const allParts = [];

  for (let i = 0; i < multipartBodyBuffer.length; i++) {
    const oneByte = multipartBodyBuffer[i];
    const prevByte = i > 0 ? multipartBodyBuffer[i - 1] : null;
    const newLineDetected = oneByte == 0x0a && prevByte == 0x0d;
    const newLineChar = oneByte == 0x0a || oneByte == 0x0d;

    // loop through the response body, one byte at a time, and append to the current line buffer
    // Every time we find a newline, depending on the current state, decide where that line belongs
    if (!newLineChar) lastLine += String.fromCharCode(oneByte);

    // If starting to read, the first newline should be after the first boundary
    if (state == ParsingState.INIT && newLineDetected) {
      if (boundary == lastLine) {
        // the boundary should be followed by the Content-Type header
        state = ParsingState.READING_HEADERS;
      } else {
        throw new Error('The first line did not match the provided boundary');
      }
      lastLine = '';
      // Set the Content-Type header when we encounter the newline after the boundary
    } else if (state == ParsingState.READING_HEADERS && newLineDetected) {
      header = lastLine;
      state = ParsingState.READING_INFO;
      lastLine = '';
      // After the Content-Type header, an additional header (we call info) may be present before the actual data
      // includes things like Content-Disposition, filename, etc.
    } else if (state == ParsingState.READING_INFO && newLineDetected) {
      info = lastLine;
      // if the info header is empty, we're done reading the headers. Start reading data
      if (info == '') {
        state = ParsingState.READING_DATA;
        lastLine = '';
      } else {
        // if the info header is not empty, we expect a newline after it
        state = ParsingState.READING_PART_SEPARATOR;
        lastLine = '';
      }
    } else if (state == ParsingState.READING_PART_SEPARATOR && newLineDetected) {
      // This is the newline after the info header. We're done reading headers. Start reading data
      state = ParsingState.READING_DATA;
      buffer = [];
      lastLine = '';
    } else if (state == ParsingState.READING_DATA) {
      if (lastLine.length > boundary.length + 4) lastLine = ''; // mem save
      if (boundary == lastLine) {
        const j = buffer.length - lastLine.length;
        const data = buffer.slice(0, j - 1);
        const p: Part = { contentTypeHeader: header, contentDispositionHeader: info, data: data };
        allParts.push(process(p));
        buffer = [];
        lastLine = '';
        state = ParsingState.OTHER_2;
        header = '';
        info = '';
      } else {
        buffer.push(oneByte);
      }
      if (newLineDetected) lastLine = '';
    } else if (state == ParsingState.OTHER_2) {
      if (newLineDetected) state = ParsingState.READING_HEADERS;
    }
  }
  return allParts;
}

/**
 * Process the part of a multipart response
 * transforms raw part, with header and metadata, into a more useful and JavaScript idiomatic object
 *
 * { header: 'Content-Disposition: form-data; name="uploads[]"; filename="A.txt"',
 * info: 'Content-Type: text/plain',
 * data: 'AAAABBBB' }
 *
 * into this one:
 *
 * { filename: 'A.txt', type: 'text/plain', data: <Buffer 41 41 41 41 42 42 42 42> }
 * @param part
 */
async function process(part: Part): Promise<Input> {
  // will transform this object:
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
    : ['Content-Disposition: form-data', 'filename="manifest.zip"', 'name="attachments.zip"'];

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
