<div id="federalHazWasteCodes" data-bind="slideVisible: isHazardous">
	<div class="row">
		<div class="col-sm-3">
			<div class="form-group">
				<label for="federalHazCodeMulti">Federal </label>
					<select id="federalHazCodeMulti" class="form-control"
							data-auto-select="false" multiple
							data-bind="attr: { disabled: lookups.federalHazardousWasteCodeOptions().length <= 0 },
															   options: lookups.federalHazardousWasteCodeOptions,
															   optionsText: function (item) {
																  return ko.unwrap(item.code);
															   },
															   optionsValue: 'code',
															   multiselect: {
																  buttonWidth: '100%',
																  numberDisplayed: 0,
																  maxHeight: 200,
																  enableFiltering: true,
																  enableCaseInsensitiveFiltering: true},
															  selectedOptions: federalHazCodes">
				</select>
			</div>
			<a href="#" id="clearAllFederalCodes"
				data-bind="click: clearFederalHazCodes, clickBubble: false"
				class="btn btn-success">Clear All</a>
		</div>
		<div class="col-sm-9">
			<div class="form-group">
				<label for="hazCodeMultiSelected">
					Selected </label> <input id="hazCodeMultiSelected"
					class="form-control" value=""
					data-bind="tokenfield: federalHazCodes,
										 tokenListLookup: {
											  values: lookups.federalHazardousWasteCodeOptions,
											  key: 'code',
											  description: 'description'
										  }">
			</div>
		</div>
	</div>
</div>
<hr data-bind="slideVisible: isHazardous"></hr>
<div id="stateGenHazWasteCodes">
	<div class="row">
		<div class="col-sm-3">
			<div class="form-group">
				<label for="stateGenHazCodeMulti"
					data-bind="text: tsdf() != null  && tsdf().hasSameState(generator())?'State':'State - Generator'">
					State - Generator </label> <select id="stateGenHazCodeMulti"
					class="form-control" data-auto-select="false" multiple
					data-bind="attr: { disabled: lookups.stateHazardousWasteCodeOptions().length <= 0 },
															   options: lookups.stateHazardousWasteCodeOptions,
															   optionsText: function (item) {
																  return ko.unwrap(item.code);
															   },
															   optionsValue: 'code',
															   multiselect: {
																  buttonWidth: '100%',
																  numberDisplayed: 0,
																  maxHeight: 200,
																  enableFiltering: true,
																  enableCaseInsensitiveFiltering: true},
															  selectedOptions: stateGenHazCodes">
				</select>
			</div>
			<a href="#" id="clearAllStateGenCodes"
				data-bind="click: clearStateGenHazCodes, clickBubble: false"
				class="btn btn-success">Clear All</a>

		</div>
		<div class="col-sm-9">
			<div class="form-group">
				<label
					for="stateGenHazCodeMultiSelected"> Selected </label> <input
					id="stateGenHazCodeMultiSelected" class="form-control"
					value=""
					data-bind="tokenfield: stateGenHazCodes,
										 tokenListLookup: {
											  values: lookups.stateHazardousWasteCodeOptions,
											  key: 'code',
											  description: 'description'
										  }">
			</div>
		</div>
	</div>
</div>
<hr  data-bind="visible: tsdf() != null && !tsdf().hasSameState(generator())">
<div id="stateTsdfHazWasteCodes" data-bind="visible: tsdf() != null && !tsdf().hasSameState(generator())">
	<div class="row">
		<div class="col-sm-3">
			<div class="form-group">
				<label for="stateTsdfHazCodeMulti">
					State - TSDF </label> <select id="stateTsdfHazCodeMulti"
					class="form-control" data-auto-select="false" multiple
					data-bind="attr: { disabled: lookups.stateHazardousWasteCodeOptions().length <= 0 },
															   options: lookups.stateHazardousWasteCodeOptions,
															   optionsText: function (item) {
																  return ko.unwrap(item.code);
															   },
															   optionsValue: 'code',
															   multiselect: {
																  buttonWidth: '100%',
																  numberDisplayed: 0,
																  maxHeight: 200,
																  enableFiltering: true,
																  enableCaseInsensitiveFiltering: true},
															  selectedOptions: stateTsdfHazCodes">
				</select>
			</div>
			<a href="#" id="clearAllStateTsdfCodes"
				data-bind="click: clearStateTsdfHazCodes, clickBubble: false"
				class="btn btn-success">Clear All</a>

		</div>
		<div class="col-sm-9">
			<div class="form-group">
				<label
					for="stateTsdfHazCodeMultiSelected"> Selected </label> <input
					id="stateTsdfHazCodeMultiSelected" class="form-control"
					value=""
					data-bind="tokenfield: stateTsdfHazCodes,
										 tokenListLookup: {
											  values: lookups.stateHazardousWasteCodeOptions,
											  key: 'code',
											  description: 'description'
										  }">
			</div>
		</div>
	</div>
</div>
<hr></hr>
<div class="row">
	<div class="col-sm-12">
		<div class="form-group">
			<label for="managementCode" class="control-label">Management Method Code</label>
			<select id="managementCode" class="form-control"
					data-bind="options: lookups.methodCodes,
							optionsCaption: '',
							optionsText: function(item){
								return item.code() +'-'+item.description();
							},
							optionsValue: 'code',
							lookupValue: managementCode,
							select2: {allowClear: true, placeholder: 'Select Management Method Code'}">
			</select>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-12">
		<div class="form-group"
			data-bind="slideVisible: managementCodeCommentVisible()">
			<label for="managementCodeComment" >Management
				Method Code Comment</label>
			<textarea id="managementCodeComment" class="form-control"
				data-bind="textInput: managementCodeComment"></textarea>
		</div>
	</div>
</div>