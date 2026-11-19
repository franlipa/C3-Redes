# C3-Redes
forwarding a medias:c
Se utilizaron los ejemplos de la clasesita para las rutas de los test realizados en el informe. 
Solo basta tener todo en la misma carpeta y correrlo en la terminal con la siguiente estructura.
Primero parra generar los tres router se utiliza:
python forwarding.py router router_IP router_puerto router_rutas.txt 
Luego para enviar el mensaje:
python forwarding.py send IP_router_final puerto_router_final IP_envio puerto_envio "mensaje"
