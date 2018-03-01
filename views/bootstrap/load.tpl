<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<link rel="stylesheet" href= "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
		<link rel="icon" type="image/png" href="/assets/favicon.png">
		<title>NNS - Prototype</title>
		<style>
			#progress{width:100%; background-color:#546e7a; border-radius:.2rem;}
			#progressbar{width:1%; height:25px; background-color:#00acc1; color:white; font-weight:bold; border-radius:.2rem;}
		</style>
	</head>

	<body class="h-100">

		<!-- HEADER -->

                <div class="jumbotron jumbotron-fluid text-center position-relative">
                        <nav class="navbar navbar-expand-lg position-absolute fixed-top">
                                <a class="navbar-brand" href="//www.ims-bordeaux.fr"><img src="/assets/images/logoimsjoom.png" height="52"></a>
                                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                                        <span class="navbar-toggler-icon"></span>
                                </button>
                                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                                        <div class="navbar-nav mr-auto">
                                        </div>
                                        <a href="//www.univ-pau.fr"><img src="/assets/images/uppa.png" height="52"></a>
                                </div>
                        </nav>
                        <div class="container">
                                <h1>NNS</h1>
                                <p class="lead text-muted">Neural Network Simulator</p>
                        </div>
                </div>

		<!-- BODY CONTENT -->

		<div class="container">
			<div class="row d-flex justify-content-center">
				<div class="row">
					<h4>Simulation n°{{timestamp}}</h4>
				</div>
				<table class="table table-hover table-bordered">
					<thead>
						<tr>
							<th scope="col">Paramètre</th>
							<th scope="col">Valeur</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td valign="middle">Progression <span style="float:right;"><a href="/cancel"><button class="btn btn-sm btn-primary">Annuler</button></a></span></td>
							<td><div id="progress"><div id="progressbar"></div><span style="white-space:nowrap; float:right;" class="d-flex justify-content-center">ETA : <span id="countdown"></span></span></div></td>
						</tr>
						<%
						for key,val in html_vars.items():
							if(key!="learning_rate")and(key!="timestamp")and(key!="html_vars"):
						%>
						<tr>
							<td>{{key}}</td>
							<td>{{val}}</td>
						</tr>
						<%
							end
						end
						%>
					</tbody>
				</table>
			</div>
			<div class="row">
				<div class="mx-auto">
					<a href="/cancel"><button class="btn btn-primary">Annuler</button></a>
				</div>
			</div>
		</div>

                <form method="post" action="/run" name="auto-submit" hidden>
                        <% for key,val in html_vars.items():
				if(key!="html_vars"): %>
			<input type="hidden" name="{{key}}" value="{{val}}">
			<%	end
			end %>
                </form>

		<!-- SCRIPTS IMPORTS -->

		<script src="/assets/js/countdown.js"></script>
		<script src="/assets/js/progress.js"></script>
		<script type="text/javascript">
			countdown({{eta}})
			progress({{eta}})
			document.forms["auto-submit"].submit();
		</script>
		<script src= "https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
		<script src= "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
		<script src= "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
	</body>
</html>
