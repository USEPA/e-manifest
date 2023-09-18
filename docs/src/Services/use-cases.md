# Use Cases and Scenarios

Sometimes it's helpful to see how the RCRAInfo services can be used in conjunction to solve a complete a task. For
Example, syncing a site's manifest with RCRAInfo can be accomplished using a combination of
the [Manifest Search Service](./Manifest/search.md) and the [Manifest Retrieve (GET) Service](./Manifest/get.md).

## Syncing a Site's Manifest

RCRAInfo currently does not offer web hooks or another mechanism for push notifications through the web services.
However, it is possible to sync a site's manifest by periodically polling the RCRAInfo web services. The following is a
high-level overview of how this can be accomplished:

1. Use the [Manifest Search Service](./Manifest/search.md) to retrieve a list of manifest tracking numbers for a site.
   The Manifest Search service allows you to filter manifests by site ID, a date range, and date type. It returns an
   array of manifest tracking numbers (MTN).
   - Pass the `dateType` parameter with a value of `UpdatedDate`
   - Pass the site's ID as the `siteId` parameter
   - If this is the first time the site is syncing with RCRAInfo, you can retrieve all manifests for the site by
     setting the `startDate` to three years prior to the current date. Otherwise, you can set the `startDate` to the
     date of the last sync.
   - Set the `endDate` to the current date.
2. For each MTN returned by the Manifest Search Service, use the [Manifest Retrieve (GET) Service](./Manifest/get.md) to
   retrieve the manifest data, and save to the local database.
3. Upon successfully completion, update the site's last sync date to the current date.

Note, the RCRAInfo web services are rate limited. You should not make more than 30 requests per minute. If you need to
sync more than 30 manifests, you should break the sync into batches, and wait at least one minute between batches.
