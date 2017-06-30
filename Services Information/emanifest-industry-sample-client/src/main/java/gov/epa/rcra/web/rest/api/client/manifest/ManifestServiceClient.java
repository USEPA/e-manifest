package gov.epa.rcra.web.rest.api.client.manifest;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import gov.epa.rcra.web.rest.api.client.BaseServicesClient;

/**
 * @author sergey
 */
public class ManifestServiceClient extends BaseServicesClient {
	private static final Log logger = LogFactory.getLog(ManifestServiceClient.class);


	public ManifestServiceClient(String restBase, String token) {
		this.restBase = restBase+"/manifest";
		this.token = token;
	}
}
