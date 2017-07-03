package gov.epa.rcra.web.rest.api.client.cli.commands;

import java.util.Properties;

import org.apache.commons.lang3.StringUtils;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

import gov.epa.rcra.web.rest.api.client.auth.AuthInfoLoader;
import gov.epa.rcra.web.rest.api.client.manifest.ManifestServiceClient;

@Parameters(commandDescription="Call Manifest Service",commandNames="eman")
public class ManifestCommand extends BaseCommand{
	
	@Parameter(names = { "--operation"}, description = "Specific Manifest Operation, possible values: 'get', "
			+ "'manifest-tracking-numbers', 'site-ids'", required=true)	
	protected String operation;
	
	
	@Parameter(names = { "--tracking-number"}, description = "eManifest Tracking Number (used with 'get' operation)")		
	protected String trackingNumber;

	@Parameter(names = { "--site-id"}, description = "Site Id (used with 'manifest-tracking-numbers' operation)")		
	protected String siteId;
	
	@Parameter(names = { "--site-type"}, description = "Site Type (used with 'site-ids' operation)")			
	protected String siteType;

	@Parameter(names = { "--state-code"}, description = "State Code (used with 'site-ids' operation)")			
	protected String stateCode;
	
	public String getTrackingNumber() {
		return trackingNumber;
	}

	public void setTrackingNumber(String trackingNumber) {
		this.trackingNumber = trackingNumber;
	}

	public String getSiteType() {
		return siteType;
	}

	public void setSiteType(String siteType) {
		this.siteType = siteType;
	}

	public String getOperation() {
		return operation;
	}

	public void setOperation(String operation) {
		this.operation = operation;
	}

	public String getSiteId() {
		return siteId;
	}

	public void setSiteId(String siteId) {
		this.siteId = siteId;
	}

	public String getStateCode() {
		return stateCode;
	}

	public void setStateCode(String stateCode) {
		this.stateCode = stateCode;
	}

	public void run() {
		if (StringUtils.isNotBlank(operation)) {
			Properties props = AuthInfoLoader.load();					
			ManifestServiceClient  maClient = new ManifestServiceClient(props.getProperty("baseUrl"), props.getProperty("token"));
			if ("get".equals(operation)) {
				if (StringUtils.isNotBlank(trackingNumber)) {
					maClient.execute("manifest/"+trackingNumber);
				}else {
					throw new IllegalArgumentException("Manifest tracking number is required");
				}
			}
			else if ("manifest-tracking-numbers".equals(operation)) {
				if (StringUtils.isNotBlank(siteId)) {
					maClient.execute(operation+"/"+siteId);
				}else {
					throw new IllegalArgumentException("Site Id is required");
				}
			}					
			else if ("site-ids".equals(operation)) {
				if (StringUtils.isNotBlank(stateCode) && StringUtils.isNotBlank(siteType)) {
					maClient.execute(operation+"/"+stateCode+"/"+siteType);
				}else {
					throw new IllegalArgumentException("Site Id and Site Type are required");
				}
			} else {
				throw new IllegalArgumentException("Applicable operation is required");
			}					
		} else {
			throw new IllegalArgumentException("Operation is required");
		}
	}
		
}
