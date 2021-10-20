/* Script para crear modelo relacional de base de datos */
CREATE TABLE IF NOT EXISTS  Empresa(
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_empresa TEXT NOT NULL UNIQUE,
    id_sede INTEGER NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES Sede(id_sede)
);

CREATE TABLE IF NOT EXISTS Sede(
    id_sede INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_sede TEXT NOT NULL UNIQUE,
    id_ciudad INTEGER NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES Ciudad(id_ciudad)
);

CREATE TABLE IF NOT EXISTS Ciudad(
    id_ciudad INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_ciudad TEXT NOT NULL UNIQUE,
    id_pais INTEGER NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES Pais(id_pais)
);

CREATE TABLE IF NOT EXISTS Pais(
    id_pais INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_pais TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Bodega(
    id_bodega INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_bodega TEXT NOT NULL UNIQUE,
    id_producto INTEGER NOT NULL,
    id_proveedor INTEGER NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor)
);

CREATE TABLE IF NOT EXISTS Persona(
    id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_persona TEXT NOT NULL,
    apellido_persona TEXT NOT NULL,
    telefono_persona TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    imagen_src TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Usuario(
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    contrasena TEXT NOT NULL,
    estatus_usuario INTEGER DEFAULT 1 NOT NULL,
    id_persona INTEGER UNIQUE NOT NULL,
    id_rol INTEGER NOT NULL,
    id_sede INTEGER NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES Sede(id_sede),
    FOREIGN KEY (id_persona) REFERENCES Persona(id_persona),
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE IF NOT EXISTS Rol(
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion_rol TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Proveedor(
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_proveedor TEXT NOT NULL,
    descripcion_proveedor TEXT NOT NULL,
    src_imagen TEXT NOT NULL,
    fecha_creado TEXT NOT NULL,
    id_empresa INTEGER NOT NULL,
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

CREATE TABLE IF NOT EXISTS Producto(
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_producto TEXT NOT NULL,
    descripcion_producto TEXT NOT NULL,
    cantidad_disponible INTEGER NOT NULL,
    calificacion REAL NOT NULL,
    src_imagen TEXT NOT NULL,
    fecha_creado TEXT NOT NULL,
    id_empresa INTEGER NOT NULL,
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);


/* Borrar modelo completo de la base de datos */
DROP TABLE Bodega;
DROP TABLE Ciudad;
DROP TABLE Pais;
DROP TABLE Persona;
DROP TABLE Producto;
DROP TABLE Proveedor;
DROP TABLE Rol;
DROP TABLE Sede;
DROP TABLE Usuario;
DROP TABLE Empresa;



/* Insertando valores de pruebas */
/* CREACION DE USUARIOS */
INSERT INTO Persona(nombre_persona, apellido_persona, telefono_persona, email, imagen_src)
VALUES ('Andres','Fonseca', '3005842614', 'andresmf@uninorte.edu.co', 'urlToImage.jpg'),
       ('Alvaro','Olmos', '3152469864', 'alope@uninorte.edu.co', 'urlToImage.jpg'),
       ('Cesar','Meneses', '3012563254', 'menesesac@uninorte.edu.co', 'urlToImage.jpg'),
       ('Jennifer','Gonzalez', '3209856614', 'jennifferg@uninorte.edu.co', 'urlToImage.jpg'),
       ('Jose','Rodriguez', '3586351614', 'jfonsecad@uninorte.edu.co', 'urlToImage.jpg');

INSERT INTO Rol(descripcion_rol)
VALUES ('usuario'),
       ('admin'),
       ('superAdmin');


INSERT INTO Pais(nombre_pais)
VALUES ('Colombia');

INSERT INTO Ciudad(nombre_ciudad, id_pais)
VALUES ('Bogota', 1),
       ('Barranquilla', 1),
       ('Valledupar', 1);

INSERT INTO Sede(nombre_sede, id_ciudad)
VALUES ('Principal', 1);

INSERT INTO Usuario(contrasena, id_persona, id_rol, id_sede)
VALUES ('Prueba123', 1, 2, 1),
       ('Prueba123', 2, 1, 1),
       ('Prueba123', 3, 2, 1),
       ('Prueba123', 4, 3, 1),
       ('Prueba123', 5, 1, 1);

INSERT INTO Proveedor(nombre_proveedor, descripcion_proveedor, src_imagen, fecha_creado, id_empresa)
VALUES ('Contactamos S.A.', 'Proveedor de llantas y amortiguadores', 'urlToImage.jpg', datetime('now', 'localtime'), 1),
       ('AsoMotores Asociados', 'Proveedor de motores', 'urlToImage.jpg', datetime('now', 'localtime'), 1),
       ('DistriCar', 'Proveedor de puertas y maquinas ensambladoras', 'urlToImage.jpg', datetime('now', 'localtime'), 1),
       ('Milenium Car', 'Proveedor de repuestos de motor, cojineria, tapiceria', 'urlToImage.jpg', datetime('now', 'localtime'), 1),
       ('Emselsa SA', 'Proveedor de llantas y rines', 'urlToImage.jpg', datetime('now', 'localtime'), 1);

INSERT INTO Producto(nombre_producto, descripcion_producto, cantidad_disponible, calificacion, src_imagen, fecha_creado, id_empresa)
VALUES ('Motor Toyota', 'Motor para camionetas 2.0', 20, 4.0, 'urlToImage',datetime('now', 'localtime'),1),
       ('LLantas Chaoyang', 'LLantas doble proteccion', 100, 4.5, 'urlToImage',datetime('now', 'localtime'),1),
       ('Puertas Chevroleth', 'Puerta original para Chevroleth Tracker', 10, 3.5, 'urlToImage',datetime('now', 'localtime'),1),
       ('Rines de lujo', 'Rin 15', 80, 3.2, 'urlToImage',datetime('now', 'localtime'),1),
       ('Motor Audi', 'Motor para camionetas Audi 3.0', 5, 5.0, 'urlToImage',datetime('now', 'localtime'),1);

SELECT usr.contrasena FROM Persona per, Usuario usr WHERE usr.id_persona = per.id_persona AND per.email = 'menesesac@uninorte.edu.co'