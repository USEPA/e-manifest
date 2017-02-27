<!-- ko with: address  -->
<div class="row">
    <div class="col-sm-12 form-group">
        <label class="control-label" for="street">Street Address</label>
        <input type="text" class="form-control" id="street" data-bind="value: street">
    </div>
</div>
<div class="row">
    <div class="col-sm-3 form-group">
            <label class="control-label" for="zip">Zip</label>
            <input type="text" class="form-control" id="zip" maxlength="14" data-bind="value: zip">
            <%-- TODO use auto fill --%>
            <%--<input type="text" class="form-control" id="zip" maxlength="14" data-bind="zipAutofill: {
                zip: zip,
                city: {
                    observable: city,
                    id: city
                },
                state: state,
                stateList: {
                    key: 'code',
                    data: lookups.states
                },
                url: '${pageContext.request.contextPath}/rest/public/lookup/city-state'
            }, maskedZip: zip">--%>
    </div>
    <div class="col-sm-5 form-group">
        <label class="control-label" for="city">City, Town or Village</label>
        <input type="text" class="form-control" id="city" data-bind="value: city">
    </div>
    <div class="col-sm-4 form-group">
        <label class="control-label" for="state">State</label>
        <select class="form-control" id="state" data-bind="lookup: 'states',
                                                            value: state,
                                                            optionsValue: 'code',
                                                            optionsText: 'name',
                                                            optionsCaption: '',
                                                            valueAllowUnset: true,
                                                            select2: {
                                                                placeholder: 'Select State'
                                                            }"></select>
    </div>
</div>
<!-- /ko -->