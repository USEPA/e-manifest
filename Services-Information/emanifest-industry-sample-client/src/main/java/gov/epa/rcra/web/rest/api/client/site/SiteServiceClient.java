package gov.epa.rcra.web.rest.api.client.site;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import gov.epa.rcra.web.rest.api.client.BaseServicesClient;

/**
 * @author sergey
 */
public class SiteServiceClient extends BaseServicesClient {
	private static final Log logger = LogFactory.getLog(SiteServiceClient.class);


	public SiteServiceClient(String restBase, String token) {
		this.restBase = restBase;
		this.token = token;
	}
}
