package gov.epa.rcra.web.rest.api;

import java.util.Properties;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import gov.epa.rcra.web.rest.api.client.auth.AuthInfoLoader;
import gov.epa.rcra.web.rest.api.client.auth.AuthServiceClient;
import gov.epa.rcra.web.rest.api.client.lookup.LookupServiceClient;
import gov.epa.rcra.web.rest.api.client.manifest.ManifestServiceClient;
import gov.epa.rcra.web.rest.api.client.manifest.lookup.EmanifestLookupServiceClient;
import gov.epa.rcra.web.rest.api.client.site.SiteServiceClient;

public class ClientRunner {

	private static HelpFormatter formatter = new HelpFormatter();
	private static final Log logger = LogFactory.getLog(ClientRunner.class);

	public static void main(String[] args) {

		Options options = buildOptions();

		CommandLineParser parser = new DefaultParser();

		try {
			CommandLine line = parser.parse(options, args);
			if (line.getOptions().length == 0) {
				throw new IllegalArgumentException("No arguments given");
			}
			if (line.hasOption("a")) {
				if (line.hasOption("apiId") && line.hasOption("apiKey") && line.hasOption("url")) {
					AuthServiceClient client = new AuthServiceClient(line.getOptionValue("apiId"),
							line.getOptionValue("apiKey"), line.getOptionValue("url"));
					client.authenticate();
				} else {
					throw new IllegalArgumentException("api id, key and end point required");
				}
			}

			if (line.hasOption("s")) {
				if (line.hasOption("operation")) {
					Properties props = AuthInfoLoader.load();					
					SiteServiceClient  serviceClient = new SiteServiceClient(props.getProperty("baseUrl"), props.getProperty("token"));
					String op = line.getOptionValue("operation");	
					if ("site-details".equals(op)) {
						if (line.hasOption("site-id")) {
							serviceClient.execute(line.getOptionValue(op)+"/"+line.getOptionValue("site-id"));
						}else {
							throw new IllegalArgumentException("Site Id is required");
						}						
					}
				} else {
					throw new IllegalArgumentException("Operation is required");
				}			
			}			
			if (line.hasOption("m")) {
				if (line.hasOption("operation")) {
					Properties props = AuthInfoLoader.load();					
					ManifestServiceClient  maClient = new ManifestServiceClient(props.getProperty("baseUrl"), props.getProperty("token"));
					String op = line.getOptionValue("operation");
					if ("get".equals(op)) {
						if (line.hasOption("tracking-number")) {
							maClient.execute(line.getOptionValue("tracking-number"));
						}else {
							throw new IllegalArgumentException("Manifest tracking number is required");
						}
					}
					if ("manifest-tracking-numbers".equals(op)) {
						if (line.hasOption("site-id")) {
							maClient.execute(line.getOptionValue(op)+"/"+line.getOptionValue("site-id"));
						}else {
							throw new IllegalArgumentException("Site Id is required");
						}
					}					
					if ("site-ids".equals(op)) {
						if (line.hasOption("state-code") && line.hasOption("site-type")) {
							maClient.execute(line.getOptionValue(op)+"/"+line.getOptionValue("state-code")+"/"+line.getOptionValue("site-type"));
						}else {
							throw new IllegalArgumentException("Site Id and Site Type are required");
						}
					}					
				} else {
					throw new IllegalArgumentException("Operation is required");
				}
			}
			if (line.hasOption("l")) {
				if (line.hasOption("operation")) {
					Properties props = AuthInfoLoader.load();
					LookupServiceClient lookup = new LookupServiceClient(props.getProperty("baseUrl"),
							props.getProperty("token"));
					String lookupType = line.getOptionValue("operation");
					if ("federal-waste-codes".equals(lookupType) || "source-codes".equals(lookupType)
							|| "form-codes".equals(lookupType) || "density-uom".equals(lookupType)
							|| "source-codes".equals(lookupType) || "density-uom".equals(lookupType)
							|| "management-method-codes".equals(lookupType)) {
						lookup.execute(lookupType);
					}
					if ("state-waste-codes".equals(lookupType)) {
						if (line.hasOption("state-code"))
							lookup.execute(lookupType + "/" + line.getOptionValue("state-code"));
						else {
							throw new IllegalArgumentException("State code is required");
						}
					}
				} else {
					throw new IllegalArgumentException("Lookup operation is required");
				}
			}
			if (line.hasOption("el")) {
				if (line.hasOption("operation")) {
					Properties props = AuthInfoLoader.load();
					EmanifestLookupServiceClient lookup = new EmanifestLookupServiceClient(props.getProperty("baseUrl"),
							props.getProperty("token"));
					String lookupType = line.getOptionValue("operation");
					if ("printed-tracking-number-suffixes".equals(lookupType) || "container-types".equals(lookupType)
							|| "proper-shipping-names".equals(lookupType) || "id-numbers".equals(lookupType)
							|| "hazard-classes".equals(lookupType) || "packing-groups".equals(lookupType)
							|| "emergency-numbers".equals(lookupType) || "quantity-uom".equals(lookupType)) {
						lookup.execute(lookupType);
					}
					if ("packing-groups-by-shipping-name-id-number".equals(lookupType)) {
						if (line.hasOption("id-number") && line.hasOption("ship-name"))
							lookup.execute(lookupType + "/" + line.getOptionValue("ship-name") + "/"
									+ line.getOptionValue("id-number"));
						else {
							throw new IllegalArgumentException("Shipping name and ID Number are required");
						}
					}
					if ("hazard-class-by-shipping-name-id-number".equals(lookupType)) {
						if (line.hasOption("id-number") && line.hasOption("ship-name"))
							lookup.execute(lookupType + "/" + line.getOptionValue("ship-name") + "/"
									+ line.getOptionValue("id-number"));
						else {
							throw new IllegalArgumentException("Shipping name and ID Number are required");
						}
					}

					if ("id-numbers-by-shipping-name".equals(lookupType)) {
						if (line.hasOption("ship-name"))
							lookup.execute(lookupType + "/" + line.getOptionValue("ship-name"));
						else {
							throw new IllegalArgumentException("Shipping name is required");
						}
					}
					if ("proper-shipping-names-by-id-number".equals(lookupType)) {
						if (line.hasOption("id-number"))
							lookup.execute(lookupType + "/" + line.getOptionValue("id-number"));
						else {
							throw new IllegalArgumentException("ID Number is required");
						}
					}
					if ("emergency-numbers-by-id-number".equals(lookupType)) {
						if (line.hasOption("id-number"))
							lookup.execute(lookupType + "/" + line.getOptionValue("id-number"));
						else {
							throw new IllegalArgumentException("ID Number is required");
						}
					}
					if ("emergency-numbers-by-id-number".equals(lookupType)) {
						if (line.hasOption("id-number"))
							lookup.execute(lookupType + "/" + line.getOptionValue("id-number"));
						else {
							throw new IllegalArgumentException("ID Number is required");
						}
					}

				}
			}
		} catch (Throwable e) {
			logger.error(e.getMessage());
			formatter.printHelp("java -jar sample-client-jar-with-dependencies.jar <arguments> ", options);
			//System.out.println("Allowed lookupType value: ");
		}

	}

