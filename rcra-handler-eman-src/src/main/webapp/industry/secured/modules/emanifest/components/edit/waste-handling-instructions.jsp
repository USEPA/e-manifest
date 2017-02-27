<!-- ko if: internationalShipment -->
<div class="row">
    <div class="col-sm-12 form-group">
        <label class="control-label" for="consent-num">Consent
            Number</label> <input id="consent-num" class="form-control" type="text"
                                  data-bind="consentNumber: consentNumber"/>
    </div>
</div>
<!-- /ko -->
<div class="row">
    <div class="col-sm-12">
        <div class="form-group">
            <label for="specialHandlingInstructions">Special Handling
                Instructions for this Waste</label>
            <textarea id="specialHandlingInstructions"
                      class="form-control" data-bind="textInput: specialHandlingInstructions"></textarea>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-sm-12">
        <div class="form-group">
            <label for="wasteHandlerCommentsDiv">Handler Defined Data for this Waste</label>
            <div id="wasteHandlerCommentsDiv">
                <div class="row"
                     data-bind="slideVisible: handlerComments().length>0">
                    <div class="col-sm-12 table-responsive">
                        <table style="width: 100%" id="wasteHandlerCommentsTable"
                               class="table table-striped table-bordered table-hover dataTable no-wrap">
                            <thead>
                            <tr>
                                <th class="top-align" width="15%">EPA ID
                                    Number
                                </th>
                                <th class="top-align" width="15%">Label</th>
                                <th class="top-align" width="60%">Description</th>
                                <th class="top-align" width="5%">Action</th>
                            </tr>
                            </thead>

                            <tbody data-bind="foreach: handlerComments">
                            <tr>
                                <td width="15%"><span data-bind="text: epaSiteId"></span>
                                </td>
                                <td width="15%"><input
                                        id="wasteHandlerCommentLabel" class="form-control"
                                        type="text" data-bind="value: label"/></td>
                                <td width="60%"><input
                                        id="wasteHandlerCommentDescription"
                                        class="form-control" style="width: 100%;" type="text"
                                        data-bind="value: description"/></td>
                                <td width="5%" style="text-align: center;"><a
                                        href="#"
                                        data-bind="click: function(){$parent.removeWasteHandlerComment($data);}"><span
                                        title="Remove" class="glyphicon glyphicon-remove"
                                        aria-hidden="true"></span></a></td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 form-group">
                        <button class="btn btn-primary"
                                data-bind="click: addWasteHandlerComment, text: handlerComments().length>0?'Add Another Comment':'Add Comment'"></button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>