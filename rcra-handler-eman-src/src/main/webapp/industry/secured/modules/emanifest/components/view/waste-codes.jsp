	<div id="federalHazWasteCodes" data-bind="slideVisible: isHazardous">
		<div class="row">
			<div class="col-sm-12">
				<div class="form-group">
					<label for="federalHazCodeMulti">Federal </label> 
					<!-- ko if: federalHazCodes().length > 0 -->
						<!--  ko foreach: federalHazCodes-->
							<span class="static-info help-block" data-bind="text: $data"></span>
						<!-- /ko -->
					<!-- /ko -->
					<!-- ko ifnot: federalHazCodes().length > 0 -->
						<span class="help-block static-info">No codes selected</span>
					<!-- /ko -->
				</div>
			</div>
		</div>
	</div>
	<hr data-bind="slideVisible: isHazardous">
	<div id="stateGenHazWasteCodes">
		<div class="row">
			<div class="col-sm-12">
				<div class="form-group">
					<label for="stateGenHazCodeMulti">State</label>
						<!-- ko if: stateGenHazCodes().length > 0 -->
							<!-- ko if: stateTsdfHazCodes().length > 0 -->
								<label>- Generator</label>
							<!-- /ko -->
							<!-- ko foreach: stateGenHazCodes-->
								<span class="help-block static-info" data-bind="text: $data"></span>
							<!-- /ko -->
						<!-- /ko -->
						<!-- ko ifnot: stateGenHazCodes().length > 0 -->
							<span class="help-block static-info">No codes selected</span>
						<!-- /ko -->
						<!-- ko if: stateTsdfHazCodes().length > 0 -->
							<!-- ko if: stateGenHazCodes().length > 0 -->
								<label>State - TSDF</label>
							<!-- /ko -->
							<!-- ko foreach: stateTsdfHazCodes -->
								<span class="help-block static-info" data-bind="text: $data"></span>
							<!-- /ko -->
							<!-- ko ifnot: stateTsdfHazCodes().length > 0-->
								<span class="static-info help-block">No codes selected</span>
							<!-- /ko -->
						<!-- /ko -->
				</div>
			</div>
		</div>
	</div>
	<!-- /ko -->
	<hr>
	<div class="row">
		<div class="col-sm-12">
			<div class="form-group">
				<label for="managementCode" class="control-label">Management Method Code</label>
				<span class="help-block static-info" data-bind="text: managementCode() && managementCode().code"></span>
			</div>
		</div>
	</div>
	<div class="row">
		<div class="col-sm-12">
			<div class="form-group"
				data-bind="slideVisible: managementCodeCommentVisible()">
				<label for="managementCodeComment" >Management
					Method Code Comment</label>
				<span class="static-info help-block" data-bind="text: managementCodeComment"></span>
			</div>
		</div>
	</div>
	<!-- /ko -->