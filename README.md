
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
![image](https://user-images.githubusercontent.com/83615514/202870082-ea85217d-b284-44bf-bd9d-d816289599d8.png)


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

## 8-

