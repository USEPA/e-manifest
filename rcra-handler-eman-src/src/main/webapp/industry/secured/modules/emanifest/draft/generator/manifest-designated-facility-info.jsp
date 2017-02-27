<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<stripes:layout-definition>
<div class="panel panel-default panel-info">
	<div class="panel-heading">8. Designated Facility Information</div>
	<div class="panel-body">
		<!-- ko ifnot: generatorPartialEdit -->
			<div class="row">
				<div class="col-sm-12 form-group">
					<label class="control-label" for="designated-facility">EPA ID - Name</label>
					<select id="designated-facility" class="form-control"
						data-bind="lookup: 'tsdfs', 
								optionsCaption: '',
								optionsValue: 'epaSiteId',
							  	optionsText: 'display', 
							  	lookupValue: tsdf, 
							  	select2: {allowClear: true, placeholder: 'Select Designated Facility'} "></select>
				</div>
			</div>
		<!-- /ko -->
		<!-- TODO need to understand if these conditions needed  -->
		<div data-bind="slideVisible: tsdf() != null && tsdf().epaSiteId() != null">
			<!-- ko ifnot: generatorPartialEdit -->
				<hr>
				<facility-info params="facilityInfo: tsdf, emergencyPhoneVisible: false"></facility-info>
			<!-- /ko -->
			<!-- ko if: generatorPartialEdit -->
				<facility-info-review params="facilityInfo: tsdf, emergencyPhoneVisible: false"></facility-info-review>
			<!-- /ko -->
		</div>
	</div>
</div>
</stripes:layout-definition>