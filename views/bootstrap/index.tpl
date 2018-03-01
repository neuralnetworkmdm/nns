<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<link rel="stylesheet" href= "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
		<style>
			.file-upload{display:none;}
			.file-upload-label{background-color:#fafafa; padding:7px; border:1px solid #ced4da; border-radius:5px;}
		</style>
		<link rel="icon" type="image/png" href="/assets/favicon.png">
		<title>NNS - Prototype</title>
	</head>
	<body>

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

		<div class="container-fluid">
			<div class="row" style="height:67vh;">

				<!-- ÉTUDE FIXE -->

				<div class="col-md-6 h-100" style="border-right: 1px dashed #aaa;">
					<div class="col-md-10 mx-auto d-flex justify-content-center">
						<h2 class="mb-4">Étude fixe</h2>
					</div>

					<ul id="clothing-nav" class="nav nav-pills justify-content-center mb-5" role="tablist">	
						<li class="nav-item">
							<a class="nav-link active" href="#basic" id="basic-tab" role="tab" data-toggle="tab" aria-controls="basic" aria-expanded="true">Configuration basique</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#advanced" role="tab" id="advanced-tab" data-toggle="tab" aria-controls="advanced">Configuration avancée</a>
						</li>
					</ul>

					<div class="col-sm-6 mx-auto">
						<div id="configuration-nav-content" class="tab-content">
							<div role="tabpanel" class="tab-pane fade show active" id="basic" aria-labelledby="basic-tab">
								<form method="post" action="/load" name="direct">
									<div class="form-group">
										<label for="learning_type">Mode d'apprentissage</label>
										<select class="form-control custom-select" id="learning_type" name="learning_type">
											<option value="supervised">supervisé</option>
											<option value="unsupervised">non-supervisé</option>
										</select>
									</div>
									<div class="form-group">
										<label for="number_of_img">Nombre d'images</label>
										<input class="form-control" id="number_of_img" name="number_of_img" type="number" min="0" max="50000" value="30000" required>
									</div>
									<div class="form-group">
										<label for="number_of_layers">Nombre de couches de neurones</label>
										<input class="form-control" id="number_of_layers" name="number_of_layers" type="number" min="2" max="5" value="3" required>
									</div>
									<div class="d-flex justify-content-center">
										<button type="submit" class="btn btn-primary">Lancer</button>
									</div>
								</form>
							</div>
							<div role="tabpanel" class="tab-pane fade text-center" id="advanced" aria-labelledby="advanced-tab">
								<form method="post" action="/load" name="parse" enctype="multipart/form-data">
									<div class="form-group">
										<label for="file" id="file-input-label" class="file-upload-label">Importer une configuration</label>
										<input type="file" accept=".ini, text/plain" id="file" class="form-control-file file-upload" required name="file">
									</div>
									<div class="form-group">
										<a href="/assets/config/default.ini" download="nns_default.ini">
											<button type="button" class="btn btn-link">Télécharger le modèle de configuration</button>
										</a>
									</div>
									<div class="d-flex justify-content-center">
										<button type="submit" class="btn btn-primary">Lancer</button>
									</div>
								</form>
							</div>
						</div>
					</div>
				</div>

				<!-- ÉTUDE PARAMÉTRIQUE -->

				<div class="col-md-6 h-100">
					<div class="col-md-10 text-center mx-auto">
						<div class="d-flex justify-content-center">
							<h2 class="mb-4">Étude paramétrique</h2>
						</div>
						<form method="post" action="/load" name="conf_ep" enctype="multipart/form-data">
							<div class="form-group">
								<label for="file_ep" id="file-input-label_ep" class="file-upload-label">Importer la configuration initiale</label>
								<input type="file" accept=".ini, text/plain" id="file_ep" class="form-control-file file-upload" required name="file">
								<select name="param" id="dynamicSelect" action="/load" class="custom-select" required>
									<option selected hidden disabled>Paramètre à étudier</option>
									<%
										with open("./assets/config/.editables","r") as opt:
											for i in opt.readlines():
									%>
												<option value="{{i}}">{{i}}</option>
									<%
											end
										end
									%>
								</select>
								<input type="hidden" value="file_ep" name="file_ep">
							</div>
							<div id="rangeOptionsConfig" style="display:none;">
								<div class="form-group row justify-content-center">
									<div class="col-sm-5">
										<label for="minValue">Valeur minimale</label>
										<input class="form-control" step="1e-16" placeholder="2e-9" id="minValue" name="minValue" type="number" required>
									</div>
									<div class="col-sm-5">
										<label for="maxValue">Valeur maximale</label>
										<input class="form-control" id="maxValue" placeholder="7e-5" step="1e-16" name="maxValue" type="number" required>
									</div>
								</div>
								<div class="form-group col-sm-4 mx-auto">
									<label for="npoints">Nombre de points</label>
									<input type="number" name="npoints" id="npoints" class="form-control" step="1" min="1" max="20" placeholder="10" required>
								</div>
							</div>
							<div class="form-group">
								<a href="/assets/config/default.ini" download="nns_default.ini"><button type="button" class="btn btn-link">Télécharger le modèle de configuration</button></a>
							</div>
							<div class="form-group">
								<button type="submit" class="btn btn-primary">Lancer</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>

		<!-- SCRIPTS IMPORTS -->

		<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
		<script src="/assets/js/file-input.js"></script>
	</body>
</html>
