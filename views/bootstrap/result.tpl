<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<link rel="stylesheet" href= "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
		<link rel="icon" type="image/png" href="/assets/favicon.png">
		<title>NNS - Prototype</title>
	</head>
	<body class="h-100">
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
		<div class="container">
			<div class="row mb-3">
				<div class="mx-auto">
					<div class="my-3">
						<h4>Simulation n°{{timestamp}}</h4>
					</div>
					<% learning_rate_percent = learning_rate*100
					if(isinstance(learning_rate_percent,float)):
						if((learning_rate_percent).is_integer()):
							learning_rate_percent=int(learning_rate_percent)
						end
					end
					%>
					<p class="lead">Taux d'apprentissage : {{learning_rate_percent}}%</p>
				</div>
			</div>
			<div class="row">
				<div class="col-md-6 d-flex justify-content-center" style="border-right: 1px dashed #ddd;">
					<a href="{{img_src[0]}}" download><img class="img-fluid rounded" src="{{img_src[0]}}"></a>
				</div>
				<div class="col-md-6 d-flex justify-content-center">
					<a href="{{img_src[1]}}" download><img class="img-fluid rounded" src="{{img_src[1]}}"></a>
				</div>
			</div>
			<div class="row">
				<div class="mx-auto">
					<a href="{{zip}}" download><button class="btn btn-primary">Télécharger les résultats</button></a>
				</div>
			</div>
			<div class="row">
				<div class="mx-auto">
					<a href="/"><button class="btn btn-link">Retour Accueil</button></a>
				</div>
			</div>
		</div>
		<script src= "https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
		<script src= "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
		<script src= "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
	</body>
</html>
