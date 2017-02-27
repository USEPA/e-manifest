<div class="row" data-bind="slideVisible: isHazardous">
	<div class="col-sm-6">
		<div class="form-group">
			<label class="control-label" for="usDotDescription_waste">Proper
				Shipping Name</label>
			<select id="usDotDescription_waste" class="form-control"
					data-bind="lookup: 'dotDescriptions',
						optionsCaption: 'Select Proper Shipping Name',
						optionsText: function(item){
							return item.shippingName();
						},
						optionsCaption: '',
						optionsValue: 'shippingName',
						valueAllowUnset: true,
						lookupValue: shippingName,
						select2: {allowClear: true, placeholder: 'Select Proper Shipping Name'}">
			</select>

		</div>
	</div>
	<div class="col-sm-2">
		<div class="form-group">
			<div class="row">
				<div class="col-sm-12">
					<label class="control-label">ID Number</label>
				</div>
			</div>
			<div class="row" data-bind="visible: !hasMultiIdNum()">
				<div class="col-sm-12">
					<span data-bind="text: shippingName() && shippingName().unIDNumber() != null ? changeSelectedIdNum(shippingName().unIDNumber()[0]) : null"></span>
				</div>
			</div>
			<div class="row" data-bind="visible: hasMultiIdNum">

				<div class="col-sm-12">
					<select id="id_num_waste" class="form-control"
							data-bind="options: shippingName() && shippingName().unIDNumber() != null ? unIdNumberArray : [],
							optionsCaption: '',
							value: selectedIdNum,
							valueAllowUnset: true,
							select2: {allowClear: true, placeholder: 'Select...'}">
					</select>
				</div>
			</div>
		</div>
	</div>
	<div class="col-sm-2">
		<div class="form-group">
			<div class="row">
				<div class="col-sm-12">
					<label class="control-label">Hazard Class </label>
				</div>
			</div>
			<div class="row" data-bind="visible: !hasMultiHazClass()">
				<div class="col-sm-12">
					<span data-bind="text: shippingName() && shippingName().hazardClass() != null ? changeSelectedHazClass(shippingName().hazardClass()[0]) : null"></span>
				</div>
			</div>
			<div class="row" data-bind="visible: hasMultiHazClass">
				<div class="col-sm-12">
					<select class="form-control"
							data-bind="options: shippingName() && shippingName().hazardClass() != null ? hazClassArray : [],
						optionsCaption: '',
						value: selectedHazClass,
						valueAllowUnset: true,
						select2: {allowClear: true, placeholder: 'Select...'}">
					</select>
				</div>
			</div>
		</div>
	</div>
	<div class="col-sm-2">
		<div class="form-group">
			<div class="row">
				<div class="col-sm-12">
					<label class="control-label">Packing Group </label>
				</div>
			</div>
			<div class="row" data-bind="visible: !hasMultiPackGroup()">
				<div class="col-sm-12">
					<span data-bind="text: shippingName() && shippingName().packingGroup() != null ? changeSelectedPackGroup(shippingName().packingGroup()[0]) : null"></span>
				</div>
			</div>
			<div class="row" data-bind="visible: hasMultiPackGroup">
				<div class="col-sm-12">
					<select class="form-control"
							data-bind="options: shippingName() && shippingName().packingGroup() != null ? packingGroupArray : [],
						optionsCaption: '',
						value: selectedPackGroup,
						valueAllowUnset: true,
						select2: {allowClear: true, placeholder: 'Select...'}">
					</select>
				</div>
			</div>
		</div>

	</div>
</div>
<div class="row">
	<div class="col-sm-12">
		<div class="form-group"
			data-bind="visible: isHazardous">
			<label for="additionalDotInformation" class="control-label">
				Printed DOT Information</label>
			<p>This information will print on the Manifest exactly as shown below. You are responsible to ensure that what is printed on the manifest meets DOT regulations.  Re-order or add information, taking care not to alter selected Proper Shipping Name and related data from what you selected. Use Reset to change selections.</p>
			<textarea id="additionalDotInformation" class="form-control" rows="2" maxRows="2"
				data-bind="textInput:  additionalDotInformation"></textarea>
		</div>
		<div class="form-group"
			data-bind="visible: isHazardous()==false">
			<label class="control-label" for="wasteDescription">
				Waste Description </label>
			<textarea id="wasteDescription" class="form-control" rows="2"
				data-bind="textInput: wasteDescription"></textarea>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-2">
		<div class="form-group">
			<button class="btn btn-success" data-bind="click: resetProperShippingName">Reset</button>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-6 form-group" data-bind="visible: isHazardous">
		<div class="form-group">
			<label class="control-label">Emergency Response Guidebook Number</label>

			<div class="row" data-bind="visible: !hasMultiEmergencyGuideNum()">
				<div class="col-sm-12">
					<span data-bind="text: shippingName() && shippingName().emergencyGuideNumber() != null ? changeSelectedEmergencyGuideNum(shippingName().emergencyGuideNumber()[0]) : null"></span>
				</div>
			</div>
			<div class="row" data-bind="visible: hasMultiEmergencyGuideNum">
				<div class="col-sm-12">
					<select class="form-control"
							data-bind="options: shippingName() && shippingName().emergencyGuideNumber() != null ? guideNumArray : [],
						optionsCaption: '',
						value: selectedEmergencyGuideNum,
						valueAllowUnset: true,
						select2: {allowClear: true, placeholder: 'Select...'}">
					</select>
				</div>
			</div>
		</div>

	</div>

</div>
<div class="row form-group">
	<phone-info params="elemWidthClass: 'col-sm-5 col-md-3', phoneLabel: 'Emergency Response Phone', phoneNumber: emergencyPhone, phoneExtension: emergencyPhoneExt"></phone-info>
</div>
