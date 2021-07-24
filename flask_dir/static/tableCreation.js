//  alternative choice use a button get response   $("button").click(function(){
//    $("#div1").load("/static/textFile.txt", function(responseTxt, statusTxt, xhr){

$(document).ready(function() {
    $.ajaxSetup({ cache: false });
//    $("#button").click(function(){
//    if it's a button , need to clean up ( remove children ) before dynamically creating th etable
//  .. otherwise get multiple table entries stacking everytime push button

//    $.get("/static/warning_log.txt", function(data, status) {

    var check = $.get("/static/warning_log.txt", function(data, status) {
      console.log( "success" );
    })
      .fail(function() {
        alert( "Error loading warning logs" );
      })
      .always(function() {
        console.log( "finished" );
      });
    check.always(function(data, status) {


// alternative choice use the get instead loading into div https://www.w3schools.com/jquery/jquery_ajax_get_post.asp
//    var name = responseTxt;
//      if(status == "error")  if(status == "success")

            var name = data;
            var splittext = name.split(/[\r\n]+/)
            var textForCell = name.split(",")

  			const tableDiv = document.querySelector("#logContent")
  			// try to select this parent to remove children, cleanup

//            let tableHeaders = ["Warning","Time","Description"]
            let tableHeaders = ["Warning","Date Time"]

            const createTable = () => {
            // TODO -remove all children elements upon creation

//               while (warnTableDiv.firstChild) {
//            parent.removeChild(warnTableDiv.firstChild);
//            }


//            while (warnTableDiv.firstChild) parent.removeChild(warnTableDiv.firstChild)
//          while (tableDiv.firstChild) tableDiv.removeChild(tableDiv.firstChild)
            let warningtable = document.createElement('table')
            warningtable.id = 'warningTable'
            let warningTableHead = document.createElement('thead')
            warningTableHead.id = 'warningTableHead'
            let warningTableRow = document.createElement('tr')
            warningTableHead.id = 'warningTableRow'

            tableHeaders.forEach(header=> {
            	let scoreHeader = document.createElement('th')
            	scoreHeader.innerText = header
            	warningTableRow.append(scoreHeader)
            })

            warningTableHead.append(warningTableRow)
            warningtable.append(warningTableHead)
            let warningTableBody = document.createElement('tbody')
            warningTableBody.id = 'tableBody'
            warningtable.append(warningTableBody)
            tableDiv.append(warningtable)

            for (p=0; p < splittext.length; p++) {
              // iterate through each line of the warning logs
            		var warningTableRowCells = document.createElement('tr')
                // create a row for the table (above header alread cretaed and appended to newly created table)
            		warningTableRowCells.class = 'warningRowCells'
            		line = splittext[p]
                // store a single line from warning log
            		console.log(line)

      		 			for (j=0; j < tableHeaders.length; j++) {
                  // iterate through each entry within a warning log line
      		 				lineSection = line.split(',');
      		 				section = lineSection[j];
      		 				console.log(section)

      		 				var cell = document.createElement("td");
                  // create a cell
      		 				var celltext = document.createTextNode(section)
                  // get content for the cell, warning entry
      		 				cell.appendChild(celltext);
                  //append to the cell
      		 				warningTableRowCells.appendChild(cell);
                  // append to the row
		 			}

	 			warningTableBody.appendChild(warningTableRowCells)
        //append row to table body (table body is a child of the table, within table )
        // add footer if needed
		 			}

	 			warningTableBody.appendChild(warningTableRowCells)
        //append row to table body (table body is a child of the table, within table )
        // add footer if needed
	 		};
            createTable();
          });  // end create table
        }); // end of ajax