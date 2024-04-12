package gov.epa.rcra.rest.site;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/site")
public class SiteController {

    private final SiteService siteService;

    SiteController(SiteService siteService) {
        this.siteService = siteService;
    }

    @GetMapping(value = "/{siteId}", produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public String getSite(@PathVariable String siteId) {
        return siteService.getSite(siteId);
    }

    @PostMapping(value = "/search")
    @ResponseBody
    public String searchSite(@RequestBody SiteSearchRequest siteSearchRequest) {
        System.out.println("searching for site: " + siteSearchRequest);
        return siteService.findSites(siteSearchRequest);
    }

    @GetMapping("/{siteId}/exists")
    public SiteExistsResult getSiteExists(@PathVariable String siteId) {
        return siteService.siteExists(siteId);
    }

}
