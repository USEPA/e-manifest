<!-- ko with: site -->
    <div class="row">
        <div class="col-sm-2 form-group">
            <label class="control-label">EPA ID Number</label>
            <span class="static-info help-block" data-bind="text: epaSiteId"></span>
        </div>
        <div class="col-sm-4 form-group">
            <label class="control-label">Name</label>
            <span class="static-info help-block" data-bind="text: siteName"></span>
        </div>
        <div class="col-sm-4 form-group">
            <label class="control-label" for="offeror-name"><span data-bind="text: $parent.siteType"></span> Name</label>
            <input type="text" class="form-control" id="offeror-name" data-bind="value: signature().printedName, validationElement: signature().printedName"/>
            <span class="validationMessage" data-bind="validationMessage: signature().printedName"></span>
        </div>
        <div class="col-sm-2 form-group">
            <label class="control-label" for="offeror-signed-date">Date Signed</label>
            <div class="input-group date">
                <input type="text" class="form-control" id="offeror-signed-date" data-bind="value: signature().signatureDate, datepicker, validationElement: signature().signatureDate"/>
                <span class="validationMessage" data-bind="validationMessage: signature().signatureDate"></span>
                <span class="input-group-addon">
                    <span class="glyphicon glyphicon-th"></span>
                </span>
            </div>
        </div>
    </div>
<!-- /ko -->