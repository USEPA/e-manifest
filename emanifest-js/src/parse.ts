/**
 * This file contains the code to parse a multipart response as defined in RFC 2046
 * https://datatracker.ietf.org/doc/html/rfc2046
 *
 * This source was adapted from the parse-multipart npm package. It was modified to
 * work asynchronously, use ES modules, export Types. Also, just can inline this dependency, as the health of
 * the parse-multipart package is questionable.
 * https://github.com/freesoftwarefactory/parse-multipart
 */

/**
 * Initially parsed data from the multipart response that has not been processed into a more useful object
 */
interface InputPart {
  contentDispositionHeader: string;
  contentTypeHeader: string;
  data: number[];
}

/**
 * The output of parsing the multipart/mixed response
 */
export interface OutputPart {
  contentType: 'application/json' | 'application/octet-stream';
  contentDisposition?: string;
  data: Buffer | string;
}

/**
 * The state of the parser
 */
enum ParsingState {
  INIT,
  READING_HEADERS,
  READING_INFO,
  READING_DATA,
  READING_PART_SEPARATOR,
  POST_READING_DATA,
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

/**
 * check the boundary and fix if possible.
 * e-Manifest attachments are returned following RFC 1341
 * --Boundary_10_12345
 * foo bar
 * --Boundary_10_12345
 * bar foo
 * --Boundary_10_12345--
 * @param headerBoundary
 */
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
export async function parseAttachments(
  multipartBodyBuffer: Buffer,
  headerBoundary: string
): Promise<OutputPart[]> {
  const boundary = checkBoundary(headerBoundary);
  // Set initial state before looping through the multipartBodyBuffer
  let lastLine = ''; // The current line buffer
  let header = '';
  let info = ''; // info about the part (e.g., content-disposition) that's included BEFORE the actual part's data
  let state = ParsingState.INIT;
  let buffer = [];
  const allParts = [];

  // loop through the response body, one byte at a time
  for (let i = 0; i < multipartBodyBuffer.length; i++) {
    const oneByte = multipartBodyBuffer[i];
    const prevByte = i > 0 ? multipartBodyBuffer[i - 1] : null;
    const newLineDetected = oneByte == 0x0a && prevByte == 0x0d;
    const newLineChar = oneByte == 0x0a || oneByte == 0x0d;

    // append the byte to the lastLine buffer unless it is a new line character
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
      // If reading the data, and we find the line length is the boundary + 2 ('--' at the end)
      // we assume we've reached the end of the part (--Boundary_12345--)
      if (lastLine.length > boundary.length + 2) lastLine = '';
      if (lastLine == boundary) {
        const j = buffer.length - lastLine.length;
        const data = buffer.slice(0, j - 1);
        allParts.push(
          process({ contentTypeHeader: header, contentDispositionHeader: info, data: data })
        );
        buffer = [];
        lastLine = '';
        state = ParsingState.POST_READING_DATA;
        header = '';
        info = '';
      } else {
        // If not at the end of the part, append the line to the buffer
        buffer.push(oneByte);
      }
      // If a newline is found, reset the line buffer
      if (newLineDetected) lastLine = '';
      // If we find more data after the boundary, we're reading another part of the multipart response
    } else if (state == ParsingState.POST_READING_DATA) {
      if (newLineDetected) state = ParsingState.READING_HEADERS;
    }
  }
  return allParts;
}

/**
 * Process the part of a multipart response
 * transforms raw part, with header and metadata, into a more useful and JavaScript idiomatic object
 * @param part
 */
function process(part: InputPart): OutputPart {
  const contentType = part.contentTypeHeader.split(':')[1].trim();
  const outputPart: OutputPart = {
    contentType: contentType as 'application/json' | 'application/octet-stream',
    data:
      contentType === 'application/json'
        ? JSON.parse(Buffer.from(part.data).toString())
        : Buffer.from(part.data),
  };
  if (part.contentDispositionHeader) {
    outputPart.contentDisposition = part.contentDispositionHeader.split(':')[1].trim();
  }
  return outputPart;
}