	static Options buildOptions() {
		Options options = new Options();
		options.addOption(Option.builder("a").desc("Authenticate").hasArg(false).build());
		options.addOption(Option.builder().argName("apiId").desc("Api Id").longOpt("apiId").hasArg().build());
		options.addOption(Option.builder().argName("apiKey").desc("Api Key").longOpt("apiKey").hasArg().build());
		options.addOption(Option.builder().argName("url").desc("Rest Endpoint").longOpt("url").hasArg().build());

		options.addOption(Option.builder("l").desc("Execute Lookup Services").hasArg(false).build());
		options.addOption(Option.builder("el").desc("Execute Emanifest Lookup Services").hasArg(false).build());
		options.addOption(
				Option.builder().argName("operation").desc("Specific Operation").longOpt("operation").hasArg().build());

		options.addOption(
				Option.builder().argName("stateCode").desc("State code").longOpt("state-code").hasArg().build());
		options.addOption(Option.builder().argName("shippingName").desc("Proper shipping name in quotes")
				.longOpt("ship-name").hasArg().build());
		options.addOption(Option.builder().argName("idNumber").desc("ID Number").longOpt("id-number").hasArg().build());

		options.addOption(Option.builder("m").desc("Execute Manifest Services").hasArg(false).build());
		options.addOption(Option.builder().argName("manifestTrackingNumber").desc("Manifest TRacking Number")
				.longOpt("tracking-number").hasArg().build());
		options.addOption(Option.builder().argName("siteId").desc("Site Id").longOpt("site-id").hasArg().build());
		options.addOption(Option.builder().argName("siteType").desc("Site Type (Tsdf, Generator, Transporter")
				.longOpt("site-type").hasArg().build());
		options.addOption(Option.builder("s").desc("Execute Site Services").hasArg(false).build());

		return options;
	}

}
