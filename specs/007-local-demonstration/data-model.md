# Data model007

No nuevas tablas. DemoPaths: workspace absoluto/raíz .oralia-demo, validación sin enlaces.
Marker: kind oralia-demo/schema1/workspace, no secreto. Fixtures manifest: schema1/profile
full|text_only/revisión1/course/material/activities(ids+modo), hashes de material. Seed
idempotente y transaccional; perfiles distintos requieren reset. RetentionPolicy1día,
actividad/política/versiones existentes. Sin consentimiento precargado.

Run receipt: run_id no secreto, PID/create_time del supervisor, workspace, puertos;
lock exclusivo protege lifecycle. Stop request: run_id. Lifecycle checking→preparing→
starting→ready→stopping→stopped; fallo limpia solo hijos propios. Reset solo stopped y
ruta marcada/confirmada, jamás importa base habitual. Logs no contienen credenciales.

La migración t007_demo_install completa index_rebuild_lock, tabla ya definida en Base pero ausente en instalaciones Alembic limpias. No introduce entidad nueva; se validan 32 tablas de aplicación y upgrade005. Cookies demo oralia_demo_admin/oralia_demo_participant separadas de las habituales; credencial solo en memoria/entorno del hijo API.
