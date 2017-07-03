package gov.epa.rcra.web.rest.api.client.cli.commands;

import java.util.Properties;

import org.apache.commons.lang3.StringUtils;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

import gov.epa.rcra.web.rest.api.client.auth.AuthInfoLoader;
import gov.epa.rcra.web.rest.api.client.lookup.LookupServiceClient;

@Parameters(commandDescription="Call Lookup Service",commandNames="lookup")
public class LookupCommand extends BaseCommand {
		
	@Parameter(names = { "--operation"}, description = "Specific Lookup Operation, possible values: 'federal-waste-codes', "
			+ "'form-codes', 'density-uom', 'source-codes', 'density-uom', 'management-method-codes', 'state-waste-codes'", required=true)	
	protected String operation;

	@Parameter(names = { "--state-code"}, description = "State Code (used with 'state-waste-codes' operation)")		
	protected String stateCode;

	public String getStateCode() {
		return stateCode;
	}

	public void setStateCode(String stateCode) {
		this.stateCode = stateCode;
	}

	public String getOperation() {
		return operation;
	}

	public void setOperation(String operation) {
		this.operation = operation;
	}
	
	
	public void run() {
		if (StringUtils.isNotBlank(operation)) {
			Properties props = AuthInfoLoader.load();
			LookupServiceClient lookup = new LookupServiceClient(props.getProperty("baseUrl"),
					props.getProperty("token"));
			if ("federal-waste-codes".equals(operation) || "source-codes".equals(operation)
					|| "form-codes".equals(operation) || "density-uom".equals(operation)
					|| "source-codes".equals(operation) || "density-uom".equals(operation)
					|| "management-method-codes".equals(operation)) {
				lookup.execute(operation);
			}
			else if ("state-waste-codes".equals(operation)) {
				if (StringUtils.isNotBlank(stateCode))
					lookup.execute(operation + "/" + stateCode);
				else {
					throw new IllegalArgumentException("State code is required");
				}
			} else {
				throw new IllegalArgumentException("Applicable operation is required");
			}
		} else {
			throw new IllegalArgumentException("Lookup operation is required");
		}
	}
	
	

}
