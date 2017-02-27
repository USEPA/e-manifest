<!-- ko if: internationalShipment -->
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label" for="consent-num">Consent Number</label> 
		<span class="static-info help-block" data-bind="text: consentNumber"></span>
	</div>
</div>
<!-- /ko -->
<div class="row">
	<div class="col-sm-12">
		<div class="form-group">
			<label for="specialHandlingInstructions">Special Handling Instructions for this Waste</label>
			<pre class="static-info help-block" data-bind="text: specialHandlingInstructions"></pre>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-12">
		<div class="form-group">
			<label for="wasteHandlerCommentsDiv">Handler Defined Data for this Waste</label>
			<div id="wasteHandlerCommentsDiv">
				<div class="row" data-bind="if: handlerComments().length>0">
					<div class="col-sm-12 table-responsive">
						<table style="width: 100%" id="wasteHandlerCommentsTable"
							class="table table-striped table-bordered table-hover dataTable no-wrap">
							<thead>
								<tr>
									<th class="top-align" width="15%">EPA ID Number</th>
									<th class="top-align" width="15%">Label</th>
									<th class="top-align" width="65%">Description</th>
								</tr>
							</thead>
							<tbody data-bind="foreach: handlerComments">
								<tr>
									<td width="15%">
										<span data-bind="text: epaSiteId"></span>
									</td>
									<td width="15%">
										<span class="static-info help-block" data-bind="text: label"></span>
									</td>
									<td width="65%">
										<span class="static-info help-block" data-bind="text: description"></span>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
<!-- /ko -->