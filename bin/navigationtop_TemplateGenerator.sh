#!/bin/sh
#WDN
#define parameters which are passed in.
GalaxyServer=$1
#define the template.
cat  << EOF
<!--
   navigation.html
   
   Copyright 2016 root <>
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
   MA 02110-1301, USA.
   
   
-->

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

 {% load static %}
</head>
  

	<script src="{% static "slider/bootstrap-slider.min.js" %}" ></script>
	<link href="{% static "slider/bootstrap-slider.min.css"  %}" rel="stylesheet" type="text/css">	
	<!-- Custom Theme JavaScript -->
	<script src="{% static "dist/js/sb-admin-2.js"  %}" ></script>

	<body>
	   	
	
	
	
	
	<!-- Navigation -->
	<nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0;background-color: #669999;">
		<div class="navbar-header">
			
<!--
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
								<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</button>
-->

		</div>
		
		<ul class="nav navbar-top-links navbar-left">
		
<li><div class="dropdown">
	<a href={% url 'sequencer:projects' %}><font color = "white">HEGP Analysis Manager v1.1</font></a>
</div>

			</li>

		</ul>
		<ul class="nav navbar-top-links navbar-right">
			<!-- /.dropdown -->
			<li><div class="dropdown">
				<a href="$GalaxyServer/">				
					<img src="{% static "sequencer/galaxyIcon_noText.png" %}" alt="My image"/>
				<font color = "white">Retour vers Galaxy</font></a>
				</div>
			</li> 
			<li>
										<div class="dropdown">
							<a class="dropdown-toggle" data-toggle="dropdown" href="#"  style="background-color: #669999;">
								<i class="fa fa-user fa-fw" style="color: black;"></i> <i class="fa fa-caret-down" style="color: black;"></i>
									<font color = "white">
										{% if user.is_authenticated %}
											Envoyer à {{user.username }}
										{% else %}
											Sélectionnez un utilisateur											
										{% endif %}
									</font>
							</a>
			<ul class="dropdown-menu dropdown-user" style="padding: 2px;margin: 5px;">
<!--
								<li><a href="#"><i class="fa fa-user fa-fw" style="color: black;"></i> 
								{% if user.is_authenticated %}
									Envoyer à  {{user.username }}
								{% else %}
									Sélectionnez un utilisateur
								{% endif %}	   
									</a>
								</li>
-->
								<li class="divider"></li>
								<li>
									<a href="{% url 'sequencer:getgalaxyusers' %}" >
									<center>
										<button class="btn btn-default"  style="color: black;background-color: #669999;">
<!--
										<button class="btn btn-info">
-->
										<i class="fa fa-refresh fa-fw"></i>
										</button> 
									</center>	
									</a>
								</li>

								<li class="divider"></li>
								<li class="divider"></li>
								{% if users %}
									{% for galaxy_user in users %}
								<li>
								<form action={% url 'sequencer:vote' galaxy_user.user_id %} method="post">
								{% csrf_token %}
										{% if user.is_authenticated  %}
										<!--if user authenticated = galaxy user put the button in green-->
											{% if user.username == galaxy_user.user_email %}
											<button type="submit" class="btn btn-success btn-circle">
												<i class="fa fa-user fa-fw"></i>
											</button> {{ galaxy_user.user_email }}
											<!--else put it in white-->
											{% else %}
											<button type="submit" class="btn btn-default btn-circle">
												<i class="fa fa-user fa-fw"></i>
											</button> {{ galaxy_user.user_email }}
											{% endif %}	
										{% else %}
											<button type="submit" class="btn btn-default btn-circle">
												<i class="fa fa-user fa-fw"></i>
											</button> {{ galaxy_user.user_email }}									
										{% endif %}
								</form>
								</li>
								<li class="divider"></li>
									{% endfor %}
								{% else %}	
								






								
								
								
								
								
									
							<p>pas d'utilisateur</p>
							{% endif %}	                                         
							</ul>
						</div>
							
			</li> 
   
			

<!--
			<li>
				<a href={% url 'sequencer:projects' %}><i class="fa fa-dashboard fa-fw"></i>Run</a>
			</li>
-->
		</ul>
		<!-- /.navbar-static-side -->
	</nav>      
	</body>
</html>
EOF
