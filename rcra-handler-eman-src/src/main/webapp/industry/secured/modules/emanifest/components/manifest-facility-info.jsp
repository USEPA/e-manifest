<%@ taglib prefix="stripes"
	uri="http://stripes.sourceforge.net/stripes-dynattr.tld"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<stripes:layout-definition>
	<script>
		$(function(){
			if (!ko.components.isRegistered('facility-info')){
				ko.components.register('facility-info', {
					template: { element: 'facility-info'}
				});
			}
		});
	</script>
	<template id="facility-info">
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
			<phone-info params="phoneLabel: 'Emergency Response Phone', phoneNumber: emergencyPhone, phoneExtension: emergencyPhoneExt, elemWidthClass: 'col-sm-4 col-md-3'"></phone-info>
			<!-- /ko -->
			<!-- ko if: $parent.contactPhoneNumberVisible == null ||  $parent.contactPhoneNumberVisible-->
			<phone-info params="phoneLabel: 'Contact Phone', phoneNumber: contactPhoneNumber, phoneExtension: contactPhoneNumberExt, elemWidthClass: 'col-sm-4 col-md-3'"></phone-info>
			<!-- /ko -->		
		</div>
	</template>
</stripes:layout-definition>