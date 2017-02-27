<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<stripes:layout-definition>
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
                    	<a href="#" data-bind="click: function(data, event){$root.generatorSearch.selectGenerator($data,event);}">
                    		<span  data-bind="text: epaSiteId"></span>
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
</stripes:layout-definition>