package gov.epa.rcra.web.rest.api.client.cli.commands;

import java.util.Properties;

import org.apache.commons.lang3.StringUtils;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

import gov.epa.rcra.web.rest.api.client.auth.AuthInfoLoader;
import gov.epa.rcra.web.rest.api.client.manifest.lookup.EmanifestLookupServiceClient;

@Parameters(commandDescription="Call Manifest Lookup Service",commandNames="emlookup")
public class ManifestLookupCommand extends BaseCommand{
	
	@Parameter(names = { "--operation"}, description = "Specific Manifest Lookup Operation, possible values: 'printed-tracking-number-suffixes', "
			+ "'container-types', 'proper-shipping-names', 'id-numbers', 'hazard-classes', 'packing-groups', 'emergency-numbers', "
			+ "'quantity-uom', 'packing-groups-by-shipping-name-id-number', 'hazard-class-by-shipping-name-id-number', 'id-numbers-by-shipping-name', "
			+ "'proper-shipping-names-by-id-number', 'emergency-numbers-by-id-number'", required=true)	
	protected String operation;
	
	
	@Parameter(names = { "--id-number"}, description = "DOT Id Number (used with 'packing-groups-by-shipping-name-id-number', "
			+ "'hazard-class-by-shipping-name-id-number', 'proper-shipping-names-by-id-number', 'emergency-numbers-by-id-number' operations)")		
	protected String idNumber;

	@Parameter(names = { "--ship-name"}, description = "DOT Proper Shipping Name (specifed in quotes due to spaces, "
			+ "used with 'packing-groups-by-shipping-name-id-number', "
			+ "'hazard-class-by-shipping-name-id-number', 'id-numbers-by-shipping-name' operations)")			
	protected String shipName;

	public String getOperation() {
		return operation;
	}

	public void setOperation(String operation) {
		this.operation = operation;
	}

	public String getIdNumber() {
		return idNumber;
	}

	public void setIdNumber(String idNumber) {
		this.idNumber = idNumber;
	}

	public String getShipName() {
		return shipName;
	}

	public void setShipName(String shipName) {
		this.shipName = shipName;
	}


	public void run() {
		if (StringUtils.isNotBlank(operation)) {
			Properties props = AuthInfoLoader.load();
			EmanifestLookupServiceClient lookup = new EmanifestLookupServiceClient(props.getProperty("baseUrl"),
					props.getProperty("token"));
			if (StringUtils.isBlank(operation)) {
				throw new IllegalArgumentException("Operation is required");
			}
			if ("printed-tracking-number-suffixes".equals(operation) || "container-types".equals(operation)
					|| "proper-shipping-names".equals(operation) || "id-numbers".equals(operation)
					|| "hazard-classes".equals(operation) || "packing-groups".equals(operation)
					|| "emergency-numbers".equals(operation) || "quantity-uom".equals(operation)) {
				lookup.execute(operation);
			}
			else if ("packing-groups-by-shipping-name-id-number".equals(operation)) {
				if (shipNameAndIdNumberValid())
					lookup.execute(operation + "/" + shipName + "/"
							+ idNumber);
				else {
					throw new IllegalArgumentException("Shipping name and ID Number are required");
				}
			}
			else if ("hazard-class-by-shipping-name-id-number".equals(operation)) {
				if (shipNameAndIdNumberValid())
					lookup.execute(operation + "/" + shipName + "/"
							+ idNumber);
				else {
					throw new IllegalArgumentException("Shipping name and ID Number are required");
				}
			}
			else if ("id-numbers-by-shipping-name".equals(operation)) {
				if (StringUtils.isNotBlank(shipName))
					lookup.execute(operation + "/" + shipName);
				else {
					throw new IllegalArgumentException("Shipping name is required");
				}
			}
			else if ("proper-shipping-names-by-id-number".equals(operation)) {
				if (StringUtils.isNotBlank(idNumber))
					lookup.execute(operation + "/" + idNumber);
				else {
					throw new IllegalArgumentException("ID Number is required");
				}
			}
			else if ("emergency-numbers-by-id-number".equals(operation)) {
				if (StringUtils.isNotBlank(idNumber))
					lookup.execute(operation + "/" + idNumber);
				else {
					throw new IllegalArgumentException("ID Number is required");
				}
			} else {
				throw new IllegalArgumentException("Applicable operation is required");
			}
		}
	}

	private boolean shipNameAndIdNumberValid() {
		return StringUtils.isNotBlank(idNumber) && StringUtils.isNotBlank("shipName");
	}
	
	
		
}
