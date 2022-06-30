$(document).ready(function(){
    $("#input").keyup(function(){
            var query = $("#input").val()
            var host = window.location.hostname;
            var port = window.location.port;
            var url = "http://"+host+":"+port+"/api?q="+query;
			
            $.get(url, function(response){
                    console.log(response);
                }
			)
			
			function editDistance(str1, str2, m, n){
				if(m == 0){
					return n;
				}
				if(n == 0){
					return m;
				}
				if(str1[m-1] == str2[n-1]){
					return editDistance(str1, str2, m-1, n-1)
				}
				return 1 + Math.min(editDistance(str1, str2, m, n-1), editDistance(str1, str2, m-1, n),
							   editDistance(str1, str2, m-1, n-1));
			}
			function similarity(s1, s2) {
			  var longer = s1;
			  var shorter = s2;
			  if (s1.length < s2.length) {
				longer = s2;
				shorter = s1;
			  }
			  var longerLength = longer.length;
			  if (longerLength === 0) {
				return 1.0;
			  }
			  return (longerLength - editDistance(s2, s1, s2.length, s1.length)) / parseFloat(longerLength);
			}
			
			function sortFunction(a, b) {
				if (a[0] === b[0]) {
					return 0;
				}
				else {
					return (a[1] < b[1]) ? -1 : 1;
				}
			}

			$("form").on("submit", function (e) {
				e.preventDefault();
				$("#query").html("QUERY: "+query)
				$.get('random-data.txt', function(data) {
				var str1 = $("#input").val()
				var line = data.split(/\r?\n/);
				console.log(line);
				var arrDistance = [];
				var arrSimiliarity = [];
				var result = [[]];
				for (var i = 0; i < line.length; i++){
					aLineDistance = editDistance(str1, line[i], str1.length, line[i].length);
					aLineSimiliarity = similarity(str1, line[i]);
					if(aLineSimiliarity >= 0.7){
						result.push([line[i],aLineSimiliarity, aLineDistance]);
					}
				}
				sortResult = result.sort(sortFunction);
				console.log(sortResult);

				$("#result").html( sortResult[0][0] + "(" + sortResult[0][2] + ") : " + sortResult[0][1] +  
				"<br/>" + sortResult[1][0] + "(" + sortResult[1][2] + ") : " + sortResult[1][1] +  "<br/>" +
				sortResult[2][0] + "(" + sortResult[2][2] + ") : " + sortResult[2][1] +  "<br/>" +
				sortResult[3][0] + "(" + sortResult[3][2] + ") : " + sortResult[3][1] +  "<br/>" +
				sortResult[4][0] + "(" + sortResult[4][2] + ") : " + sortResult[4][1] +  "<br/>" +
				sortResult[5][0] + "(" + sortResult[5][2] + ") : " + sortResult[5][1] +  "<br/>" +
				sortResult[6][0] + "(" + sortResult[6][2] + ") : " + sortResult[6][1] +  "<br/>" +
				sortResult[7][0] + "(" + sortResult[7][2] + ") : " + sortResult[7][1] +  "<br/>" +
				sortResult[8][0] + "(" + sortResult[8][2] + ") : " + sortResult[8][1] +  "<br/>" +
				sortResult[9][0] + "(" + sortResult[9][2] + ") : " + sortResult[9][1]
				);
				}, 'text');
				
			})
        }
	)
}
)

