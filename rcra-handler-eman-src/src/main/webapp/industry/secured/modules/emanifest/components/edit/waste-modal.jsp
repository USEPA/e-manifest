<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="display" uri="http://displaytag.sf.net/el" %>
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>
<stripes:layout-render name="/industry/secured/modules/emanifest/common/modal-layout.jsp" title="Add Waste To Manifest" addClass="modal-lg modal-xlg" id="manifestWasteSectionModal">
    <stripes:layout-component name="body">
        <!-- ko if: waste -->
        <div class="row">
            <div class="col-sm-12">
                <div class="form-group" data-bind="with: waste">
                    <label class="control-label" for="hazWaste">9a. Hazardous Material?</label>
                    <bs-switch params="enable: $parent.generatorPartialEdit, flag: isHazardous"></bs-switch>
                </div>
            </div>
        </div>
        <div class="panel panel-info">
            <div class="panel-heading">9b. U.S. DOT Description</div>
            <div class="panel-body">
                <!-- ko if: generatorPartialEdit -->
                <dot-description-review params="data: waste()"></dot-description-review>
                <!-- /ko -->
                <!-- ko ifnot: generatorPartialEdit -->
                    <dot-description params="data: waste(), tsdf: tsdf, generatorPartialEdit: generatorPartialEdit"></dot-description>
                <!-- /ko -->
            </div>
        </div>
        <div class="panel panel-info">
            <div class="panel-heading">10-12. Containers and Quantity</div>
            <div class="panel-body">
                <containers params="data: waste(), tsdf: tsdf, generatorPartialEdit: generatorPartialEdit"></containers>
            </div>
        </div>
        <div class="panel panel-info">
            <div class="panel-heading">13. Hazardous Waste Codes</div>
            <div class="panel-body">
                <waste-codes params="data: waste(), tsdf: tsdf, generatorPartialEdit: generatorPartialEdit, generator: generator"></waste-codes>
            </div>
        </div>
        <div class="panel panel-info">
            <div class="panel-heading">Special Handling Instructions and Additional Information</div>
            <div class="panel-body">
                <waste-handling-instructions params="data: waste(), tsdf: tsdf, generatorPartialEdit: generatorPartialEdit, internationalShipment: internationalShipment"></waste-handling-instructions>
            </div>
        </div>
        <!-- /ko -->
    </stripes:layout-component>
    <stripes:layout-component name="footer">
        <div class="row">
            <div id="wasteButtonToolbar" class="col-sm-12 btn-toolbar">
                <button class="btn btn-primary" data-bind="close: popupModel().saveAndClose">Save &amp; Return</button>
	         <!-- ko ifnot:  popupModel().generatorPartialEdit -->
                 <button class="btn btn-primary" data-bind="close: popupModel().addAndContinue">Save &amp; Add New</button>
                 <!-- /ko -->
                <button class="btn btn-default" data-bind="close: 'cancel'">Cancel</button>
            </div>
        </div>
    </stripes:layout-component>
</stripes:layout-render>
