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
    telefono_persona TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    imagen_src TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Usuario(
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    contrasena TEXT NOT NULL,
    estatus_usuario INTEGER DEFAULT 1 NOT NULL,
    id_persona INTEGER NOT NULL,
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
    id_proveedor INTEGER NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor)
);

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
