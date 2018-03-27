package gov.epa.rcra.web.rest.api;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.beust.jcommander.JCommander;

import gov.epa.rcra.web.rest.api.client.cli.commands.AuthenticateCommand;
import gov.epa.rcra.web.rest.api.client.cli.commands.BaseCommand;
import gov.epa.rcra.web.rest.api.client.cli.commands.LookupCommand;
import gov.epa.rcra.web.rest.api.client.cli.commands.ManifestCommand;
import gov.epa.rcra.web.rest.api.client.cli.commands.ManifestLookupCommand;
import gov.epa.rcra.web.rest.api.client.cli.commands.SiteCommand;

public class ClientRunner {

	private static final Log logger = LogFactory.getLog(ClientRunner.class);

	public static void main(String[] args) {

		JCommander b = buildCommands();
		
		try {
			b.parse(args);
			if (b.getParsedCommand() == null)
				throw new IllegalArgumentException();
			((BaseCommand)b.getCommands().get(b.getParsedCommand()).getObjects().get(0)).run();			
		} catch (Throwable e) {
			logger.error(e.getMessage());			
			b.usage();
		}

	}

	private static JCommander buildCommands() {
		AuthenticateCommand authCommand = new AuthenticateCommand();
		LookupCommand lookupCommand = new LookupCommand();
		SiteCommand siteCommand = new SiteCommand();
		ManifestLookupCommand manifestLookupCommand = new ManifestLookupCommand();
		ManifestCommand manifestCommand = new ManifestCommand();
		JCommander b = JCommander.newBuilder()
		  .addCommand(authCommand).addCommand(lookupCommand).addCommand(siteCommand).addCommand(manifestCommand)
		  .addCommand(manifestLookupCommand).acceptUnknownOptions(true)
		  .build();
		b.setProgramName("java -jar sample-client-jar-with-dependencies.jar ");
		return b;
	}

}
