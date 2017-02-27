<div class="row form-group" data-bind="with: facilityInfo">
	<div class="col-sm-3">
		<label class="control-label">EPA ID Number</label>
		<span class="help-block static-info" data-bind="text: epaSiteId"></span>
	</div>
	<div class="col-sm-9">
		<label class="control-labecl" for="genName">Name</label> 
		<span class="help-block static-info" id="genName" data-bind="text: siteName"></span>
	</div>
	<!-- ko if: address && address.street -->
	<div class="col-sm-12">
		<address-info params="addressLabel: 'Mailing Address', address: address"></address-info>
	</div>
	 <!-- /ko -->
	<!-- ko if: siteAddress && siteAddress.street -->
	<div class="col-sm-12">
		<address-info params="addressLabel: 'Site Address', address: siteAddress"></address-info>
	</div>
	 <!-- /ko -->
</div>
<div class="row form-group" data-bind="with: facilityInfo">
	<!-- ko if: $parent.emergencyPhoneVisible == null || $parent.emergencyPhoneVisible-->
	<phone-info-review params="phoneLabel: 'Emergency Response Phone', phoneNumber: emergencyPhone, phoneExtension: emergencyPhoneExt"></phone-info-review>
	<!-- /ko -->
	<!-- ko if: $parent.contactPhoneNumberVisible == null ||  $parent.contactPhoneNumberVisible-->
	<phone-info-review params="phoneLabel: 'Contact Phone', phoneNumber: contactPhoneNumber, phoneExtension: contactPhoneNumberExt"></phone-info-review>
	<!-- /ko -->		
</div>