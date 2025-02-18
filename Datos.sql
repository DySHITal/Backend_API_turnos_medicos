INSERT INTO Profesional (Nombre, Apellido, Correo, Especialidad, Numero_Matricula, Contrasena)
VALUES
('Juan', 'Pérez', 'juan.perez@ejemplo.com', 'Cardiología', 'MAT12345', 'contrasena123'),
('María', 'González', 'maria.gonzalez@ejemplo.com', 'Pediatría', 'MAT23456', 'contrasena234'),
('Carlos', 'López', 'carlos.lopez@ejemplo.com', 'Dermatología', 'MAT34567', 'contrasena345'),
('Laura', 'Martínez', 'laura.martinez@ejemplo.com', 'Psiquiatría', 'MAT45678', 'contrasena456'),
('Pedro', 'Sánchez', 'pedro.sanchez@ejemplo.com', 'Traumatología', 'MAT56789', 'contrasena567');

INSERT INTO Disponibilidad (Dias_Semana, Hora_Inicio, Hora_Fin, ID_Profesional)
VALUES
('Lunes,Martes,Miércoles,Jueves,Viernes', '09:00:00', '13:00:00', 1),
('Lunes,Martes,Miércoles,Jueves,Viernes', '14:00:00', '18:00:00', 1),
('Martes,Jueves,Sábado', '10:00:00', '14:00:00', 2),
('Martes,Jueves,Sábado', '18:00:00', '22:00:00', 2),
('Lunes,Miércoles,Viernes', '13:00:00', '17:00:00', 3),
('Lunes,Martes,Miércoles,Jueves,Viernes,Sábado', '09:00:00', '16:00:00', 4),
('Martes,Viernes', '15:00:00', '19:00:00', 5);

INSERT INTO Obra_Social (Nombre)
VALUES
('Sancor Salud'),
('IPS'),
('Swiss Medical'),
('Ospe'),
('Boreal');

INSERT INTO Profesional_ObraSocial (ID_Profesional, ID_ObraSocial)
VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 1),
(4, 5),
(5, 2);
