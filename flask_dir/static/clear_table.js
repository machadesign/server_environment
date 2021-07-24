// clear table
$("#clear-warnings").click(function(e) {
  if (confirm("Do you want to clear warning log?")) {
//    txt = "You pressed OK!";
//    alert(txt)
    $.ajaxSetup({ cache: false });
      var cleared_warnings = false;
//      alert('warning log cleared')
      $("#logContentBox").empty()
      e.preventDefault();
      $.ajax({
          type: 'POST',
          url: '/clear_logs',
          data: { id: $(this).val() },
          success: function(data,status,xhr){
//                alert('success')
                cleared_warnings = true;
            //code to open in new window comes here
          },
          error: function(xhr, status, error){
             if(xhr.status != 200){
            alert("Error!" + xhr.status);
          }
          },
          complete: function(){
            alert('warning log cleared')
          if(cleared_warnings == true){
                alert('Issue clearing warnings');
          }
          },
          dataType: "xml"
      });
      } else {
      alert("Do nothing!")
      }
    });


     // if request.form['btn'] == 'Save'