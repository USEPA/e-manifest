package gov.epa.rcra.rest.site;

public record SiteSearchResult(int totalNumberOfSites, int totalNumberOfPages, int currentPAge,
                               SiteSearchRequest searchedParameters) {
}
