import { http, HttpResponse } from 'msw';
import { MOCK_API_ID, MOCK_API_KEY, MOCK_BAD_SITE_ID, MOCK_PACKING_GROUPS, MOCK_TOKEN } from '../mockConstants';
import { RCRAINFO_PREPROD } from '../../client';

export const handlers = [
  http.get(`${RCRAINFO_PREPROD}/v1/auth/${MOCK_API_ID}/${MOCK_API_KEY}`, (info) => {
    return HttpResponse.json(
      {
        token: `${MOCK_TOKEN}`,
        expiration: '2021-01-01T00:00:00.000Z',
      },
      { status: 200 },
    );
  }),
  http.get(`${RCRAINFO_PREPROD}/v1/emanifest/lookup/packing-groups`, (info) => {
    if (info.request.headers.get('Authorization') === `Bearer ${MOCK_TOKEN}`) {
      return HttpResponse.json(MOCK_PACKING_GROUPS, { status: 200 });
    }
    return HttpResponse.json({}, { status: 401 });
  }),
  // Request for a bad site ID (likely a better way to parameterize this)
  http.get(`${RCRAINFO_PREPROD}/v1/site-details/${MOCK_BAD_SITE_ID}`, (info) => {
    if (info.request.headers.get('Authorization') === `Bearer ${MOCK_TOKEN}`) {
      return HttpResponse.json(
        {
          code: 'E_SiteIdNotFound',
          message: 'Site with Provided Site id is Not Found',
          errorId: '41cb95ed-f477-41aa-83af-fc4a28efbfa5',
          errorDate: '2023-08-11T18:10:45.979+00:00',
        },
        { status: 400 },
      );
    }
    return HttpResponse.json('', { status: 401 });
  }),
];
