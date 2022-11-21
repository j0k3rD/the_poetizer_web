
<pre>
 ______                                                           _                       _ 
(_____ \                                                         (_)                     | |
 _____) )  ____   ___    ____   ____  _____  ____   _____   ____  _   ___   ____   _____ | |
|  ____/  / ___) / _ \  / _  | / ___)(____ ||    \ (____ | / ___)| | / _ \ |  _ \ (_____)| |
| |      | |    | |_| |( (_| || |    / ___ || | | |/ ___ |( (___ | || |_| || | | |       | |
|_|      |_|     \___/  \___ ||_|    \_____||_|_|_|\_____| \____)|_| \___/ |_| |_|       |_|
                       (_____|                                                              
</pre>

Prof. Andrea Navarro - @AndreaNavarroMoreno -- Prof. Matias Navarro 

-----------------------------------------------------------------------------------------------------------------------------------------

En este proyecto nos enfocaremos en crear una página web para Poetas.

<br>

<p align='center'>
 <img src='https://user-images.githubusercontent.com/83615514/202943480-72f8dadd-8d37-468e-a9bf-16638dbb4410.png'>
</p>


Teniendo en cuenta los siguientes topicos: 

-----------------------------------------------------------------------------------------------------------------------------------------

  ##
## 1- BACKEND Y FRONTEND
  - Creacion de Entorno Virtual e instalacion de complementos para la correcta creacion del mismo.
  ![image](https://user-images.githubusercontent.com/83615514/202869917-6105b45e-2660-406b-b11e-dac463d22786.png)


## 2- CREACION DE API REST (BACKEND)
  - cURL
  ![image](https://user-images.githubusercontent.com/83615514/202869946-27aeef8d-80ca-4bef-8de4-0bb0b49f7a83.png)
  ![image](https://user-images.githubusercontent.com/83615514/202869960-243388e2-b294-4839-92b5-096efa27a6ef.png)


## 3- BASE DE DATOS (BACKEND)
  - Decidimos usar una base de datos SQL por su facil uso que le podemos dar con Python, ademas de que solo vamos a almacenar datos en formato plano (nada de contenido digital).
  Lo que hicimos fue crear las relaciones entre las tablas.
  ![image](https://user-images.githubusercontent.com/83615514/202870493-00450846-eac0-42c4-bdab-8206a895e501.png)
  ![image](https://user-images.githubusercontent.com/83615514/202870539-61b5a612-0c68-4bb9-9c98-f67401c752cb.png)


## 4- FILTRADO Y PAGINACION (BACKEND)
  -  Creamos los filtros en las consultas donde corresponde y aplicamos paginacion para luego poder mostrar los recursos como el usuario quiera de forma ordenada.
  ![image](https://user-images.githubusercontent.com/83615514/202876183-4485a70d-29e5-41c4-9192-cd1ed70624aa.png)
  ![image](https://user-images.githubusercontent.com/83615514/202876186-5939b5e6-5c20-4dc8-910b-50db38d4ab6a.png)

## 5- AUTENTICACION JWT (BACKEND)
  - Implementamos los métodos de autenticación (Register y Login), protegimos las rutas de acuerdo a los requisitos, modificamos la implementación dependiendo del rol donde sea necesario.
 ![image](https://user-images.githubusercontent.com/83615514/202876276-ba7d8860-7056-4c51-b2cb-5df17e9f60a1.png)
 ![image](https://user-images.githubusercontent.com/83615514/202876281-40c9a6fc-4d9e-4774-8a60-ecc3ff5476ee.png)
 ![image](https://user-images.githubusercontent.com/83615514/202876301-e24c1ae1-6047-4767-8cd4-c5899b17b1e6.png)
 ![image](https://user-images.githubusercontent.com/83615514/202876327-02121067-b93f-44de-83b2-0deccf7eb8fb.png)

## 6- Envio de Email (BACKEND)
  - Para esto hicimos uso de la libreria Email Sending de Flask, basicamente lo que nos permite es enviar un email al poeta una vez que se ha concretado su registro en la pagina y cuando algun otro poeta comenta un poema de el. Ademas creamos platillas simples en HTML (raw, txt, normal) que seran las que el poeta recibira en su correo.
  ![image](https://user-images.githubusercontent.com/83615514/202876406-f70d6589-48be-400f-ba2b-5a05a711ad3a.png)
  ![image](https://user-images.githubusercontent.com/83615514/202876412-b9c8b5d4-9c55-4733-88b2-65d1262b11f2.png)
  ![image](https://user-images.githubusercontent.com/83615514/202876427-2a0a0498-1154-4b4b-b03c-afd6d48537fd.png)
  ![image](https://user-images.githubusercontent.com/83615514/202876467-5ae8f3c2-c43c-417f-a383-0024c570935e.png)

## 7- BOCETOS PARA FRONTEND
  - Creamos modelos para tener una mejor idea de como queriamos que se viera nuestra pagina web, lo que nos ayudara a luego poder pasar todas las ideas e implementaciones a codigo. Puedes ver mis bocetos en la pagina de Figma.com (https://www.figma.com/file/Qf4m2hZcihMOkdT7JoC43m/THE-POETIZER-(maquetacion)?node-id=105%3A225&t=8GLDC4MptIcYlWyU-1)
  ![image](https://user-images.githubusercontent.com/83615514/202876568-feb1095f-b3f1-4d25-9761-d110b5f18e4a.png)

## 8- VISTAS BOOTSTRAP
- Procedemos a volcar nuestras maquetas a codigo, realizando nuestros primero HTML TEMPLATES y codeando algunos estilos adicionales en CSS. Ya que hicimos uso de Bootstrap para la creacion de las mismas, teniendo como ejemplo guia de codigo algunas navbars, tablas, formularios, etc, que aparecian en su pagina web.
![image](https://user-images.githubusercontent.com/83615514/202876729-614c7209-c3fe-4379-bad4-5c6d33e04180.png)

## 9- ENRUTAMIENTO SERVIDOR FLASK
- Con la ayuda de librerias como redirect, render_templates, url_for, etc, que son propias de Flask, comenzamos con el enrutamiento de nuestra pagina. Pudiendo realizar los primeros desplazamientos entre los diferentes templates con los botones que habiamos creado en los mismos.
![image](https://user-images.githubusercontent.com/83615514/202876927-3dea38f6-9ad4-454e-909e-3283cd35fcec.png)
![image](https://user-images.githubusercontent.com/83615514/202876941-2bdd39cf-00ed-43e9-a971-8a1cf1dfa5f6.png)

## 10- JINJA2
- Jinja2 es un motor de renderizado de Flask el cual lo implementamos para no tener tanto código repetido en nuestros templates. Lo que hicimos fue crear un 'base.html' el cual, como su nombre lo indica, tiene todas las partes que se repetirian en todos los templates como navbars, menus, footer, etc. Nos ayuda a poder integrar todo esto en los demas templates sin tener que repetir esto en cada uno de ellos.
 ![image](https://user-images.githubusercontent.com/83615514/202944417-68bd5a12-c357-479e-badd-ff2e08959f18.png)
 ![image](https://user-images.githubusercontent.com/83615514/202944529-ce8e91cc-1102-4649-95b6-cf3e1907437d.png)
 ![image](https://user-images.githubusercontent.com/83615514/202944559-4f154603-652e-4a5e-8f47-dae8efbaa518.png)
 ![image](https://user-images.githubusercontent.com/83615514/202944985-fd36d243-51d4-415b-8405-7b823d47324c.png)

## 11- REQUESTS Y PROTECCION DE LAS VISTAS
- Por último lo que hicimos fue terminar de enlazar nuestro servidor Backend con el servidor Frontend a través de Requests a la base de datos. Lo que hacemos es tomar todas las peticiones que realiza el usuario a traves de la página, enviarlas a al Backend en forma de consulta y este a su vez, tambien devolver una respuesta con consultas. Y por supuesto, protegimos todas las vistas para que los usuarios que no estuvieran logueados no puedan acceder a rutas en donde sea necesario el token.
  ![image](https://user-images.githubusercontent.com/83615514/202945178-ac37836b-29ef-4224-9975-8a7326b7b261.png)
  ![image](https://user-images.githubusercontent.com/83615514/202945343-826d1014-4f2c-4355-bded-b060aa04a210.png) 


### Bibliografia
INSOMNIA = Insomnia es un cliente REST multiplataforma.
FLASK = 

