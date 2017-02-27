<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<stripes:layout-definition>
<div class="panel panel-default panel-info">
	<div class="panel-heading">1-5. Generator Information</div>
	<div class="panel-body">
	
		<!-- ko if: generator().epaSiteId() -->
		<facility-info params="facilityInfo: generator"></facility-info>
		<hr>
		<!-- /ko -->
        <div class="row">
            <div class="col-sm-8">
                <button class="btn btn-primary" data-bind="click: generatorSearch.navigateSearch" data-toggle="modal" data-target="#search-facility-modal">Select<span data-bind="text: (generator().epaSiteId())?' Different ':''"></span> Generator</button>
            </div>
        </div>
	</div>
</div>
<stripes:layout-render name="/secured/modules/emanifest/common/search-facility-modal.jsp"/>
</stripes:layout-definition>