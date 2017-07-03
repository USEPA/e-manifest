package gov.epa.rcra.web.rest.api.client.lookup;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import gov.epa.rcra.web.rest.api.client.BaseServicesClient;

/**
 * @author sergey
 */
public class LookupServiceClient extends BaseServicesClient {
	private static final Log logger = LogFactory.getLog(LookupServiceClient.class);


	public LookupServiceClient(String restBase, String token) {
		this.restBase = restBase+"/lookup";
		this.token = token;
	}
}
