-- Crear la base de datos
CREATE DATABASE TurnosDB;
USE TurnosDB;

-- Tabla: Profesional_Médico
CREATE TABLE Profesional (
    ID_Profesional INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Apellido VARCHAR(255) NOT NULL,
    Correo VARCHAR(255) NOT NULL,
    Especialidad VARCHAR(255) NOT NULL,
    Numero_Matricula VARCHAR(50) UNIQUE NOT NULL,
    Contrasena VARCHAR(255) NOT NULL
);

-- Tabla: Paciente
CREATE TABLE Paciente (
    ID_Paciente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Apellido VARCHAR(255) NOT NULL,
    Correo VARCHAR(255) UNIQUE NOT NULL,
    Dni INT UNIQUE NOT NULL,
    Obra_social VARCHAR(255),
    Contrasena VARCHAR(255) NOT NULL
);

-- Tabla: Turno
CREATE TABLE Turno (
    ID_Turno INT AUTO_INCREMENT PRIMARY KEY,
    Fecha DATE NOT NULL,
    Hora TIME NOT NULL,
    Estado ENUM('Reservado', 'Cancelado por Paciente', 'Cancelado por Profesional') NOT NULL,
    ID_Paciente INT NOT NULL,
    ID_Profesional INT NOT NULL,
	CONSTRAINT UC_FechaHoraProfesional UNIQUE (Fecha, Hora, ID_Profesional),
    FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente),
    FOREIGN KEY (ID_Profesional) REFERENCES Profesional(ID_Profesional)
);

-- Tabla: Horario_Atención
CREATE TABLE Disponibilidad (
    ID_Horario INT AUTO_INCREMENT PRIMARY KEY,
    Dia_Semana ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo') NOT NULL,
    Hora_Inicio TIME NOT NULL,
    Hora_Fin TIME NOT NULL,
    ID_Profesional INT NOT NULL,
    FOREIGN KEY (ID_Profesional) REFERENCES Profesional(ID_Profesional)
);

-- Tabla: Obra_Social
CREATE TABLE Obra_Social (
    ID_ObraSocial INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla: Profesional_ObraSocial (relación muchos a muchos entre Profesional_Médico y Obra_Social)
CREATE TABLE Profesional_ObraSocial (
    ID_Profesional_ObraSocial INT AUTO_INCREMENT PRIMARY KEY,
    ID_Profesional INT NOT NULL,
    ID_ObraSocial INT NOT NULL,
    FOREIGN KEY (ID_Profesional) REFERENCES Profesional(ID_Profesional),
    FOREIGN KEY (ID_ObraSocial) REFERENCES Obra_Social(ID_ObraSocial)
);

-- Tabla: Cancelación
CREATE TABLE Cancelacion (
    ID_Cancelacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_Turno INT NOT NULL,
	ID_Paciente_cancelacion INT DEFAULT NULL,
    ID_Profesional_cancelacion INT DEFAULT NULL,
    Fecha_Cancelacion DATETIME NOT NULL,
    Razon TEXT,
    FOREIGN KEY (ID_Turno) REFERENCES Turno(ID_Turno),
    CONSTRAINT fk_cancelacion_paciente FOREIGN KEY (id_paciente_cancelacion) REFERENCES turnosDB.paciente(ID_Paciente),
	CONSTRAINT fk_cancelacion_profesional FOREIGN KEY (id_profesional_cancelacion) REFERENCES turnosDB.profesional(ID_Profesional)
);

-- Tabla: Realizado_por
CREATE TABLE Realizado_por (
    ID_realizado_por INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cancelacion INT NOT NULL,
    ID_Paciente INT,
    ID_Profesional INT,
    FOREIGN KEY (ID_Cancelacion) REFERENCES Cancelacion(ID_Cancelacion),
    FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente),
    FOREIGN KEY (ID_Profesional) REFERENCES Profesional(ID_Profesional)
);