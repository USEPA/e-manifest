import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// configures a mocking server with the given request handlers.
export const server = setupServer(...handlers);
