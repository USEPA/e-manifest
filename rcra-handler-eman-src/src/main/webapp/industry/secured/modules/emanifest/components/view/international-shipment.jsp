<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group">
		<input id="import-to-us" name="shipment-import-export" type="radio"
			data-bind="checked: importToUs, checkedValue: true" disabled></input> 
		<label class="control-label" for="import-to-us">Import to U.S.</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 form-group">
		<input id="export-from-us" name="shipment-import-export"
			type="radio" data-bind="checked: importToUs, checkedValue: false" disabled></input>
		<label class="control-label" for="export-from-us">Export
			from U.S.</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label">Port of Entry/Exit</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-4 form-group">
		<label class="control-label" for="port-city">City</label> 
		<span id="port-city" class="static-info" data-bind="text: city" />
	</div>
	<div class="col-sm-4 form-group">
		<label class="control-label" for="port-state">State</label> 
		<span id="port-state" class="static-info" data-bind="text: state.name"></span>
	</div>
	<div class="col-sm-4 form-group">
		<label class="control-label" for="port-date-leaving">Date
			Leaving U.S.</label> 
		<span id="port-date-leaving" class="static-info" data-bind="text: dateLeaving" />
	</div>
</div>
<!-- /ko -->