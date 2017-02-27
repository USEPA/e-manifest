<!-- ko with: form.discrepancy -->
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label">Discrepancy</label>
		<bs-switch params="enable: true, flag: discrepancy"></bs-switch>
	</div>
</div>
<div data-bind="slideVisible: discrepancy">
	<div class="row">
		<div class="col-sm-12 form-group">
			<label class="control-label">Select all that apply:</label>
			<div class="checkbox">
				<label><input type="checkbox" name="rejection-type" value="Quantity" data-bind="checked: types"/>Quantity</label>
			</div>
			<div class="checkbox">
				<label><input type="checkbox" name="rejection-type" value="Type" data-bind="checked: types"/>Type</label>
			</div>
			<div class="checkbox">
				<label><input type="checkbox" name="rejection-type" value="Residue" data-bind="checked: types"/>Residue</label>
			</div>
		</div>
	</div>
	<div class="well">
		<div class="row">
			<div class="col-sm-12 form-group">
				<label class="control-label" for="rejection-type">Rejection Information</label>
				<select class="form-control" id="rejection-type" data-bind="options: ['Partial', 'Full'],
																			value: rejectionType,
																			optionsCaption: '',
																			select2:{
																				allowClear: true,
																				placeholder: 'None'
																			}">
				</select>
			</div>
		</div>
		<div data-bind="slideVisible: showReferenceTrackingNumber">
			<div class="row">
				<div class="col-sm-12 form-group">
					<label class="control-label" for="manifest-tracking-number-reference">Related Manifest Tracking Number</label>
					<input id="manifest-tracking-number-reference" class="form-control" type="text" data-bind="value: referenceTrackingNumber"/>
				</div>
			</div>
		</div>
		<div data-bind="slideVisible: rejectionType() == 'Full'">
			<div class="row">
				<div class="col-sm-12 form-group">
					<label class="control-label"><input type="radio" name="refection-full" data-bind="checked: fullRejectionType, checkedValue: 'number'"/>Manifest Tracking Number for Reference</label>
					<div data-bind="slideVisible: fullRejectionType() == 'number'">
						<label class="sr-only" for="manifest-tracking-number-reference-full">Manifest Tracking Number for Reference</label>
						<input id="manifest-tracking-number-reference-full" class="form-control" type="text" data-bind="value: referenceTrackingNumber"/>
					</div>
				</div>
				<div class="col-sm-12 form-group">
					<label class="control-label"><input type="radio" name="refection-full" data-bind="checked: fullRejectionType, checkedValue: 'facility'"/>Alternate Facility using this Manifest</label>
					<div data-bind="slideVisible: fullRejectionType() == 'facility'">
						<label class="sr-only"for="manifest-send-alternate-facility"> Alternate Facility using this Manifest</label>
						<select id="manifest-send-alternate-facility" class="form-control" data-bind="options: alternateFacilities,
																									lookupValue: alternateFacility,
																									optionsValue: 'epaSiteId',
																									optionsText: 'display',
																									optionsCaption: '',
																									select2: {
																										allowClear: true,
																										placehodler: 'Select Alternate Facility'
																									}">
							
						</select>
					</div>
				</div>
			</div>
		</div>
	</div>
	<div class="row">
		<div class="col-sm-12 form-group">
			<label class="control-label" for="discrepancy-comments">Discrepancy Comments</label>
			<textarea class="form-control" id="discrepancy-comments" data-bind="value: comment"></textarea>
		</div>
	</div>
</div>
<!-- /ko -->