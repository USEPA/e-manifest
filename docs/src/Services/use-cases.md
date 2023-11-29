# Use Cases and Scenarios

Sometimes it's helpful to see how the RCRAInfo services can be used in conjunction to solve a complete a task. For
Example, syncing a site's manifest with RCRAInfo can be accomplished using a combination of
the [Manifest Search Service](./Manifest/search.md) and the [Manifest Retrieve (GET) Service](./Manifest/get.md).

Note, the RCRAInfo web services are rate limited. You should not make more than 30 requests per minute. If you need to
sync more than 30 manifests, you should break the sync into batches, and wait at least one minute between batches.

## Syncing a Site's Manifest

RCRAInfo currently does not offer web hooks or another mechanism for push notifications through the web services.
However, it is possible to sync a site's manifest by periodically polling the RCRAInfo web services. The following is a
high-level overview of how this can be accomplished:

1. Authenticate and obtain a token for use with all future session requests via
   the [authenticate service](./authentication.md).
2. Use the [Manifest Search Service](./Manifest/search.md) to retrieve a list of manifest tracking numbers for a site.
   The Manifest Search service allows you to filter manifests by site ID, a date range, and date type. It returns an
   array of manifest tracking numbers (MTN).
   - Pass the `dateType` parameter with a value of `UpdatedDate`
   - Pass the site's ID as the `siteId` parameter
   - If this is the first time the site is syncing with RCRAInfo, you can retrieve all manifests for the site by
     setting the `startDate` to three years prior to the current date. Otherwise, you can set the `startDate` to the
     date of the last sync.
   - Set the `endDate` to the current date.
3. For each MTN returned by the Manifest Search Service, use the [Manifest Retrieve (GET) Service](./Manifest/get.md) to
   retrieve the manifest data, and save to the local database.
4. Upon successfully completion, update the site's last sync date to the current date.
5. Repeat the process at a future time, next time setting the `startDate` to the date of the last sync.

## Obtaining Manifest via manifest-tracking- numbers service

1. Requester performs auth service to obtain Security Token. See details in section auth.
2. If Authentication process was successful the service returns Security Token. This Security Token shall be stored for
   the duration of the session. It will be passed to all the services.
3. Requester performs manifest-tracking-numbers service to obtain the list of Manifest Tracking Numbers for Manifests
   stored in the system. See details in section Error! Reference source not found.
4. If there are Manifests for the provided Site ID the manifest-tracking-numbers service returns the list of Manifest
   Tracking Numbers.

## Obtaining Site Ids via site-ids service

1. Requester performs auth services to obtain Security Token. See details in section auth.
2. If Authentication process was successful the service returns Security Token. This Security Token shall be stored for
   the duration of the session. It will be passed to all the services.
3. Requester performs site-ids service to obtain the list either of all Transporter IDs or all TSDF Ids or all Generator
   Ids for the provided State Code and Site Type. See details in section site-ids.
4. site-ids service returns list of either all Transporter IDs or all TSDF Ids or all Generator Ids for the state.

## Obtaining Site Details via site-details service

1. Requester performs auth services to obtain Security Token. See details in section auth.
2. If Authentication process was successful the service returns Security Token. This Security Token shall be stored for
   the duration of the session. It will be passed to all the services.
3. Requester performs site-details service to obtain Site Details by Site Id. See details in section site-details
4. site-details service returns Site Details.
