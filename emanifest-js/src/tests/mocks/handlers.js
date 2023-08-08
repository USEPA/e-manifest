import { rest } from 'msw';
import { MOCK_API_ID, MOCK_API_KEY, MOCK_PACKING_GROUPS, MOCK_TOKEN } from '../mockConstants';
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
];
