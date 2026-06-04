CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_usuarios_id ON usuarios (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_usuarios_email ON usuarios (email);

CREATE TABLE IF NOT EXISTS ingredientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad DOUBLE PRECISION NOT NULL,
    unidad VARCHAR(50) NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS ix_ingredientes_id ON ingredientes (id);

CREATE TABLE IF NOT EXISTS recetas (
    id SERIAL PRIMARY KEY,
    nombre_plato VARCHAR(150) NOT NULL,
    ingredientes_json JSON NOT NULL,
    pasos_json JSON NOT NULL,
    tiempo_estimado VARCHAR(100) NOT NULL,
    dificultad VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS ix_recetas_id ON recetas (id);

CREATE TABLE IF NOT EXISTS calificaciones (
    id SERIAL PRIMARY KEY,
    estrellas INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    receta_id INTEGER NOT NULL REFERENCES recetas(id)
);

CREATE INDEX IF NOT EXISTS ix_calificaciones_id ON calificaciones (id);
