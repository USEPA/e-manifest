<%@ page contentType="text/html;charset=UTF-8" language="java"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld"%>
<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group table-responsive">
		<label class="constrol-label" for="waste-table" data-bind="slideVisible: wasteSection().wasteCollection().length > 0">Waste
			Characteristics (Total lines: <span data-bind="text: wasteSection().wasteCollection().length"></span>)</label>
		<!-- ko if: wasteSection().wasteCollection().length > 0 -->
		<table id="waste-table" class="table table-striped table-bordered"
			data-bind="slideVisible: wasteSection().wasteCollection().length > 0">
			<thead class="bg-warning">
				<tr class="info">
					<th>Line Number</th>
					<th>U.S. DOT Description</th>
					<th>Containers</th>
					<th>Type</th>
					<th>Total Qty.</th>
					<th>Units</th>
					<th>Waste Codes</th>
					<th>Management <br> Method <br> Code</th>
					<th>Action</th>							
				</tr>
			</thead>
			<tbody data-bind="foreach: wasteSection().wasteCollection">
				<tr>
					<td>
						<span data-bind="text: lineNumber"></span>
					</td>
					<td>
						<span data-bind="text: dotDescriptionDisplay"></span>
					</td>
					<td>
						<span data-bind="text: containerInfo.number">
					</td>
					<td>
						<span data-bind="text: containerInfo.type()==null?'':containerInfo.type().code">
					</td>
					<td>
						<span data-bind="text: containerInfo.quantity">
					</td>
					<td>
						<span data-bind="text: containerInfo.unit()==null?'':containerInfo.unit().code">
					</td>
					<td>
						<span data-bind="text: displayWasteCodes()">
					</td>	
					<td><span data-bind="text: managementCode() ? managementCode().code() : null"></td>
					<td>
						<a href="#" title="View" class="unsavedCheckIgnore"
								data-bind="modal: {
												name: 'review-waste',
												params: {
													data: {
														waste: $data,
														internationalShipment: $parent.internationalShipment
													}
												}
											}">
							<span class="glyphicon glyphicon-eye-open"></span>
						</a>
					</td>
				</tr>
			</tbody>
		</table>
		<!-- /ko -->
	</div>
</div>
<!-- /ko -->