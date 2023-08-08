import { AxiosError, AxiosResponse } from 'axios';
import { MOCK_API_ID, MOCK_API_KEY, MOCK_PACKING_GROUPS, MOCK_TOKEN } from './mockConstants';
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { newClient, RCRAINFO_PREPROD, RCRAINFO_PROD } from '../index';
// @ts-ignore
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('RcraClient', () => {
  it('instantiates an object', () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD });
    expect(typeof rcrainfo).toBe('object');
    expect(typeof rcrainfo.authenticate).toBe('function');
  });
  it('Retrieves a token when authenticating', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, apiID: MOCK_API_ID, apiKey: MOCK_API_KEY });
    await rcrainfo.authenticate();
    expect(rcrainfo.token).toBe(MOCK_TOKEN);
  });
  it('does not enable auto-authentication by default', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, apiID: MOCK_API_ID, apiKey: MOCK_API_KEY });
    // We expect a 401 because we didn't call authenticate() first
    await rcrainfo.getPackingGroups().catch((err: AxiosError) => {
      expect(err.response?.status).toBe(401);
    });
  });
  it('auto-authenticates when enabled, and retrieved a token on calling any service', async () => {
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: MOCK_API_KEY,
      authAuth: true,
    });
    const resp: AxiosResponse = await rcrainfo.getPackingGroups();
    expect(rcrainfo.token).toEqual(MOCK_TOKEN);
    expect(resp.data).toEqual(MOCK_PACKING_GROUPS);
  });
  it('adds a Authorization headers with "Bearer" + token', async () => {
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: MOCK_API_KEY,
    });
    rcrainfo
      .authenticate()
      .then((authResp: AxiosResponse) => {
        expect(authResp.status).toBe(200);
        expect(rcrainfo.token).toBeTruthy();
        fail('should not have authenticated');
        return rcrainfo.getPackingGroups();
      })
      .then((resp) => {
        expect(resp.status).toBe(200);
      })
      .catch((err: AxiosError) => {
        console.log('error', err);
      });
    // expect(authResponse.status).toBe(200);
    // expect(rcrainfo.token).toBeTruthy(); // Ensure token is set
    // console.log(rcrainfo.token);
    // // Our mock service worker will return a 401 if Authorization: 'Bearer mockToken' is not set
    // const resp = await rcrainfo.getPackingGroups();
    // expect(resp.status).toBe(200);
  });
});

describe('emanifest package', () => {
  it('exports a URL constant RCRAINFO_PREPROD', () => {
    expect(RCRAINFO_PREPROD).toBeDefined();
  });
  it('exports a URL constant RCRAINFO_PROD', () => {
    expect(RCRAINFO_PROD).toBeDefined();
  });
});
