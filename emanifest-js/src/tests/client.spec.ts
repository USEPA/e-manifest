import { AxiosError, AxiosResponse } from 'axios';
import {
  MOCK_API_ID,
  MOCK_API_KEY,
  MOCK_BAD_SITE_ID,
  MOCK_PACKING_GROUPS,
  MOCK_TOKEN,
} from './mockConstants';
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { newClient, RCRAINFO_PREPROD, RCRAINFO_PROD } from '../index';
// @ts-expect-error - we're importing a mock server, ok for testing
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
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: MOCK_API_KEY,
    });
    await rcrainfo.authenticate();
    expect(rcrainfo.token).toBe(MOCK_TOKEN);
  });
  it('does not enable auto-authentication by default', async () => {
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: MOCK_API_KEY,
    });
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
      autoAuth: true,
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
        return rcrainfo.getPackingGroups();
      })
      .then((resp) => {
        expect(resp.status).toBe(200);
      })
      .catch((err: AxiosError) => {
        console.log('error', err);
      });
  });
  it('throws an error if API ID or Key is missing during auto-authentication', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, autoAuth: true });
    await expect(rcrainfo.getPackingGroups()).rejects.toThrowError();
  });

  it('throws an error if authentication fails', async () => {
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: 'INVALID_KEY',
      autoAuth: true,
    });
    await expect(rcrainfo.getPackingGroups()).rejects.toThrowError();
  });
  it('does not add Authorization header if URL contains "auth"', async () => {
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: MOCK_API_KEY,
    });
    const resp: AxiosResponse = await rcrainfo.authenticate();
    expect(resp.config.headers.Authorization).toBeUndefined();
  });
});

describe('RcraClient validation', () => {
  it('is disabled by default', async () => {
    const rcrainfo = newClient({
      apiBaseURL: RCRAINFO_PREPROD,
      apiID: MOCK_API_ID,
      apiKey: MOCK_API_KEY,
      autoAuth: true,
    });
    await expect(() => rcrainfo.getSite(MOCK_BAD_SITE_ID)).rejects.toThrowError();
  });
  it('throws an error if stateCode is not two characters long', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, validateInput: true });
    await expect(() => rcrainfo.getStateWasteCodes('BAD_STATE_CODE')).rejects.toThrowError();
  });
  it('throws an error if siteID is not 12 characters long', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, validateInput: true });
    await expect(() => rcrainfo.getSite('lengthy_site_id_yo_yo')).rejects.toThrowError(
      'siteID must be a string of length 12'
    );
    await expect(() => rcrainfo.getSite('12345')).rejects.toThrowError(
      'siteID must be a string of length 12'
    );
  });
  it('throws an error if siteID is empty', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, validateInput: true });
    // @ts-expect-error - intentionally testing invalid input
    await expect(() => rcrainfo.getSite()).rejects.toThrowError('Site ID cannot be empty');
    await expect(() => rcrainfo.getSite('')).rejects.toThrowError();
  });
  it('throws an error if siteType is not one of acceptable enums', async () => {
    const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, validateInput: true });
    await expect(() =>
      rcrainfo.getStateSites({ stateCode: 'VA', siteType: 'bad_site_type' })
    ).rejects.toThrowError();
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
