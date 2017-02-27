<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<stripes:layout-definition>
  <div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel_searchFacility" 
  		data-keyboard="false" data-backdrop="static"
       	id="search-facility-modal"
       	aria-hidden="true" data-bind="with: generatorSearch">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"><span
                  aria-hidden="true">&times;</span><span
                  class="sr-only">Close</span></button>
            <h4 class="modal-title" id="myLargeModalLabel_searchFacility" data-bind="text: activePage"></h4>
        </div>
        <div class="modal-body">
            <!-- ko if: showSearch -->
            <stripes:layout-render name="/secured/modules/emanifest/common/search-facility-criteria.jsp"/>
            <!-- /ko -->
            <!-- ko if: showResults -->
            <stripes:layout-render name="/secured/modules/emanifest/common/search-facility-results.jsp"/>
            <!-- /ko -->
        </div>
        <div class="modal-footer">

        </div>
      </div>
    </div>
  </div>
</stripes:layout-definition>