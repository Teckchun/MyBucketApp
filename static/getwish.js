 $(function() {
        $.ajax({
            url: '/getWish',
            type: 'GET',
            success: function(res) {
                console.log(res);
                var txt = "";
                for(var i in res){
                	console.log("RES"+res)
                txt +=`<div class="list-group">
		  <a href="#" class="list-group-item active">
		    <h4 class="list-group-item-heading">${"res[i].Title"}</h4>
		    <p class="list-group-item-text">${"res[i].Description"}</p>
		  </a>
		</div>`	

                }
                $('.jumbotron').append(txt);

            },
            error: function(error) {
                console.log(error);
            }
        });
    });