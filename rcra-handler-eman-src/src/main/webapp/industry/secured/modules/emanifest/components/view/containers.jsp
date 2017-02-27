<div class="row">
	<div class="col-sm-2 col-md-1">
		<div class="form-group">
			<label for="containersNumber" class="control-label">Number</label>
			<span class="static-info help-block" data-bind="text: number"></span>
		</div>
	</div>
	<div class="col-sm-6 col-md-6">
		<div class="form-group">
			<label for="containersType" class="control-label">Type</label>
			<span class="static-info help-block" data-bind="text: type().code() + ' - ' + type().description()"></span>
		</div>
	</div>
	<!-- ko if: type() && type().code() == 'NL' -->
	<div class="col-sm-3">
		<div class="form-group">
			<label for="notListedType" class="control-label">Not Listed Type</label> 
			<span class="static-info help-block" data-bind="text: notListedType"></span>
		</div>
	</div>
	<!-- /ko -->
	<div class="col-sm-3 col-md-2">
		<div class="form-group">
			<label for="containersTotalQuantity">Quantity</label> 
			<span class="static-info help-block" data-bind="text: quantity"></span>
		</div>
	</div>
	<div class="col-sm-4 col-md-3">
		<div class="form-group">
			<label for="containersUnit" class="control-label" style="white-space: nowrap;">Unit Wt./Vol.</label>
			<span class="static-info help-block" data-bind="text: unit().code() + ' - ' + unit().description()"></span>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-12">
		<div class="panel panel-default">
			<div class="panel-heading">Biennial Report Information</div>
			<div class="panel-body">
				<div class="row">
					<div class="col-sm-12">
						<div class="form-group">
							<label for="hazWaste">Provide BR Information? </label>
							<span class="static-info help-block" data-bind="text: provideBRInfo() ? 'Yes' : 'No'"></span>
						</div>
					</div>
				</div>
				<div id="brInfo" data-bind="if: provideBRInfo">
					<div class="row">
						<div class="col-sm-2">
							<div class="form-group"
								data-bind="slideVisible: showDensity">
								<label for="containersDensity">Density</label>
								<span class="static-info help-block" data-bind="text: density"></span>
							</div>
						</div>
						<div class="col-sm-2">
							<div class="form-group"
								data-bind="slideVisible: showDensity">
								<label for="containersDensityUnits">Density Units</label>
								<span class="static-info help-block" data-bind="text: densityUnit"></span>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group">
								<label for="formCode" class="control-label">Form Code</label>
								<span class="static-info help-block" data-bind="text: formCode() && formCode().code()"></span>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group"
								data-bind="slideVisible: formCommentVisible()">
								<label for="formCodeComment" class="control-label">Form
									Code Comment</label>
								<pre class="static-info help-block" data-bind="text: formCodeComment"></pre>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group">
								<label for="sourceCode" class="control-label">Source Code</label>
								<span class="static-info help-block" data-bind="text: sourceCode() && sourceCode().code()"></span>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group"
								data-bind="slideVisible: sourceCommentVisible()">
								<label for="sourceCodeComment" class="control-label">Source Code Comment</label>
								<pre data-bind="text: sourceCodeComment"></pre>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>