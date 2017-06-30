package gov.epa.rcra.web.rest.api.client.manifest.lookup;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import gov.epa.rcra.web.rest.api.client.BaseServicesClient;

/**
 * @author sergey
 */
public class EmanifestLookupServiceClient extends BaseServicesClient {
	static final Log logger = LogFactory.getLog(EmanifestLookupServiceClient.class);


	public EmanifestLookupServiceClient(String restBase, String token) {
		this.restBase = restBase+"/emanifest/lookup";
		this.token = token;
	}
	
}
