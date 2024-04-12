package gov.epa.rcra.rest.site;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record SiteSearchRequest(String epaSiteId, String name, String streetNumber, String address1, String city,
                                String state, String zip, String siteType) {
}
