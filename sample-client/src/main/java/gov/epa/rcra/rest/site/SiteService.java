package gov.epa.rcra.rest.site;

import org.springframework.stereotype.Service;

@Service
class SiteService {

    private final SiteClient client;

    SiteService(SiteClient siteClient) {
        client = siteClient;
    }

    public String getSite(String siteId) {
        return client.getEpaSite(siteId);
    }

    public SiteExistsResult siteExists(String siteId) {
        return client.getSiteExists(siteId);
    }

    public String findSites(SiteSearchRequest siteSearchRequest) {
        return client.findSites(siteSearchRequest);
    }
}
