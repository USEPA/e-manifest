<div class="row" data-bind="with: facilityInfo">
    <div class="col-sm-3 form-group">
        <label class="control-label">EPA ID Number</label>
        <input type="text" class="form-control" data-bind="value: epaSiteId, disable: $parent.editMode"/>
    </div>
    <div class="col-sm-9 form-group">
        <label class="control-label" for="genName">Name</label>
        <input type="text" id="genName" class="form-control" data-bind="value:siteName"/>
    </div>
    <div class="col-sm-12">
        <div class="h4">Mailing Address</div>
        <address-info-edit params="address: address"></address-info-edit>
    </div>
    <div class="col-sm-12">
        <div class="h4">Site Address</div>
        <div class="checkbox">
        	<label>
        		<input type="checkbox" data-bind="checked: siteAddressSame">Site address is same as mailing address
        	</label>
        </div>
        <address-info-edit params="address: siteAddress"></address-info-edit>
    </div>
</div>
<div class="row form-group" data-bind="with: facilityInfo">
    <!-- ko if: $parent.emergencyPhoneVisible == null || $parent.emergencyPhoneVisible-->
    <phone-info params="phoneLabel: 'Emergency Response Phone', phoneNumber: emergencyPhone, phoneExtension: emergencyPhoneExt"></phone-info>
    <!-- /ko -->
    <!-- ko if: $parent.contactPhoneNumberVisible == null ||  $parent.contactPhoneNumberVisible-->
    <phone-info params="phoneLabel: 'Contact Phone', phoneNumber: contactPhoneNumber, phoneExtension: contactPhoneNumberExt"></phone-info>
    <!-- /ko -->
</div>