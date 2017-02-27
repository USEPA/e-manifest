<!-- ko with: form -->
<!-- ko if: tsdf() && tsdf().epaSiteId() -->
<facility-info params="facilityInfo: tsdf, emergencyPhoneVisible: false"></facility-info>
<!-- /ko -->
<!-- ko ifnot: tsdf() && tsdf().epaSiteId() -->
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
<!-- /ko -->