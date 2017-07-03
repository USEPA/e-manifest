package gov.epa.rcra.web.rest.api.client.cli.commands;

import java.util.Properties;

import org.apache.commons.lang3.StringUtils;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

import gov.epa.rcra.web.rest.api.client.auth.AuthInfoLoader;
import gov.epa.rcra.web.rest.api.client.site.SiteServiceClient;

@Parameters(commandDescription="Call Site Service",commandNames="site")
public class SiteCommand extends BaseCommand{
	
	@Parameter(names = { "--operation"}, description = "Specific Site Operation, possible values: site-details", required=true)	
	protected String operation;
	
	@Parameter(names = { "--site-id"}, description = "Site Id",required=true)		
	protected String siteId;

	public String getSiteId() {
		return siteId;
	}

	public void setSiteId(String siteId) {
		this.siteId = siteId;
	}

	public void run() {
		if (StringUtils.isNotBlank(operation)) {
			Properties props = AuthInfoLoader.load();					
			SiteServiceClient  serviceClient = new SiteServiceClient(props.getProperty("baseUrl"), props.getProperty("token"));
			if ("site-details".equals(operation)) {
				if (StringUtils.isNotBlank(siteId)) {
					serviceClient.execute(operation+"/"+siteId);
				}else {
					throw new IllegalArgumentException("Site Id is required");
				}						
			} else {
				throw new IllegalArgumentException("Applicable operation is required");
			}
		} else {
			throw new IllegalArgumentException("Operation is required");
		}
	}	
		
}
