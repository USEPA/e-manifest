import { rest } from 'msw';
import { MOCK_API_ID, MOCK_API_KEY, MOCK_BAD_SITE_ID, MOCK_PACKING_GROUPS, MOCK_TOKEN } from '../mockConstants';
import { RCRAINFO_PREPROD } from '../../client';

export const handlers = [
  rest.get(`${RCRAINFO_PREPROD}/v1/auth/${MOCK_API_ID}/${MOCK_API_KEY}`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        token: `${MOCK_TOKEN}`,
        expiration: '2021-01-01T00:00:00.000Z',
      }),
    );
  }),
  rest.get(`${RCRAINFO_PREPROD}/v1/emanifest/lookup/packing-groups`, (req, res, ctx) => {
    if (req.headers.get('Authorization') === `Bearer ${MOCK_TOKEN}`) {
      return res(ctx.status(200), ctx.json(MOCK_PACKING_GROUPS));
    }
    return res(ctx.status(401));
  }),
  // Request for a bad site ID (likely a better way to parameterize this)
  rest.get(`${RCRAINFO_PREPROD}/v1/site-details/${MOCK_BAD_SITE_ID}`, (req, res, ctx) => {
    if (req.headers.get('Authorization') === `Bearer ${MOCK_TOKEN}`) {
      return res(
        ctx.status(400),
        ctx.json({
          code: 'E_SiteIdNotFound',
          message: 'Site with Provided Site id is Not Found',
          errorId: '41cb95ed-f477-41aa-83af-fc4a28efbfa5',
          errorDate: '2023-08-11T18:10:45.979+00:00',
        }),
      );
    }
    return res(ctx.status(401));
  }),
];
