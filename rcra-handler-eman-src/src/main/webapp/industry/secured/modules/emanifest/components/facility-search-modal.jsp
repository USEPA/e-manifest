<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="display" uri="http://displaytag.sf.net/el" %>
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>
<stripes:layout-render name="/industry/secured/modules/emanifest/common/modal-layout.jsp" title="Search" addClass="modal-lg modal-xlg">
    <stripes:layout-component name="body">
        <!-- ko if: showSearch -->
            <!-- ko with: searchCriteria -->
                <div class="row">
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="siteId" class="control-label">Generator ID</label>
                            <input type="text" id="siteId" class="form-control" data-bind="validationOptions: { insertMessages: false },textInput: handlerId" />
                        </div>
                    </div>
                    <div class="col-sm-8">
                        <div class="form-group">
                            <label for="siteName" class="control-label">Generator Name</label>
                            <input type="text" id="siteName" class="form-control" data-bind="validationOptions: { insertMessages: false },textInput: handlerName" />
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="streetNumber" class="control-label">Street Number</label>
                            <input type="text" id="streetNumber" class="form-control" data-bind="textInput: streetNumber" />
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="streetName" class="control-label">Street Name</label>
                            <input type="text" id="streetName" class="form-control" data-bind="textInput: streetName" />
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="city" class="control-label">City</label>
                            <input type="text" id="city" class="form-control" data-bind="textInput: city" />
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="state" class="control-label">State</label>
                            <select id="state" class="form-control" data-bind="value: state,
                                    lookup: 'states',
                                    optionsValue: 'code',
                                    optionsText: 'name',
                                    valueAllowUnset: true,
                                    optionsCaption: 'Select a State'">
                            </select>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="country" class="control-label">County</label>
                            <%--<select id="country" class="form-control" data-bind="value: country,
                                    lookup: 'counties',
                                    optionsValue: 'code',
                                    optionsText: 'name',
                                    optionsCaption: 'Select a County',
                                    attr: {disabled: lookups.counties().length == 0}">                            >
                            </select>--%>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label for="zip" class="control-label">Zip</label>
                            <input type="text" id="zip" class="form-control" data-bind="validationOptions: { insertMessages: false }, textInput: zip" />
                        </div>
                    </div>
                </div>
                <!-- ko if: $parent.conditionalValidationMessage -->
                    <div class="row top-buffer">
                        <div class="col-sm-12">
                            <span class="validationMessage" data-bind="text: $parent.conditionalValidationMessage"></span>
                        </div>
                    </div>
                <!-- /ko -->
            <!-- /ko -->
        <!-- /ko -->
        <!-- ko if: showResults -->
            <!-- ko with: searchResults -->
                <div class="row">
                    <div class="col-sm-12">
                        <table id="addGenResultsTable"
                               class="table table-striped table-bordered table-hover dataTable responsive no-wrap">
                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Address</th>
                                <th>City</th>
                                <th>State</th>
                                <th>Zip</th>
                            </tr>
                            </thead>
                            <tbody data-bind="dataTablesForEach: {data: data, dataTableOptions: {
                                      language: {
                                        'emptyTable': 'There are no results to display.'
                                      },
                                      searching: false,
                                      responsive: true,
                                      lengthMenu: [[5, 10, 20, 50, 100], [5, 10, 20, 50, 100]],
                                      order: [[ 1, 'asc' ]],
                                      columnDefs: [
                                        { width: '5%', targets: [4,5] }
                                    ]
                                  }
                              }">
                            <tr>
                                <td>
                                    <a href="JavaScript:" class="unsavedCheckIgnore"
                                        data-bind="click: $parents[1].selectGenerator, text: epaSiteId">
                                    </a>
                                </td>
                                <td data-bind="text: siteName"></td>
                                <td data-bind="text: siteAddress.street"></td>
                                <td data-bind="text: siteAddress.city"></td>
                                <td data-bind="text: siteAddress.state"></td>
                                <td data-bind="text: siteAddress.zip"></td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            <!-- /ko -->
        <!-- /ko -->
    </stripes:layout-component>
    <stripes:layout-component name="footer">
        <!-- ko with: popupModel -->
            <!-- ko if: showSearch -->
                <button type="button" class="btn btn-primary pull-left" data-bind="click: search">Search</button>
                <button type="button" class="btn btn-primary pull-left" data-bind="click: clearCriteria">Clear</button>
            <!-- /ko -->
            <!-- ko if: showResults -->
                <button type="button" class="btn btn-primary pull-left" data-bind="click: function(){showSearch(true);}">Back to Search Criteria</button>
                <button type="button" class="btn btn-default pull-left" data-bind="click: facilityNotFound">Site Not Found</button>
            <!-- /ko -->
        <!-- /ko -->
        <button type="button" class="btn btn-default pull-left" data-bind="close: 'cancel'">Close</button>
    </stripes:layout-component>
</stripes:layout-render>